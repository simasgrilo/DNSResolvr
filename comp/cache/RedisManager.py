""" Module that implements the caching strategy using Redis (through redis-py: https://redis.io/docs/latest/develop/clients/redis-py/)"""
import redis
import json
from comp.cache.CacheManager import CacheManager

class RedisManager(CacheManager):
    
    def __init__(self, config):
        super().__init__(config)
        self.host = self.config['redis']['host']
        self.port = self.config['redis']['port']
        self.decode_response = self.config['redis']['decode_responses']
        self.connect()
        
    def connect(self):
        """Overrides the connect method from the base abstract class CacheManager to connect to Redis"""
        self.redis = redis.Redis(host=self.host, port=self.port, decode_responses=self.decode_response)
        
    def store(self, key, value, data_type="str"):
        """
        store the value in the remote cache, based on the data type.
        Considers the standard type of the data value as an string
        Args:
            value (any): value to be stored
        """
        if data_type == "json":
            value = json.dumps(value)
        elif data_type == "str":
            value = str(value)
        elif data_type == "int":
            value = int(value)
        elif data_type == "float":
            value = float(value)
        else:
            raise ValueError(f"Unsupported data type: {data_type}") 
        self.redis.set(key, value)
        
    def get(self, key: any):
        """
        get the value from the remote cache
        Args:
            key (any): key to be retrieved - preferably a string key.s
        """
        return self.redis.get(key)