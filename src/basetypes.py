import model
import os

OUTPUT_PATH = os.path.abspath('output')

def output_to(file_name:str) -> str:
    return f'{OUTPUT_PATH}/{file_name}'

class Response():
    def __init__(self, raw_response, judgement):
        self.raw_response = raw_response
        self.judgement = judgement


class Filter():
    nice_name = None

    # Raise error when not overwritten
    @property
    def nice_name(self):
        raise NotImplementedError

    def check_email(self, message: model.Message) -> Response:
        raise NotImplementedError

