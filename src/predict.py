import tensorflow as tf
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.preprocess import clean_text
from src.config import MODEL_PATH, VECTORIZER_PATH

def load_trained_model():
    if MODEL_PATH.exists():
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded successfully!")
        return model
    else:
        print("⚠️ Model not found! Train it first.")
        return None

def load_vectorizer():
    if VECTORIZER_PATH.exists():
        loaded_model = tf.saved_model.load(VECTORIZER_PATH)
        vectorizer_layer = loaded_model.layers[0] if hasattr(loaded_model, 'layers') else loaded_model
        print("✅ Vectorizer loaded successfully!")
        return vectorizer_layer
    else:
        raise FileNotFoundError("Vectorizer not found! Retrain model first.")

def predict_email(model, email_text):
    try:
        vectorizer = load_vectorizer()
        cleaned_text = clean_text(email_text)
        
        # Handle the vectorizer based on its type
        if hasattr(vectorizer, '__call__'):
            # Direct callable function
            input_vector = vectorizer([cleaned_text])
        elif hasattr(vectorizer, 'predict'):
            # Sequential model with predict method
            input_vector = vectorizer.predict([cleaned_text])
        else:
            # Try direct call as last resort
            input_vector = vectorizer([cleaned_text])
            
        prediction = model.predict(input_vector)
        confidence = prediction.flatten()[0]
        
        # Format with confidence percentage
        result = "Spam" if confidence > 0.5 else "Not Spam"
        return result, confidence 
    
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return "Error: Could not predict"

if __name__ == "__main__":
    model = load_trained_model()
    if model:
        email_text = input("📩 Enter an email to classify: ")
        result = predict_email(model, email_text)
        print(f"🛑 Prediction: {result}")
