from comp.utils import UTCTimeStampCalculator
import requests
from requests.exceptions import ConnectionError as ReqConnectionError
from comp.logging import Logger
import json
import time


class LogFlush:
    """
    Class to dispatch logs to the destination. This class is responsible for reading the log file existing for the server, dispatching it to the destination and upon success,
    cleaning the directory by removing the file.
    """
    
    def __init__(self, config, logger: Logger):
        """
        Initializes the LogFlush class with the configuration read from the file provided upon server initalization
        Args:
            config (dict): Configuration dict read from file
        """
        #self._logger = Logger().logger
        self._logger = logger
        self._config = config
        self._backoff = 1
    
    @property
    def config(self):
        return self._config
    
    @property
    def logger(self):
        return self._logger
    
    def read_file(self, file_path: str):
        content = None
        with open(file_path, "rt") as fp:
            content = "".join(fp.readlines())
            return content
    
            
    def flush(self, file_path: str):
        """
        Method to flush the log file to the LogAggregator service
        """
        print("flush 'em")
        content = self.read_file(file_path)
        url = "{}://{}:{}{}".format(self.config["LogAggregator"]["protocol"], self.config["LogAggregator"]["host"], self.config["LogAggregator"]["port"], self.config["LogAggregator"]["endpoint"])
        try:
            #requests.post(url=url,json=json.dumps(content))
            requests.post(url=url, data=content)
        except ConnectionError and ReqConnectionError as e:
            self.logger.error("Error trying to connect to {}: {}".format(url, e.__str__()), 500)
        except TimeoutError:
            # TODO enhance the backoff logic. this is not threadsafe and might occur in wrong values for the backoff
            # maybe a queue could be useful here
            self.logger.error("Timeout error occurred. Retrying in {} seconds".format(self._backoff))
            time.sleep(self._backoff)
            self._backoff += 5
            self.flush(file_path)
            self._backoff = 1
        except Exception as e:
            import traceback
            traceback.print_exception(e)
            
    def schedule_flush(self, file_path: str):
        """
        Schedules a task to flush the content of the log. this can be based on either minutes, days or hours.
        Although the content in the config.json file is in a human-readable format, sched expects it to be UTC timestamp, so everything is converted to seconds.
        Note that this needs to use async primitive from asyncio as it blocks the whole application
        """
        days = UTCTimeStampCalculator.days(self.config["logSchedule"]["days"]) if "logSchedule" in self.config and "days" in self.config["logSchedule"] else 0
        hours = UTCTimeStampCalculator.hours(self.config["logSchedule"]["hours"]) if "logSchedule" in self.config and "hours" in self.config["logSchedule"] else 0
        minutes = UTCTimeStampCalculator.minutes(self.config["logSchedule"]["mins"]) if "logSchedule" in self.config and "mins" in self.config["logSchedule"] else 0
        wait_time = days + hours + minutes
        while True:
            print("flush job will execute in {} seconds".format(wait_time))
            time.sleep(wait_time)
            self.flush(file_path)
