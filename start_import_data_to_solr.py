import os
import logging
from logging.handlers import TimedRotatingFileHandler as TimedRotatingFileHandler
import schedule
import time

log_folder = './../.log/'

class WholeIntervalTimedRotatingFileHandler(TimedRotatingFileHandler):
    """A class to manage the backup compression.
    Args:
        TimedRotatingFileHandler ([type]): [description]
    """
    def __init__(self, filename="", when="midnight", interval=1, backupCount=0):
        super(WholeIntervalTimedRotatingFileHandler, self).__init__(
            filename=filename,
            when=when,
            interval=int(interval),
            backupCount=int(backupCount))
    
    def computeRollover(self, currentTime):
        if self.when[0] == 'w' or self.when == 'midnight':
            return super().computeRollover(currentTime)
        return ((currentTime // self.interval) + 1) * self.interval

    def doRollover(self):
        super(WholeIntervalTimedRotatingFileHandler, self).doRollover()
        

if not os.path.exists(log_folder):
    os.makedirs(log_folder)
logger = logging.getLogger(__name__)
filename = log_folder + __name__  + '.log'
file_handler = WholeIntervalTimedRotatingFileHandler(filename=filename, when='midnight', interval=1, backupCount=30)#when midnight, s (seconds), M (minutes)... etc
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def job():
    try:
        cmd = "python ./.util/import_data_to_solr.py -c ../.config/.configs.yml"
        result = os.system(cmd)
        logger.info(f'importing data done with no exception. Exit status {result}')
        print(f'importing data done with exit status {result}')
    except Exception as exp:
        logger.warning(f'importing data failed with exit status {result}')
        print(f'importing data failed with exit status {result}')

job()

schedule.every(24).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(2)
