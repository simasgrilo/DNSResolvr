import socket
from comp.dns.DNSMessage import DNSMessage

class DNSConnection:
    """Defines an UDP connection to message the DNS server asking for the IP of the message"""
    def __init__(self, ip:str, port: int):
        self.__ip = ip
        self.__port = port
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendDNSMessage(self, message: DNSMessage):
        """Connects to the DNS server specified in tis connection and send the message
            @:message: parameter containining the DNS message to be sent to the server
            @:return the message received from the server specified in (self.__ip, self.__port)
        """
        try:
            #SOCK_DGRAM for UDP connection, SOCK_STREAM for TCP connection
            dns_msg = message.format_header() + message.format_question()
            self.__conn.sendto(dns_msg, (self.__ip, self.__port))
            message = self.__conn.recvfrom(4096) #buffer of 4096
        except TimeoutError:
            pass
        except ConnectionError:
            pass
        except OSError:
            pass
        finally:
            self.__conn.close()

        return message[0] if message else None

