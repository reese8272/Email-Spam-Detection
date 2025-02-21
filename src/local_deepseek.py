import model

import basetypes as bt

from ollama import chat
from ollama import ChatResponse

# https://github.com/ollama/ollama/issues/1170
# Looks like it's not possible to give ollama direct DB access.
# TODO try harder

class OllamaDeepseek(bt.Filter):
    nice_name = "Ollama Deepseek"
    # Determine if model said true or false.
    def judgement(self, response: ChatResponse) -> bool:
        text = response.message.content

        if "True" in text:
            result = True
        elif "False" in text:
            result = False
        else:
            # TODO error here
            result = None

        return result

    # Cast to our type
    def chatResponse_to_ModelResponse(self, response: ChatResponse) -> bt.Response:
        newResponse = bt.Response(
            raw_response=response.message,
            judgement = self.judgement(response)
        )
        return newResponse

    # Actually ask the model
    def do_query(self, message:model.Message) -> ChatResponse:
        query = (
                f'Is this email spam? You are to ONLY answer with "True" or "False". '
                f'There will be nothing no other thoughts or feelings. Thanks.\n\n'
                f'Subject: {message.subject}\n'
                f'{message.body}'
        )

        response: ChatResponse = chat(model='deepseek-r1', messages=[
            {
                'role': 'user',
                'content': query,
            },
        ])

        return response


    def check_email(self, message: model.Message) -> bt.Response:
        return self.chatResponse_to_ModelResponse(
            self.do_query(message)
        )
