
class ResultIsEmpty(Exception):
    def __init__(self):
        self.msg = "The result varilable is None. Did you execute make_request method?"
        super().__init__(self.msg)


class NoSuchVideoQuality(Exception):
    def __init__(self):
        self.msg = "No such video quality"
        super().__init__(self.msg)


class NoHeaders(Exception):
    def __init__(self):
        self.msg = "User did not provide a user-agent/headers"
        super().__init__(self.msg)


class NoAdditionalInformation(Exception):
    def __init__(self):
        self.msg = "User did not give an argument to specify to fetch additional information"
        super().__init__(self.msg)


class NoPostData(Exception):
    def __init__(self):
        self.msg = "No post data"
        super().__init__(self.msg)


class InvalidSize(Exception):
    def __init__(self):
        self.msg = "Invalid size requested"
        super().__init__(self.msg)

