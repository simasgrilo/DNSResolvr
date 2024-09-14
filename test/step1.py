import unittest
from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader

class TestStep1(unittest.TestCase):

    def setUp(self):
        self.__dns_header = DNSHeader("0102",
                               "0",
                               "0000",
                               "0",
                               "0", "1",
                               "0",
                               "000",
                               "0000",
                               "0001",
                               "0000",
                               "0000",
                               "0000")
        self.__message = DNSMessage("dns.google.com", self.__dns_header)
    def testMessageAssemble(self):
        assert self.__message is not None

    def testMessageHeaderContent(self):
        pass