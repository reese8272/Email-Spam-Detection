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

    # Convert label to binary (1 for spam, 0 for ham/legitimate)
    # Handle various label formats in the datasets
    if df['label'].dtype == 'object':  # If labels are strings
        # Map common spam/ham variations to binary values
        spam_indicators = ['spam', 'junk', 'scam', '1', 'yes', 'true', 'unwanted']
        ham_indicators = ['ham', 'legitimate', 'normal', '0', 'no', 'false', 'wanted']
        
        # Convert all labels to lowercase for case-insensitive comparison
        df['label'] = df['label'].astype(str).str.lower()
        
        # Create a mapping function that handles different label formats
        def map_label(label):
            label = str(label).lower().strip()
            if any(indicator in label for indicator in spam_indicators):
                return 1
            elif any(indicator in label for indicator in ham_indicators):
                return 0
            else:
                # Default to 0 (ham) if unrecognized
                return 0
                
        df['label'] = df['label'].apply(map_label)
    else:
        # If labels are already numeric, just ensure they're 0 or 1
        df['label'] = df['label'].astype(int).clip(0, 1)

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
