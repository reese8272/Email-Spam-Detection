import pandas as pd
import tensorflow as tf
from src.load_data import load_dataset

# Constants
VOCAB_SIZE = 10000  # Maximum number of unique words
MAX_LENGTH = 100  # Max length of each text sequence

# Define Text Vectorization
vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_sequence_length=MAX_LENGTH
)

def clean_text(text):
    """Cleans email text: lowercasing, removing punctuation & extra spaces."""
    if not isinstance(text, str):  # Ensure text is a string
        return ""  # Convert NaN values to empty strings
    
    text = text.lower()
    return text

def preprocess_dataset():
    """Loads, cleans, tokenizes, and prepares the dataset."""
    df = load_dataset()

    # Drop unnecessary columns (fix extra Unnamed columns issue)
    df = df[["text", "label"]]  

    # Check for NaN values
    print("Checking for NaN values in dataset...")
    print(df.isnull().sum())  # Print count of NaN values per column

    # Drop rows where `label` is missing
    df = df.dropna(subset=["label"])

    # Ensure all labels are valid (either 'spam' or 'ham')
    df = df[df["label"].isin(["spam", "ham"])]

    # Replace NaN values in `text` with empty strings
    df["text"] = df["text"].fillna("")

    # Convert labels to binary (spam = 1, ham = 0)
    df["label"] = df["label"].map({"ham": 0, "spam": 1})

    return df
