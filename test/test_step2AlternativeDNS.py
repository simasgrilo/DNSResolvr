import unittest
from comp.dns.DNSMessage import DNSMessage, DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection

class TestStep2(unittest.TestCase):
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
        self.__msg = DNSMessage("dns.google.com", self.__dns_header)
        self.__connection = DNSConnection("8.8.8.8",53)

    def testMessageWithNoErrors(self):
        "checks whether the RCODE bits are set. the last four bits needs to be zero (could also compare to hex)"
        message = DNSAnswer(self.__connection.sendDNSMessage(self.__msg))
        answer = message.decode_flags("bin").split('0b')
        self.assertEqual(answer[2][4:],  '0000', "Message is not an answer")

    def testMessageAnswered(self):
        """checks whether the QR bit is set to 1. Every response needs to have it set to 1
        we convert it to a binary format to check the exact bit."""
        message = DNSAnswer(self.__connection.sendDNSMessage(self.__msg))
        answer = message.decode_flags("bin").split("0b")
        self.assertEqual(answer[1][0],  '1', "Message is not an answer")
    def testMessageIDequalsAnswerID(self):
        message = DNSAnswer(self.__connection.sendDNSMessage(self.__msg))
        id = self.__msg.get_header().get_id()
        self.assertEqual(message.decode_id(), str(hex(id[0])) + str(hex(id[1])), "IDs does not match. Please check your input")
