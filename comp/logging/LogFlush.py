from comp.utils import UTCTimeStampCalculator
import requests
from requests.exceptions import ConnectionError as ReqConnectionError
import json
import time
import sched


class LogFlush:
    """
    Class to dispatch logs to the destination. This class is responsible for reading the log file existing for the server, dispatching it to the destination and upon success,
    cleaning the directory by removing the file.
    """
    
    def __init__(self, config):
        """
        Initializes the LogFlush class with the configuration read from the file provided upon server initalization
        Args:
            config (dict): Configuration dict read from file
        """
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._config = config
        self._backoff = 1000
    
    @property
    def config(self):
        return self._config
    
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
            requests.post(url=url,json=json.dumps(content))
            print("request sent")
        except ConnectionError and ReqConnectionError as e:
            return "Error trying to connect to {}: {}".format(url, e.strerror), 500
        except TimeoutError:
            # TODO enhance the backoff logic. this is not threadsafe and might occur in wrong values for the backoff
            # maybe a queue could be useful here
            time.sleep(self._backoff * 1000)
            self._backoff += 1000
            self.flush(content)
            self._backoff = 1000
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
        time = days + hours + minutes
        print("got schedule?")
        self._scheduler.enter(time, 1, self.flush, argument=(file_path,))
        self._scheduler.enter(time, 2, self.schedule_flush, argument=(file_path,))
        self._scheduler.run()