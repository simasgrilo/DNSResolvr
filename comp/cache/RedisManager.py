""" Module that implements the caching strategy using Redis (through redis-py: https://redis.io/docs/latest/develop/clients/redis-py/)"""
import redis
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
        
    def store(self, key, value):
        """
        store the value in the remote cache
        Args:
            value (any): value to be stored
        """
        self.redis.set(key, value)
        
    def get(self, key: any):
        """
        get the value from the remote cache
        Args:
            key (any): key to be retrieved - preferably a string key.s
        """
        return self.redis.get(key)