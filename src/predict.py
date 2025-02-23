import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Ensure src/ is found

import tensorflow as tf
import numpy as np
from src.preprocess import clean_text, vectorizer, preprocess_dataset
from src.model import create_model

# Define model path
MODEL_PATH = Path("models/spam_classifier.keras")  # Updated model path

def load_trained_model():
    """Loads the trained spam classifier model if it exists."""
    
    # Check if model exists
    if MODEL_PATH.exists():
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully!")
            return model
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None
    else:
        print("⚠️ No trained model found! Please train the model first.")
        return None

def predict_email(model, email_text):
    """Predicts whether an email is spam or not spam."""
    
    # Step 1: Clean the input email
    cleaned_text = clean_text(email_text)

    # Step 2: Ensure vectorizer is initialized before making predictions
    df = preprocess_dataset()
    vectorizer.adapt(df["text"].values)

    # Step 3: Convert text into numerical format
    input_vector = vectorizer([cleaned_text])

    # Step 4: Make prediction and correctly extract scalar value
    prediction_array = model.predict(input_vector)

    # Fix: Ensure we extract a scalar value correctly
    prediction_value = float(np.array(prediction_array).flatten()[0])  # Proper NumPy-safe extraction

    # Step 5: Convert to human-readable label
    return "Spam" if prediction_value > 0.5 else "Not Spam"

if __name__ == "__main__":
    model = load_trained_model()
    
    if model:
        email_text = input("📩 Enter an email to classify: ")
        result = predict_email(model, email_text)
        print(f"🛑 Prediction: {result}")
