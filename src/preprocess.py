import re
import pandas as pd
import tensorflow as tf
from src.load_data import load_dataset
from src.config import VECTORIZER_PATH

VOCAB_SIZE = 10000
MAX_LENGTH = 100

vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_sequence_length=MAX_LENGTH
)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_dataset():
    df = load_dataset()

    df['text'] = df['text'].fillna("").apply(clean_text)

    df['label'] = df['label'].str.lower().map({
        'spam': 1, 'ham': 0, 'scam': 1, 'legitimate': 0
    }).fillna(0).astype(int)

    return df

def get_vectorizer(texts=None):
    """Get or create and adapt the vectorizer"""
    if texts is not None:
        # Create and adapt a new vectorizer
        vectorizer.adapt(texts)
        
        # Save the vectorizer
        export_model = tf.keras.Sequential([vectorizer])
        tf.saved_model.save(export_model, VECTORIZER_PATH)
    
    return vectorizer
