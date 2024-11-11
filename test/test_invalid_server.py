from unittest import TestCase
from comp.dns.DNSQuerier import DNSQuerier
from comp.dns.DNSUtils import DNSUtils

class TestInvalidServer(TestCase):

    #begin fix #4 - EGRILO
    def setUp(self):
        self.__querier = DNSQuerier()

    def testWhenNoAddRecordThenQueryThem(self):
        self.assertRaises(ValueError, lambda: self.__querier.query_server("invalidServer"))
    #end fix #4 - EGRILO
