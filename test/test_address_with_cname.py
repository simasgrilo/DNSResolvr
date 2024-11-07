import unittest
from comp.dns.DNSQuerier import DNSQuerier
from comp.dns.DNSUtils import DNSUtils

class TestAddrCname(unittest.TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()

    def testWhenCnameInForeignDomainThenAddressFound(self):
        query_result = self.__querier.query_server("www.brazzers.com")
        self.assertIn('66.254.114.234', DNSUtils.get_type_a_record(query_result)["Address"])

    def testWhenCnameInBrazilDomainThenAddressFound(self):
        query_result = self.__querier.query_server("www.amazon.com.br")
        self.assertIn('99.84.27.4', DNSUtils.get_type_a_record(query_result)["Address"])