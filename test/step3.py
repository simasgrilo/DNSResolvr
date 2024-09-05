import unittest
from comp.dns.DNSAnswer import DNSAnswer
from comp.dns.DNSMessage import DNSMessage
from comp.net.connection import DNSConnection
class TestStep3(unittest.TestCase):


    def setUp(self):
        self.__message = DNSMessage("dns.google.com")
        self.__connection = DNSConnection("8.8.8.8", 53)

    def testMessageSuccessfullyReceived(self):
        """asserts that a successful DNS query to a valid DNS server will return at least one valid resource"""
        message = DNSAnswer(self.__connection.sendDNSMessage(self.__message)).decode_answer()
        self.assertIsNotNone(message[0])

    def testParseMessage(self):
        message = DNSAnswer(self.__connection.sendDNSMessage(self.__message)).decode_answer()
        ip_addr = message[0]['Address']
        self.assertEqual(ip_addr[0], '8.8.8.8')