from flask import Flask, request
from comp.dns.DNSQuerier import DNSQuerier
from comp.exc.BadServerNameException import BadServerNameException
from comp.logging import Logger, LogFlush
from comp.utils.ConfigManager import ConfigManager
import json
import os


class DNSServer:
    __app = Flask(__name__)
    
    HTTP_400_BAD_REQUEST = 400

    def __init__(self, config_file: str):
        config_manager = ConfigManager(config_file)
        self._config = config_manager.config
        self._log_path = os.path.join(os.path.dirname(__file__), "dns.log")
        config_manager.set("logPath", self._log_path)
        self.__logger = Logger(self._log_path).logger
        self.__logger.info("Starting DNS server with configuration from {}".format(config_file))
        self.__querier = DNSQuerier()
        self.__flusher = LogFlush(self._config)
        self.__flusher.schedule_flush(self._log_path)

    @property
    def flask_app(self):
        return self.__app

    @property
    def querier(self):
        return self.__querier
    
    @property
    def logger(self):
        return self.__logger


    @__app.route("/dns/<address>")
    def get_dns(self, address: str):
        try:
            extra_params = {
                "client_ip": request.remote_addr,
            }
            self.logger.info("Querying DNS server for address {}".format(address), extra=extra_params)
            return json.dumps(self.querier.query_server(address))
        except BadServerNameException as e:
            self.logger.error("Provided URL {} is a invalid URL".format(address), extra=extra_params)
            return self.incorrect_server_name_format(e)

    @__app.errorhandler(400)
    def incorrect_server_name_format(error):
        return json.dumps(error.__str__()), DNSServer.HTTP_400_BAD_REQUEST
