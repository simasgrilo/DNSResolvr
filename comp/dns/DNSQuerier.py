from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection
from comp.dns.DNSUtils import DNSUtils

class DNSQuerier:

    TLD_HOSTS = ["198.41.0.4"]
    IPV4 = 'A'
    IPV6 = 'AAAA'
    CNAME = 'CNAME'
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
        print("Querying {dns_server} to discover {hostname}'s address".format(dns_server=dns_server, hostname=hostname))
        message = DNSMessage(hostname, dns_header)
        connection = DNSConnection(dns_server, 53)
        response = DNSAnswer(connection.sendDNSMessage(message))
        if not response:
            return
        query_servers, query_additional_data = response.decode_answer()
        if query_additional_data == 0:
            #this is the case that there's no more additional data. the program emits a signal that answers were found
            return query_servers
        # Begin fix #3
        # if there's a CNAME record and no A record with type IN, we need to restart the query from the CNAME name
        for return_record in query_servers:
            server = return_record["Name Server"]
            if not query_additional_data:
                # begin fix #2
                # the server did not have an IP address in the additional section.
                server_ips = self.query_server(server)[0]
                if not server_ips:
                    return None
                # end fix #2
            #TODO: enable IPV6 support
            else:
                server_ips = query_additional_data.get((server, self.IPV4))
            #search for the IP of the current server we're querying.
            if server_ips:
                server_ips = server_ips['Address']
                #scenario where the IP of the server in the answer section was received in the additional RR part.
                for ip in server_ips:
                    server = self.__query(hostname, ip)
                    if server:
                        return server
        return None


    def query_server(self, hostname: str):
        """ returns the answer (if exists) from a complete DNS query, starting from a root server"""
        answer = []
        for tld in self.TLD_HOSTS:
            answer += self.__query(hostname,tld)
            # begin fix #3 - CNAME process EGRILO
            if DNSUtils.check_if_valid_a_rrr(answer):
                return answer
            answer += self.query_server(DNSUtils.get_cname_record(answer))
            # end fix #3
        return answer

