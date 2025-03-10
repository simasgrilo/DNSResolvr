from comp.server.server import DNSServer
import sys
import os

def main():
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "config.json")
    server = DNSServer(config_file).flask_app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()