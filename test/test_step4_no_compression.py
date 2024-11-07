import unittest
from comp.dns.DNSQuerier import DNSQuerier

class TestStep4(unittest.TestCase):

    def setUp(self):
        self.__querier = DNSQuerier()