import unittest
from comp.dns.DNSQuerier import DNSQuerier

class TestStep4(unittest.TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()

    def testValidDNSProcess(self):
        query_result = self.__querier.query_server("www.google.com")
        self.assertIn('142.251.133.164',query_result[0]["Address"])
