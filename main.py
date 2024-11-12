from comp.server.server import DNSServer


def main():
    server = DNSServer().get_app().run(host="0.0.0.0")

if __name__ == "__main__":
    main()