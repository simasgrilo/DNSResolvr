import sys

class DNSAnswer:

    def __init__(self, response: bytes):
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
        #ANSWER_SIZE = 12 #12 bytes per answer
        COMPRESSED_NAME = 192
        answers = self.__response[6] + self.__response[7]
        questions = self.__response[4] + self.__response[5]
        #no questions, no responses
        if not questions:
            return None
        #move the pointer from byte 6 to the answers offset - which moves from the questions to the answers
        #you also need the amount of questions to know the offset - 11 bytes is the count from the ID to the queries.
        #each query contains 3 sections of two bytes each - 6 bytes per question
        #the encoded name has a byte
        offset = 12
        response = self.__response
        #ignore the query section:
        for query in range(questions):
            while response[offset]:
                offset += response[offset] + 1 #we need to parse 1 + offset bytes until reaching the EOD \x00.
            #skip the last byte and both type and class entries - each one has a fixed length of two bytes
            offset += 5
        parsed_answers = []
        for answer in range(0, answers):
            #TODO: refactor the parsing process into different methods
            parsed_answer = {}
            name = []
            while response[offset] != b'\x00':
                if response[offset] == COMPRESSED_NAME:
                    #read from the next pointer and return: by the RFC, pointers are only found at the end of a name.
                    name.append(self.__decode_name(response[response[offset + 1]::]))
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
            full_addr = []
            curr_addr = []
            offset += 2
            index = 0
            for byte in range(offset, offset + rdata_length):
                curr_addr.append(str(int(response[offset: offset + 1].hex(),16)))
                index += 1
                if not index % 4:
                    full_addr.append(".".join(curr_addr))
                    curr_addr.clear()
                    index = 0
            parsed_answer['Address'] = full_addr
            parsed_answers.append(parsed_answer)
            #position the offset at the next pos, which is the length of the read data:
            offset += rdata_length


        return parsed_answers


    def __decode_name(self, name:bytes):
        offset = 0
        parsed_name = []
        while name[offset]:
            length = name[offset]
            part_name = ""
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
            16: 'TXT'
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


