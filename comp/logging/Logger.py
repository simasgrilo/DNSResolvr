import logging
import requests
from flask import request

class Logger(logging.Logger):
    """
    Python class to log messages to a file, encapsuling calls to the standard logging module.
    The format of this logger is the same as described in LogAggregator (https://github.com/simasgrilo/log-aggregator)
    """
    def __init__(self, log_file_path, log_level=logging.INFO):
        """
        Args:
            log_file_path (str): path to the file where the logs will be written
            log_level (int): level of criticality of the log entry. Defaults to INFO
        """
        super().__init__(__name__)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(log_level)
        self.__formatter = logging.Formatter('%(asctime)s - %(client_ip)-15s %(process)d - %(levelname)s - %(funcName)s - %(filename)s - %(message)s')
        self.__file_handler = logging.FileHandler(log_file_path) #the handler defines where the info will be logged. for now, all logged info will be written to a file
        self.__file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__file_handler)
        
    @property
    def logger(self):
        return self.__logger
    
class IPLogAdapter(logging.LoggerAdapter):
    """
    Python class to log messages to a file, encapsuling calls to the standard logging module.
    The format of this logger is the same as described in LogAggregator 
    """
    
    def process(self, msg, kwargs):
        """
        Args:
            msg (str): message to be logged
            kwargs (dict): dictionary containing the log level
        """
        return f'{self.extra["client_ip"]} - {msg}', kwargs
    
    