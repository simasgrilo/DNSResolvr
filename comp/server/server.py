from flask import Flask
from comp.dns.DNSQuerier import DNSQuerier
import json

class DNSServer:
    __app = Flask(__name__)

    def __init__(self):
        self.__querier = DNSQuerier()
        # print(querier.query_server("www.google.com"))
        # print(querier.query_server("www.ic.uff.br"))
        #print(self.__querier.query_server("www.amazon.com.br"))

    def get_app(self):
        return self.__app

    def get_querier(self):
        return self.__querier

dns = DNSServer()
app = dns.get_app()

@app.route("/dns/<address>")
def get_dns(address: str):
    try:
        return json.dumps(dns.get_querier().query_server(address))
    except Exception:
        import traceback
        traceback.print_exc()
