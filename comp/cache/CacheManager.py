"""This class defines the Cache strategy of the DNS Reslolvr app, which can be extended to other caching strategies."""
from abc import ABC, abstractmethod
import json

class CacheManager(ABC):
   
   
    def __init__(self, config):
        with open(config, 'r') as fp:
            self.config = json.load(fp)
        
    @abstractmethod
    def connect(self):
        """Connect to the cache."""
    