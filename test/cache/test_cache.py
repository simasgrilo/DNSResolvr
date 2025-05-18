"""Test for cache using redis through RedisManager (redis-py)"""
import unittest
import os
from pathlib import Path
from comp.cache.RedisManager import RedisManager
from comp.dns.DNSQuerier import DNSQuerier
from comp.dns.DNSUtils import DNSUtils

class TestRedisManager(unittest.TestCase):
    
    def setUp(self):
        # Initialize RedisManager with test configuration
        config_path = os.path.join(Path(__file__).parent, "config.json")
        self.redis_manager = RedisManager(config_path)
        self.redis_manager.connect()
        self._querier = DNSQuerier()


    def test_store_and_get(self):
        # Test storing and retrieving a value - smoke test to confirm the connection is OK.
        key = 'test_key'
        value = 'test_value'
        
        # Store the value
        self.redis_manager.store(key, value)
        
        # Retrieve the value
        retrieved_value = self.redis_manager.get(key)
        
        # Assert that the retrieved value matches the stored value
        self.assertEqual(value, retrieved_value)
        
    def test_store_a_valid_value(self):
        query_result = self._querier.query_server("developer.mozilla.org")
        print(query_result)
        self.assertIn('34.111.97.67', DNSUtils.get_type_a_record(query_result)["Address"])


    # def tearDown(self):
    #     # Clean up the Redis connection
    #     self.redis_manager.close()