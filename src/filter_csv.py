from connector import init_db
import model
import basetypes as bt
from local_deepseek import OllamaDeepseek

import pickle

import os

# GPT slop
def load_existing_records(fname: str):
    """Load the existing records from the pickle file, if it exists."""
    if os.path.exists(fname):
        with open(fname, 'rb') as f:
            try:
                # Expecting a single object (list of records)
                records = pickle.load(f)
            except EOFError:
                records = []
    else:
        records = []
    return records

def save_records(fname: str, records) -> None:
    """Save all records to the pickle file as a single object."""


    os.makedirs(os.path.dirname(fname), exist_ok=True)
    
    with open(fname, 'wb') as f:
        pickle.dump(records, f)

def FilterCSVtoPickle(
        filter: bt.Filter,
        messages: [model.Message],
        out_name: str
) -> None:
    """
    Run filter against CSV
    """
    records = []
    save_records(out_name, records) # Save
    counter = 0
    for m in messages:
        counter += 1
        try:
            response = filter.check_email(m)


            print(response.raw_response)
            print(
                "Is spam?"
                f"\nModel answer: {response.judgement}\n"
                f"Correct answer: {m.spam}"
            )

            print("\n\n")

        # "Log" error and keep going.
        except Exception as error:
            response = bt.Response(
                str(error),
                None
            )

        records.append((m, response))

        # Write every x times
        if counter > 100:
            counter = 0
            records += load_existing_records(fname) # Load and append
            save_records(out_name, records) # Save
            records = []



if __name__ == "__main__":
    session = init_db('dataset.csv')
    messages = session.query(model.Message).all()

    myfilter = OllamaDeepseek()
    # myfilter = filter.RandomGuess()

    fname = bt.output_to(f"{myfilter.nice_name}.pkl")

    FilterCSVtoPickle(
        myfilter,
        messages,
        fname
    )
