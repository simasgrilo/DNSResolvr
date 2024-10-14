from comp.dns.DNSQuerier import DNSQuerier

def main():
    #below DNSHeader should be built elsewhere. this needs to be a json
    querier = DNSQuerier()
    querier.query("dns.google.com")


if __name__ == "__main__":
    main()