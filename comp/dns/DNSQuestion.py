

class DNSQuestion:

    def __init__(self, name: str):
        # encoding of the name being queried in a bytes object with the corresponding encoding
        # could be the same as b'www.google.com', for example.
        self.__qname = bytes(name, encoding='UTF-8')
        self.__qtype = b'\x01'
        self.__qclass = b'\x01'
