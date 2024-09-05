import random
import struct

class DNSHeader:

    def __init__(self):
        """models the DNS header section as specified in RFC 1035, Section 4.1.1. Uses position of an array per byte before encoding
        TODO pretty sure there's a better way to address it. Let´s check it out."""
        self.__id = b'\x01\x02'#random.randbytes(2)
        self.__second_header_field = b'\x01\x00'
        #group each field as per the RFC 1035, so instead setting bit by bit, set the two byter for each field.
        #in python, a bytestring can have values set up as hex values, like b'\x09\x00\x09\ denotes this bit string: 000010010000000000001001
        # self.__qr = [0]
        # self.__opcode = [0] * 4
        # self.__authoritative_answer = [0]
        # self.__tc = [0]
        # self.__rd = [1] #set to 1 to ask for a DNS resolver first.
        # self.__ra = [0]
        # self.__z = [0] * 4
        # self.__rcode = [0] * 4
        self.__qdcount = b'\x00\x01'
        self.__ancount = b'\x00\x00'
        self.__nscount = b'\x00\x00'
        self.__arcount = b'\x00\x00'

    def get_id(self):
        return self.__id

    def get_sec_header_field(self):
        return self.__second_header_field

    def get_qdcount(self):
        return self.__qdcount

    def get_ancount(self):
        return self.__ancount

    def get_nscount(self):
        return self.__nscount

    def get_arcount(self):
        return self.__arcount






