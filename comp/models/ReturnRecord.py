""" Convenience class to model the return record of the DNS query in a structured way."""
from typing import List, Dict


class ReturnRecord:
    """ Convenience class to model the return record of the DNS query in a structured way.
    """
    def __init__(self, server_name: str, server_address: List[str]):
        self._server_name = server_name
        self._server_address = server_address

    @classmethod
    def from_raw(cls, server_name: str, server: Dict):
        """ Factory method to create a ReturnRecord instance from a raw server dictionary.
        
        Args:
            server_name (str): The name of the server.
            server (Dict): The raw server dictionary.
        
        Returns:
            ReturnRecord: An instance of ReturnRecord.
        """
        server_address = []
        for server_entry in server:
            server_address.append({
                "Type": server_entry["Type"] if "Type" in server_entry else None,
                "Class": server_entry["Class"] if "Class" in server_entry else None,
                "TTL": server_entry["TTL"] if "TTL" in server_entry else None,
                "Address": server_entry["Address"] if "Address" in server_entry else None 
            })
        return cls(server_name, server_address)

    @property
    def server_name(self):
        return self._server_name
    
    @property
    def server_address(self):
        return self._server_address
    
    @server_name.setter
    def server_name(self, value):
        self._server_name = value
        
    @server_address.setter
    def server_address(self, value):
        self._server_address = value
    
    def to_json(self):
        """ Convert the ReturnRecord instance to a JSON-serializable dictionary.
        
        Returns:
            Dict: A dictionary representation of the ReturnRecord instance, with the server name as the key.
        """
        return {
            "Server": self._server_name,
            "Address": self._server_address
        }