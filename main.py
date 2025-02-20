import db
import model.local_deepseek
import model.random_bot
from model.types import Model
import model
session = db.init_db()

messages = session.query(db.Message).all()

fname = None

import pickle


def foo(_model: Model):
    records = []
    for m in messages:
        try:
            response = _model.check_email(m)


            print(response.raw_response)
            print(
                "Is spam?"
                f"\nModel answer: {response.judgement}\n" # TODO specify model
                f"Correct answer: {m.spam}"
            )

            print("\n\n")
        # "Log" error and keep going.
        except Exception as e:
            response = model.types.Response(
                str(e),
                None
            )


        # writedown(m, response)
        records.append(
            (m, response)
        )

    with open(fname, 'wb') as f:
        pickle.dump(records, f)


mymodel = model.local_deepseek.OllamaDeepseek()
# mymodel = model.random_bot.RandomGuess()

# TODO create output folder programatically

fname= f"output/{mymodel.nice_name}.pkl"

foo(mymodel)