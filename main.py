import random

from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection

def main():
    #below DNSHeader should be built elsewhere. this needs to be a json
    dns_header = DNSHeader("0102",
                           "0",
                           "0000",
                           "0",
                           "0","0",
                           "0",
                           "000",
                           "0000",
                           "0001",
                           "0000",
                           "0000",
                           "0000")
    message = DNSMessage("dns.google.com", dns_header)
    connection = DNSConnection("198.41.0.4",53)
    response = DNSAnswer(connection.sendDNSMessage(message))
    if response:
        print(response.decode_answer())

if __name__ == "__main__":
    main()