import random
import struct

class DNSHeader:

    def __init__(self, id : str, qr, opcode, auth_answer, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount):
        """models the DNS header section as specified in RFC 1035, Section 4.1.1. Uses position of an array per byte before encoding
        each parameter is denoted as a hex string (so each char is actually a 4-bit representation of a hex value

        TODO pretty sure there's a better way to address it. Let´s check it out."""

        self.__id = bytes.fromhex(id)  #b'\x01\x02'#random.randbytes(2)
        #see RFC 1035, Section 3.1 for more details
        first_byte = str(int(qr + opcode + auth_answer + tc + rd,2))
        if len(first_byte) % 2:
            #turn it into a byte for hex formatting (each pos in the str is a 4-bit representation)
            first_byte = '0' + first_byte
        second_byte = str(int(ra + z + rcode))
        if len(second_byte) % 2:
            second_byte = '0' + second_byte
        self.__second_header_field = bytes.fromhex(first_byte) + bytes.fromhex(second_byte) #b'\x01\x00'
        self.__qdcount = bytes.fromhex(qdcount) #b'\x00\x01'
        self.__ancount = bytes.fromhex(ancount) #b'\x00\x00'
        self.__nscount = bytes.fromhex(nscount) #b'\x00\x00'
        self.__arcount = bytes.fromhex(arcount) #b'\x00\x00'

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






