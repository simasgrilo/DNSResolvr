import json
from json import JSONDecodeError
class ConfigManager:
    """
    Class to configure reading of the configuration file, providing a single access point of the configuration thoughout the application
    """
    _instance = None
    
    def __new__(self, config_file: str):
        """
        Singleton implementation for the ConfigManager class
        """
        if self._instance is None:
            self._instance = super(ConfigManager, self).__new__(self)
        return self._instance
    
    def __init__(self, config_file: str):
        """
        Initializes a dict object from the json file with the configuration
        Args:
            config_file (str): path to the configuration file
        """
        config = None
        try:
            with open(config_file, "rt") as fp:
                content = fp.readlines()
                config = "".join(content)
            self._config = json.loads(config)
        except JSONDecodeError as e:
            raise ValueError("Invalid configuration file")
        
    @property
    def config(self):
        return self._config
    
    def set(self, key: str, value: object):
        self._config[key] = value