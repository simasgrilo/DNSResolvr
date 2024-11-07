from unittest import TestCase
from comp.dns.DNSQuerier import DNSQuerier
from comp.dns.DNSUtils import DNSUtils

class TestStep4(TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()

    def testWhenNoAddRecordThenQueryThem(self):
        query_result = self.__querier.query_server("developer.mozilla.org")
        self.assertIn('34.111.97.67', DNSUtils.get_type_a_record(query_result)["Address"])


    def testNoAddRecordBrazilianDomain(self):
        query_result = self.__querier.query_server("www.ic.uff.br")
        self.assertIn("35.199.94.97", DNSUtils.get_type_a_record(query_result)["Address"])
