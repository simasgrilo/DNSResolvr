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

    def format_header(self):
        return self.__header.get_id() + self.__header.get_sec_header_field() + self.__header.get_qdcount() + self.__header.get_ancount() + self.__header.get_nscount() + self.__header.get_arcount()

    def format_question(self):
        return self.__question.get_question_name() + self.__question.get_question_type() + self.__question.get_question_class()

    def get_question(self):
        return self.__question

    def get_header(self):
        return self.__header

    def decode_message(self, message: hex):
        pass
