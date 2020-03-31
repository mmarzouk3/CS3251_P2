import enum

class Request:
    def __init__(self, method, body=None):
        self.method = method
        self.body = body


    # get functions, not super necessary

    def get_method(self):
        return self.method

    def get_body(self):
        return self.body

class Method(enum.Enum):
    CHECK_USER = enum.auto()
    LOGOUT = enum.auto()
    TWEET = enum.auto()
    GET_USERS = enum.auto()
    GET_TWEETS = enum.auto()
    SUB = enum.auto()
    UNSUB = enum.auto()
    TIMELINE = enum.auto()
