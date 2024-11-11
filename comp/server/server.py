from flask import Flask
from comp.dns.DNSQuerier import DNSQuerier
from comp.exc.BadServerNameException import BadServerNameException
import json

class DNSServer:
    __app = Flask(__name__)

    HTTP_400_BAD_REQUEST = 400

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
    except BadServerNameException as e:
        return incorrect_server_name_format(e)

@app.errorhandler(400)
def incorrect_server_name_format(error):
    return json.dumps(error.__str__()), dns.HTTP_400_BAD_REQUEST
