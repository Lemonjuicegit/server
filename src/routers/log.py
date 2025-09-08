import logging
import sys
import time
from loguru import logger as loguru_logger
from pathlib import Path
logpath_info = Path.cwd() / "log" / 'info'
logpath_error = Path.cwd() / "log" / 'error'
logpath_warning = Path.cwd() / "log" / 'warning'
def createlog(path):
    if not logpath_info.exists():
        logpath_info.mkdir(parents=True)
    if not logpath_error.exists():
        logpath_error.mkdir(parents=True)
    if not logpath_warning.exists():
        logpath_warning.mkdir(parents=True)
           
    logger = logging.getLogger(__name__)
    logger.setLevel('INFO')
    formatter = logging.Formatter("%(asctime)s %(filename)s 第%(lineno)s行: %(message)s")
    
    handler = logging.FileHandler(logpath_info / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}INFO.log", encoding="utf-8")
    handler.setLevel('INFO')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    handler_err = logging.FileHandler(logpath_error / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}ERROR.log", encoding="utf-8")
    handler_err.setLevel('ERROR')
    handler_err.setFormatter(formatter)
    logger.addHandler(handler_err)
    
    handler_war = logging.FileHandler(logpath_warning / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}WARNING.log", encoding="utf-8")
    handler_war.setLevel('WARNING')
    handler_war.setFormatter(formatter)
    logger.addHandler(handler_war)
    
    return logger


class Loggin:
    def __init__(self) -> None:
        debug = True
        if debug:
            self.level = "DEBUG"
        else:
            self.level = "INFO"
        self.ERROR_LOG = logpath_error / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}ERROR.log"
        self.INFO_LOG = logpath_info / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}INFO.log"
        self.WARNING_LOG = logpath_warning / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}WARNING.log"
    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=self.ERROR_LOG,rotation="10 MB", retention='10 days',level='ERROR')
        loguru_logger.add(sink=self.INFO_LOG,rotation="10 MB", retention='10 days',level='INFO')
        loguru_logger.add(sink=self.WARNING_LOG,rotation="10 MB", retention='10 days',level='WARNING')
        return loguru_logger
loggin = Loggin()
logger = loggin.setup_logger()
