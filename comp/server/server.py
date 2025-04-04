from flask import Flask, request
from comp.dns.DNSQuerier import DNSQuerier
from comp.exc.BadServerNameException import BadServerNameException
from comp.logging import Logger, LogFlush
from comp.utils.ConfigManager import ConfigManager
import json
import os
import threading
from pathlib import Path

class DNSServer:
    __app = Flask(__name__)
    
    __instance = None
    
    HTTP_400_BAD_REQUEST = 400
    
    def __new__(cls, config_file: str):
        if cls.__instance is None:
            cls.__instance = super(DNSServer, cls).__new__(cls)
        return cls.__instance

    def __init__(self, config_file: str):
        self._log_path = os.path.join(Path(__file__).parent.parent.parent, 'logs', "dns.log")
        config_manager = ConfigManager(config_file)
        config_manager.set("logPath", self._log_path)
        self._config = config_manager.config
        self.__logger = Logger(self._log_path).logger
        self.__logger.info("Starting DNS server with configuration from {}".format(config_file))
        self.__querier = DNSQuerier()
        self.__flusher = LogFlush(self._config, self.__logger)
        
        # Schedule the log task sending in another thread so it will not block the execution of the server.
        self._periodic_thread = threading.Thread(target=self.__flusher.schedule_flush, kwargs={"file_path" : self._log_path})
        self._periodic_thread.start()

    def flask_app(self):
        return self.__app

    @property
    def querier(self):
        return self.__querier
    
    @property
    def logger(self):
        return self.__logger
    
    def get_instance():
        return DNSServer.__instance


    @__app.route("/dns/<address>")
    def get_dns(address: str):
        dns = DNSServer.get_instance()
        try:
            extra_params = {
                "client_ip": request.remote_addr,
            }
            dns.logger.info("Querying DNS server for address {}".format(address), extra=extra_params)
            return json.dumps(dns.querier.query_server(address))
        except BadServerNameException as e:
            dns.logger.error("Provided URL {} is a invalid URL".format(address), extra=extra_params)
            return dns.incorrect_server_name_format(e)

    @__app.errorhandler(400)
    def incorrect_server_name_format(self, error):
        return json.dumps(error.__str__()), DNSServer.HTTP_400_BAD_REQUEST
