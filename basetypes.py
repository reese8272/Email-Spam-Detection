import database.model as model
import os
import random
from typing import Sequence, List, Tuple, TypeVar


T = TypeVar('T')

def randomly_split_iter(iter: Sequence[T], percent: float) -> Tuple[List[T], List[T]]:
    """
    Shuffle and split an iterable based on the provided percentage.
    """
    shuffled = random.sample(iter, len(iter))

    # Calculate split sizes
    split_index = int(len(shuffled) * percent)

    # Split the messages
    x = shuffled[:split_index]
    y = shuffled[split_index:]

    return x, y

import pickle
def pickle_it(it, fname):
    with open(f'{fname}.pkl', 'wb') as f:
        pickle.dumps(it, f)



OUTPUT_PATH = os.path.abspath('output')

def output_to(file_name:str) -> str:
    return f'{OUTPUT_PATH}/{file_name}'

class Response():
    def __init__(self, raw_response, judgement):
        self.raw_response = raw_response
        self.judgement = judgement


class Filter():
    # Nice name to display
    @property
    def nice_name(self):
        # Raise error when not overwritten
        raise NotImplementedError

    def check_email(self, message: model.Message) -> Response:
        raise NotImplementedError

