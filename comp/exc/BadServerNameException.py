
class BadServerNameException(ValueError):

    def __init__(self, message):
        super()
        self.__message = message

    def get_message(self):
        return self.__message
