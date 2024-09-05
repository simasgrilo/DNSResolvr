import sys

class DNSQuestion:

    def __init__(self, name: str):
        # encoding of the name being queried in a bytes object with the corresponding encoding
        # could be the same as b'www.google.com', for example.
        self.__qname = self.__encode_cnt(name)
        self.__qtype = b'\x00\x01'
        self.__qclass = b'\x00\x01'

    def get_question_name(self):
        return self.__qname

    def get_question_type(self):
        return self.__qtype

    def get_question_class(self):
        return self.__qclass

    def __encode_cnt(self, name: str):
        enc = bytes()
        for adr in name.split("."):
            #each length is represented as an octet preceding the encoding of the bytestring denoting parts of the address to
            #be queried.
            enc += len(adr).to_bytes(1, byteorder= 'big') + bytes(adr, encoding='UTF-8')
        return enc + b'\x00'

    def get_size(self):
        return sys.getsizeof(self)

