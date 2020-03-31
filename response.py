import enum

class Response:
    def __init__(self, status, body=None):
        self.status = status
        self.body = body


    # get functions, not super necessary

    def get_status(self):
        return self.status

    def get_body(self):
        return self.body

class Status(enum.Enum):
    ERROR = enum.auto()
    OK = enum.auto()
    PUSH = enum.auto()
