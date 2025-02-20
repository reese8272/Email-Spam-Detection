import db

class Response():
    def __init__(self, raw_response, judgement):
        self.raw_response = raw_response
        self.judgement = judgement

class Model():
    nice_name = None

    # Raise error when not overwritten
    @property
    def nice_name(self):
        raise NotImplementedError

    def check_email(self, message: db.Message) -> Response:
        raise NotImplementedError

