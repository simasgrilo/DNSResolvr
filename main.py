from comp.dns.DNSMessage import DNSMessage
from comp.dns.DNSAnswer import DNSAnswer
from comp.net.connection import DNSConnection

def main():
    message = DNSMessage("dns.google.com")
    connection = DNSConnection("8.8.8.8",53)
    response = DNSAnswer(connection.sendDNSMessage(message))
    if response:
        print(response.decode_answer())

if __name__ == "__main__":
    main()