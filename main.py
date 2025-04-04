from comp.server.server import DNSServer
import os

config_file = os.path.join(os.path.dirname(__file__), "config.json")
app = DNSServer(config_file).flask_app()#.run(host="0.0.0.0",port=3001)


