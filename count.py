import pickle

def check_judgements(fname: str):
    # Load records from the pickle file
    with open(f'output/{fname}', 'rb') as f:
        records = pickle.load(f)

    total = 0
    correct = 0

    # Iterate through each record (each record is a tuple: (message, response))
    for m, response in records:
        total += 1
        # Compare the model's judgement with the correct spam value
        if response.judgement == m.spam:
            correct += 1

    # Compute accuracy percentage
    accuracy = (correct / total * 100) if total > 0 else 0

    print(f"Total records: {total}")
    print(f"Correct judgements: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

# Example usage:
check_judgements('Random Guess.pkl')


# check("Random Guess.txt")