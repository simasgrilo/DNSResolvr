from comp.dns.DNSHeader import DNSHeader
# from DNSAnswer import DNSAuthority
# from DNSAnswer import DNSAnswer
from comp.dns.DNSQuestion import DNSQuestion
# from DNSAddSection import DNSAddSection

class DNSMessage():
    """Class to provide a DNS Message, based on other components defined in the same package """

    def __init__(self, hostname: str):
        self.__header = DNSHeader()
        self.__question = DNSQuestion(hostname)

    def format(self):
        return self.__header.get_id() + self.__header.get_sec_header_field() + self.__header.get_qdcount() + self.__header.get_ancount() + self.__header.get_nscount() + self.__header.get_arcount()
