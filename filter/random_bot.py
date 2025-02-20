from database import model
from basetypes import Filter
from basetypes import Response

import random

class RandomGuess(Filter):
    nice_name = "Random Guess"

    def check_email(self, message: model.Message) -> Response:
        return Response(
            raw_response="I guessed.",
            judgement=random.choice([True, False])
        )


