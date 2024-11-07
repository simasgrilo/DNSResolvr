from comp.server.server import DNSServer


def main():
    server = DNSServer().get_app().run()

if __name__ == "__main__":
    main()