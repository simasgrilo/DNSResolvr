from unittest import TestCase
from comp.dns.DNSQuerier import DNSQuerier

class TestStep4(TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()

    def testWhenNoAddRecordThenQueryThem(self):
        query_result = self.__querier.query_server("developer.mozilla.org")
        self.assertIn('3.109.100.110', query_result[0]["Address"])

    def testNoAddRecordBrazilianDomain(self):
        query_result = self.__querier.query_server("www.amazon.com.br")
        self.assertIn("50.45.102.114", query_result[0]["Address"])