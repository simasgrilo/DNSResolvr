from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection

class DNSQuerier():

    TLD_HOSTS = ["198.41.0.4"]
    __query = None
    def query(self, hostname: str):
        for tld_ip in self.TLD_HOSTS:
            dns_header = DNSHeader("0102",
                                   "0",
                                   "0000",
                                   "0",
                                   "0", "0",
                                   "0",
                                   "000",
                                   "0000",
                                   "0001",
                                   "0000",
                                   "0000",
                                   "0000")
            message = DNSMessage(hostname, dns_header)
            connection = DNSConnection(tld_ip, 53)
            response = DNSAnswer(connection.sendDNSMessage(message))
            if response:
                query_servers = response.decode_answer()
                print(query_servers)