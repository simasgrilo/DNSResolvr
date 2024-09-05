import unittest
from comp.dns.DNSMessage import DNSMessage

class TestStep1(unittest.TestCase):

    def setup(self):
        self.__msg = DNSMessage("dns.google.com")
    def testMessageAssemble(self):
        assert self.__msg is not None

    def testMessageHeaderContent(self):
        pass