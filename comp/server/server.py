from flask import Flask, request
from comp.dns.DNSQuerier import DNSQuerier
from comp.exc.BadServerNameException import BadServerNameException
from comp.logging.Logger import Logger
import os
import json

class DNSServer:
    __app = Flask(__name__)
    
    __logger = Logger(os.path.abspath(__file__) + "dns.log").logger

    HTTP_400_BAD_REQUEST = 400

    def __init__(self):
        self.__querier = DNSQuerier()

    @property
    def app(self):
        return self.__app

    @property
    def querier(self):
        return self.__querier
    
    @property
    def logger(self):
        return self.__logger


dns = DNSServer()
app = dns.app

@app.route("/dns/<address>")
def get_dns(address: str):
    try:
        extra_params = {
            "client_ip": request.remote_addr,
        }
        dns.logger.info("Querying DNS server for address {}".format(address), extra=extra_params)
        return json.dumps(dns.querier.query_server(address))
    except BadServerNameException as e:
        dns.logger.error("Provided URL {} is a invalid URL".format(address), extra=extra_params)
        return incorrect_server_name_format(e)

@app.errorhandler(400)
def incorrect_server_name_format(error):
    return json.dumps(error.__str__()), dns.HTTP_400_BAD_REQUEST
