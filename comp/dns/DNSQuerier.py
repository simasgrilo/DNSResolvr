import json
from datetime import datetime, timedelta
from redis.exceptions import ConnectionError
from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSHeader import DNSHeader
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection
from comp.dns.DNSUtils import DNSUtils
from comp.models.ReturnRecord import ReturnRecord

class DNSQuerier:

    #TODO clear this part of the code. TLD_HOSTS should be in a config file and IPV4, IPV6, CNAME should be in a DNSUtils (or constants) class.
    TLD_HOSTS = ["198.41.0.4"]
    IPV4 = 'A'
    IPV6 = 'AAAA'
    CNAME = 'CNAME'

    def __init__(self, cache_manager = None, logger = None):
        self._cache_manager = cache_manager
        self._logger = logger
    
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
        print(f'Querying {dns_server} to discover {hostname}\'s address')
        message = DNSMessage(hostname, dns_header)
        connection = DNSConnection(dns_server, 53)
        response = DNSAnswer(connection.sendDNSMessage(message))
        if not response:
            return None
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
                server_ips = self.run_query_server(server)[0]
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
        """ Wrapper method to encapsulate the query server method with a cache layer.

        Args:
            hostname (str): Name of the server which IP address is being queried.
        """
        # check for the cache first
        try:
            cached_answer = self.check_cache_for_ip(hostname)
            if cached_answer:
                print(f'Found {hostname} in cache')
                return cached_answer
        except ConnectionError:
            self._logger.error("Cache connection error when storing. Proceeding with DNS query.", extra={"client_ip": ""})
        answer = self.run_query_server(hostname)
        if answer:
            # store the answer in the cache - consider only the relevant entries
            valid_a_records = list(filter(lambda server_entry: server_entry['Type'] == self.IPV4, answer))
            dns_answer = ReturnRecord.from_raw(hostname, valid_a_records).to_json()
            self._store(dns_answer)
            return dns_answer
        return None
        
    def run_query_server(self, hostname: str):
        """ returns the answer (if exists) from a complete DNS query, starting from a root server"""
        answer = []
        for tld in self.TLD_HOSTS:
            answer += self.__query(hostname,tld)
            # begin fix #3 - CNAME process EGRILO
            if DNSUtils.check_if_valid_a_rrr(answer):
                return answer
            answer += self.run_query_server(DNSUtils.get_cname_record(answer))
            # end fix #3
        return answer


    def check_cache_for_ip(self, server_name: str):
        """Checks if the server name is already in the cache. If it is, no further processing is requred.
        Args:
            server_name (str): human-readable server name (e.g., developer.mozilla.org)
        """
        if not self._cache_manager:
            return None
        answer = self._cache_manager.get(server_name)
        if not answer:
            return None
        return json.loads(answer)
        
    def _store(self, dns_answer: dict):
        """
        Store the server entry in the cache. The server entry is a dictionary with the following keys:
        - Type: record type (A, CNAME)
        - Class: record class (IN)
        - TTL: time to live (in seconds)
        - Data Length: Lengfth of the data field in bytes. varies according to the record type.
        - Address: the IP address of the server (if the record type is A)
        Args:
            server_name (str): human readable server name (e.g., developer.mozilla.org)
            server_entry (dict): return record from the DNS querier.
        """
        self._calculate_ttl(dns_answer)
        server_name = dns_answer["Server"]
        try:
            self._cache_manager.store(server_name, dns_answer, "json")
        except ConnectionError:
            self._logger.error("Cache connection error when storing. Proceeding with DNS query.", extra={"client_ip": ""})
            
    def _calculate_ttl(self, dns_answer: dict): 
        addresses = dns_answer["Address"]
        for entry in addresses:
            if "TTL" in entry:
                expires_in = str(datetime.now() + timedelta(seconds=entry["TTL"]))
                entry["Expires"] = expires_in
    
    def get_cache_manager(self):
        """ Returns the cache manager object. """
        return self._cache_manager
