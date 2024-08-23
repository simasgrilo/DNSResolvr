import unittest
from comp.dns.DNSMessage import DNSMessage

class test(unittest.TestCase):

    def testMessageAssemble(self):
        msg = DNSMessage("www.google.com")
        assert msg is not None

    def testMessageHeaderContent(self):
        pass
