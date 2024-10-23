import unittest
from comp.dns.DNSQuerier import DNSQuerier

class TestStep4(unittest.TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()

    def testValidDNSProcess(self):
        query_result = self.__querier.query_server("www.ic.uff.br")
        self.assertIn('111.115.192.16', query_result[0]["Address"])
        self.assertIn('5.115.97.112', query_result[0]["Address"])
