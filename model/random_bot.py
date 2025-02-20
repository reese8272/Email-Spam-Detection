import db
import model.types as types

from model.types import Response

import random

class RandomGuess(types.Model):
    nice_name = "Random Guess"

    def check_email(self, message: db.Message) -> Response:
        return Response(
            raw_response="I guessed.",
            judgement=random.choice([True, False])
        )


