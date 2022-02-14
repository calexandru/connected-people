class ClientException(Exception):
    pass


class InvalidUserException(ClientException):
    pass


class GenericException(ClientException):
    pass
