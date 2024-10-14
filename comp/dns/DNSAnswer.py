import sys
from typing import List, Dict

class DNSAnswer:

    def __init__(self, response: bytes):
        self.__COMPRESSED_NAME = 192
        self.__IPv4 = 'A'
        self.__IPv6 = 'AAAA'
        self.__response = response
        self.__byteString = bytes.hex(response)

    def get_message(self):
        return self.__response

    def get_bytestring(self):
        return self.__byteString

    def decode_id(self, mode:str=None):
        """decodes the id from the DNS response,
        @:parameter mode: bin to decode it as a binary string, None defaults to hex
        @:return a string containnig the response"""
        if mode == "bin":
            return str(bin(self.__response[0])) + str(bin(self.__response[1]))
        return str(hex(self.__response[0])) + str(hex(self.__response[1]))

    def decode_flags(self, mode:str=None):
        if mode == 'bin':
            return str(bin(self.__response[2])) + str(bin(self.__response[3]))
        return self.__response[2] + self.__response[3]

    def decode_answer(self):
        """decodes the answer of the DNS request.
            if the answer header contains entries in field ANCOUNT, means that the payload contains Return Records
            (RR's) with the address of the server we have requested
            otherwise, it did ping some top-level domain server to get this information. Then we need to iterate over
            the list of TLD servers and restart the query to search for it.
            @param: none
            @:return: parsed_answers - a list of records containing the structuring of the

        """
        #ANSWER_SIZE = 12 #12 bytes per answer
        answers = self.__response[6] + self.__response[7]
        questions = self.__response[4] + self.__response[5]
        authority_rr = self.__response[8] + self.__response[9]
        additional_rr = self.__response[10] + self.__response[11]
        parsed_answers = []
        #no questions, no responses
        if not questions:
            return None
        if answers:
            return self.__decode_answer(questions)
        else:
            if authority_rr:
                offset, parsed_answers = self.__decode_authoritative(questions,authority_rr, additional_rr) #will use both the authority and additional records section
                parsed_additional_rr = self.__decode_additional_rr(offset, additional_rr)
        return parsed_answers

    def __parse_questions(self, offset: int, questions_offset: int, response: bytes) -> int:
        for query in range(questions_offset):
            while response[offset]:
                offset += response[offset] + 1 #we need to parse 1 + offset bytes until reaching the EOR \x00.
            #skip the last byte and both type and class entries - each one has a fixed length of two bytes
            offset += 5
        return offset

    def __decode_answer(self, questions_offset: int) -> List[Dict]:
        #move the pointer from byte 6 to the answers offset - which moves from the questions to the answers
        #you also need the amount of questions to know the offset - 11 bytes is the count from the ID to the queries.
        #each query contains 3 sections of two bytes each - 6 bytes per question
        #the encoded name has a byte
        COMPRESSED_NAME = 192
        offset = 12
        response = self.__response
        #ignore the query section:
        offset = self.__parse_questions(offset, questions_offset, response)
        parsed_answers = []
        for answer in range(0, questions_offset):
            #TODO: refactor the parsing process into different methods
            parsed_answer = {}
            name = []
            while response[offset] != b'\x00':
                if response[offset] == COMPRESSED_NAME:
                    #read from the next pointer and return: by the RFC, pointers are only found at the end of a name.
                    name.append(self.__decode_name(response, response[offset + 1]))
                    break
                else:
                    #regular addresses: no pointers to process:
                    name.append(bytes.decode(bytes.fromhex((str(response[offset]))))) #bytes.decode(bytes.fromhex('64'))
                offset += 1
            #from here onwards: each domain has the same length
            parsed_answer["Name"] = ".".join(name)
            offset += 2
            rr_type = self.__get_rr_definition(int(response[offset: offset + 2].hex(), 16))
            parsed_answer["Type"] = rr_type
            #end of the Type part of the answer record
            offset += 2

            #parse the Class type:
            class_type = self.__get_class_type(int(response[offset: offset + 2].hex(), 16))
            parsed_answer["Class"] = class_type
            offset += 2
            #position at the TTL record. Note that ttl has a length of four bytes.
            parsed_answer["TTL"] = int(response[offset: offset + 4].hex(), 16)
            offset += 4

            rdata_length = int(response[offset: offset + 2].hex(), 16)
            parsed_answer["Data Length"] = rdata_length
            offset += 2
            # full_addr = []
            # curr_addr = []
            # index = 0
            # for byte in range(offset, offset + rdata_length):
            #     curr_addr.append(str(int(response[offset: offset + 1].hex(),16)))
            #     index += 1
            #     if not index % 4:
            #         full_addr.append(".".join(curr_addr))
            #         curr_addr.clear()
            #         index = 0
            parsed_answer['Address'] = self.__parse_ipv4_addr(response, offset, rdata_length)
            parsed_answers.append(parsed_answer)
            #position the offset at the next pos, which is the length of the read data:
            offset += rdata_length
        return parsed_answers

    def __parse_ipv4_addr(self, response: bytes, offset: int, rdata_length: int):
        """Parses IPv4 addresses as in the answer format (you can have more than one IPv4 address
           Can be reused also in retrieving the IP for TLD or authoritative servers as in auth_rr records.
           @:param response: the bytestream response of the DNS request
           @:param offset: the byte position as an integer in the message to start the processing
           @:param rdata_length: resource data length for the attribute being processed.
           @:return full_addr: a String linst containing all IPv4 addresses returned
        """
        full_addr = []
        curr_addr = []
        index = 0
        for byte in range(offset, offset + rdata_length):
            curr_addr.append(str(int(response[byte: byte + 1].hex(), 16)))
            index += 1
            if not index % 4:
                full_addr.append(".".join(curr_addr))
                curr_addr.clear()
                index = 0
        return full_addr

    def __decode_authoritative(self, questions_offset: int, authority_rr: int, additional_rr: int):
        """interprets the authoritative server and queries it again with a new DNS message iteratively for each Authoritative
           name server
           @:param questions_offset - the offset position of the original message to be parsed.
           @:returns (offset, parsed_answers) - A tuple containing the position of the byte stream where the
                     processing of the authoritative nameservers has ended and the additional recors is to start,
                     and all data extracted from the DNS answer regarding the authoritative nameservers
        """
        offset = 12 #ignores the first 12 bytes of the header.
        COMPRESSED_NAME = 192
        parsed_answers = []
        response = self.__response
        #ignore the query section:
        offset = self.__parse_questions(offset, questions_offset, response)
        for record in range(0, authority_rr):
            parsed_answer = {}
            #each authority record contains 32 bytes. We need to process them following the specs in Section 3.2.2.
            #parse name
            name = []
            while response[offset] != b'\x00':
                if response[offset] == COMPRESSED_NAME:
                    # name references to a pointer:
                    # read from the next pointer and return: by the RFC, pointers are only found at the end of a name.
                    name.append(self.__decode_name(response, response[offset + 1]))
                    print(name)
                    break
                else:
                    #regular addresses: no pointers to process:
                    name.append(bytes.decode(bytes.fromhex((str(response[offset]))))) #bytes.decode(bytes.fromhex('64'))
                offset += 1
            parsed_answer["Name"] = "".join(name)
            #skip the name record
            offset += 2
            #parse type
            parsed_answer["Type"] = self.__get_rr_definition(int(response[offset: offset + 2].hex(), 16))
            # end of the Type part of the answer record
            offset += 2
            # parse the Class type:
            class_type = self.__get_class_type(int(response[offset: offset + 2].hex(), 16))
            parsed_answer["Class"] = class_type
            offset += 2
            # position at the TTL record. Note that ttl has a length of four bytes.
            parsed_answer["TTL"] = int(response[offset: offset + 4].hex(), 16)
            offset += 4

            rdata_length = int(response[offset: offset + 2].hex(), 16)
            parsed_answer["Data Length"] = rdata_length
            offset += 2
            # full_addr = []
            # curr_addr = []
            # index = 0
            # for byte in range(offset, offset + rdata_length):
            #     curr_addr.append(str(int(response[offset: offset + 1].hex(), 16)))
            #     index += 1
            #     if not index % 4:
            #         full_addr.append(".".join(curr_addr))
            #         curr_addr.clear()
            #         index = 0
            #the decoding of the server name is the same as the answer server name.
            #note: pass the full message so __decode_name_server can correctly parse when the compression pointer is reached
            parsed_answer['Name Server'] = ".".join(self.__decode_name_server(response, offset))
            parsed_answers.append(parsed_answer)
            # position the offset at the next pos, which is the length of the read data:
            offset += rdata_length
        return (offset, parsed_answers)

    def __decode_additional_rr(self, offset: int, additional_rr: int):
        """Parses the additional RR section of the DNS response if present."""
        if not additional_rr:
            return None
        response = self.__response
        additional_rr_data = {}
        #idea: have a dictionary of dictionaries where the key is the resource and type, instead of a list of resources
        #this is to optimize the process of retrieving the information for the resource queried
        for record in range(additional_rr):
            parsed_additional_rr = {}
            rr_name = "".join(self.__decode_name_server(response, offset))
            #position the offset until '\x00' is found:
            while response[offset]:
                offset += 1
            rr_type = self.__get_rr_definition(int(response[offset: offset + 2].hex(), 16))
            parsed_additional_rr["Type"] = rr_type
            offset += 2
            parsed_additional_rr["Class"] = self.__get_class_type(int(response[offset: offset + 2].hex(), 16))
            offset += 2
            parsed_additional_rr["TTL"] = int(response[offset: offset + 4].hex(), 16)
            offset += 4
            rdata_length = int(response[offset:offset + 2].hex(), 16)
            parsed_additional_rr["Data Length"] = rdata_length
            offset += 2
            if parsed_additional_rr["Type"] == self.__IPv4:
                #only parses IPv4 address
                parsed_additional_rr['Address'] = self.__parse_ipv4_addr(response, offset, rdata_length)
            additional_rr_data[(rr_name,rr_type)] = parsed_additional_rr
            offset += rdata_length
            #TODO: address the IPv6 parsing - needs to consider the offset also.
            #additional_rr_data.append(parsed_additional_rr) #this should be a dict of dictionariews with the key being the server name.
        return additional_rr_data

    def __decode_name_server(self, message: bytes, offset: int):
        """Similar to __decode_name, but allows the introduction of pointers to previously visited strings"""
        #offset = 0
        parsed_name = []
        while message[offset]:
            length = message[offset]
            part_name = ""
            if length == self.__COMPRESSED_NAME:
                #decode the name in the pointer
                part_name += self.__decode_name(message, message[offset + 1])
                parsed_name.append(part_name)
                break
            else:
                #iterates over the name with no pointers to previously seen addresses, decoding char by char:
                for pointer in range(offset + 1, offset + length + 1):
                    part_name += chr(message[pointer])
                parsed_name.append(part_name)
                #move the pointer to the next name position
                offset = pointer + 1
        return parsed_name #"".join(parsed_name)

    def __decode_name(self, name: bytes, offset: int):
        #offset = 0
        parsed_name = []
        while name[offset]:
            length = name[offset]
            part_name = ""
            if length == self.__COMPRESSED_NAME:
                part_name += "".join(self.__decode_name_server(name, offset))
                parsed_name.append(part_name)
                break
            else:
                for pointer in range(offset + 1, offset + length + 1):
                    part_name += chr(name[pointer])
                parsed_name.append(part_name)
            offset = pointer + 1
        return ".".join(parsed_name)

    def __get_rr_definition(self, rr: int) -> str:
        rr_map = {
            1: 'A',
            2: 'NS',
            3: 'MD',
            4: 'MF',
            5: 'CNAME',
            6: 'SOA',
            7: 'MB',
            8: 'MG',
            9: 'MR',
            10: 'NULL',
            11: 'WKS',
            12: 'PTR',
            13: 'HINFO',
            14: 'MINFO',
            15: 'MX',
            16: 'TXT',
            28: 'AAAA'
        }
        return rr_map[rr]

    def __get_class_type(self, class_type: int) -> str:
        class_map = {
            1: 'IN',
            2: 'CS',
            3: 'CH',
            4: 'HS'
        }
        return class_map[class_type]


