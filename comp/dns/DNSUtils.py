from typing import List


class DNSUtils:
    """class with utilities to parse and process different DNS type records"""

    IPv4 = 'A'
    IPv6 = 'AAAA'
    CNAME = 'CNAME'

    @staticmethod
    def check_if_cname_has_a_rr(self ):
        pass

    @staticmethod
    def check_if_valid_a_rrr(answer: List[dict]) -> bool:
        return any(rr["Type"] == DNSUtils.IPv4 and rr["Address"] for rr in answer)

    @staticmethod
    def get_cname_record(answer: List[dict]):
        return next((rr['CNAME'] for rr in answer if rr['CNAME']), None)

    @staticmethod
    def get_type_a_record(answer: List[dict]):
        return next((rr for rr in answer if rr['Address'] and rr['Type'] == DNSUtils.IPv4), None)
