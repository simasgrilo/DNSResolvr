from comp.dns.DNSMessage import DNSMessage
from comp.net.connection import DNSConnection

def main():
    message = DNSMessage("www.google.com")
    connection = DNSConnection("8.8.8.8",53)
    response = connection.sendDNSMessage(message)
    print(response)

if __name__ == "__main__":
    main()