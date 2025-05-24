"""Test for cache using redis through RedisManager (redis-py)"""
import unittest
import json
import os
from unittest.mock import patch
from pathlib import Path
from comp.cache.RedisManager import RedisManager
from comp.dns.DNSQuerier import DNSQuerier

class TestRedisManager(unittest.TestCase):
    
    def setUp(self):
        # Initialize RedisManager with test configuration
        config_path = os.path.join(Path(__file__).parent, "config.json")
        self.redis_manager = RedisManager(config_path)
        self.redis_manager.connect()
        self._querier = DNSQuerier(self.redis_manager)


    @patch("comp.cache.RedisManager.RedisManager.store")
    @patch("comp.cache.RedisManager.RedisManager.get")
    def test_store_and_get(self, get_mock, store_mock):
        # Test storing and retrieving a value - smoke test to confirm the connection is OK.
        key = 'test_key'
        value = 'test_value'
        
        # Store the value
        self.redis_manager.store(key, value)
        store_mock.return_value = { key: value }
        get_mock.return_value = store_mock.return_value[key]
        print(get_mock.return_value, "get_mock.return_value")
        # Retrieve the value
        retrieved_value = self.redis_manager.get(key)
        print(retrieved_value, "retrieved_value")

        
        # Assert that the retrieved value matches the stored value
        self.assertEqual(value, retrieved_value)
        

    @patch("comp.cache.RedisManager.RedisManager.get")
    def test_query_server_with_cache(self, redis_manager_mock):
        # test the DNS Resolver with a mocked (dict) cache as the RedisManager
        # the objective of this test is to check if the DNS resolver is able to get the data from the cache if available before
        # triggering any DNS query to the Root DNS servers.
        redis_manager_mock.return_value = json.dumps({
	        "Server": "www.google.com",
	        "Address": [
                { 
                    "Type": "A",
                    "Class": "IN",
                    "TTL": 300,
                    "Address": [
                        "142.250.78.228"
                    ],
			    "Expires": "2025-05-24 01:14:18.920387"
		        }
	        ]
        })
        test = self._querier.query_server("www.google.com")
        ip_address = test['Address'][0]['Address'][0]
        self.assertEqual(test['Server'], "www.google.com")
        self.assertEqual("142.250.78.228", ip_address)


    @patch("comp.cache.RedisManager.RedisManager.store")
    @patch("comp.cache.RedisManager.RedisManager.get")
    def test_query_server_without_cache(self, get_mock, store_mock):
        # Test the DNS resolver without a cache
        # the objective of this test is to check whether the insertion of the cache did not affect the DNS query process.
        get_mock.return_value = None
        store_mock.return_value = None
        query_response_address = self._querier.query_server("developer.mozilla.org")['Address']
        addresses = []
        for address in query_response_address:
            addresses += address['Address']
        self.assertIn('34.111.97.67', addresses)
