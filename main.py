from comp.dns.DNSQuerier import DNSQuerier

def main():
    #below DNSHeader should be built elsewhere?
    querier = DNSQuerier()
    # print(querier.query_server("www.google.com"))
    # print(querier.query_server("www.ic.uff.br"))
    print(querier.query_server("www.amazon.com.br"))


if __name__ == "__main__":
    main()