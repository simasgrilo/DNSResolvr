from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection

class DNSQuerier():

    TLD_HOSTS = ["198.41.0.4"]
    IPV4 = 'A'
    IPV6 = 'AAAA'
    def __query(self, hostname: str, dns_server: str):
        #for tld_ip in self.TLD_HOSTS:
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
        print("Querying {dns_server} to discover {hostname}'s address".format(dns_server=dns_server,hostname=hostname))
        message = DNSMessage(hostname, dns_header)
        connection = DNSConnection(dns_server, 53)
        response = DNSAnswer(connection.sendDNSMessage(message))
        if not response:
            return
        query_servers, query_additional_data = response.decode_answer()
        if query_additional_data == 0:
            #this is the case that there's no more additional data. the program emits a signal that answers were found
            return query_servers
        for return_record in query_servers:
            server = return_record["Name Server"]
            #TODO: enable IPV6 support
            server_ips = query_additional_data.get((server, self.IPV4))['Address']
            if server_ips:
                #scenario where the IP of the server in the answer section was received in the additional RR part.
                for ip in server_ips:
                    server = self.__query(hostname, ip)
                    if server:
                        return server
            else:
                #search for the IP of the current server we're querying.
                pass
        return None


    def query_server(self, hostname: str):
        for tld in self.TLD_HOSTS:
            answer = self.__query(hostname,tld)
            if answer:
                return answer

