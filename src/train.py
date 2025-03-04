import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.preprocess import preprocess_dataset, get_vectorizer, VOCAB_SIZE, MAX_LENGTH
from src.model import create_model
from src.config import MODEL_PATH, MODELS_DIR

def train_model(epochs=10, batch_size=64):
    """Train the spam classification model."""
    
    # Ensure models directory exists
    MODELS_DIR.mkdir(exist_ok=True)
    
    print("🔍 Preprocessing dataset...")
    df = preprocess_dataset()
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'].values, df['label'].values, 
        test_size=0.2, random_state=42
    )
    
    print("🔄 Adapting text vectorizer...")
    vectorizer = get_vectorizer(X_train)
    
    # Vectorize the text data
    X_train_vec = vectorizer(np.array([[text] for text in X_train])).numpy()
    X_test_vec = vectorizer(np.array([[text] for text in X_test])).numpy()
    
    # Create and compile the model
    print("🏗️ Creating model...")
    model = create_model(vocab_size=VOCAB_SIZE, max_length=MAX_LENGTH)
    
    # Define callbacks, isn't used but can be if needed
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=2, restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=1
        )
    ]
    
    # Train the model
    print(f"🚀 Training model for {epochs} epochs...")
    history = model.fit(
        X_train_vec, y_train,
        validation_data=(X_test_vec, y_test),
        epochs=epochs,
        batch_size=batch_size,
    )
    
    # Evaluate the model
    loss, accuracy = model.evaluate(X_test_vec, y_test)
    print(f"📊 Test Accuracy: {accuracy:.4f}")
    
    # Save the model
    print(f"💾 Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    print("✅ Training complete!")
    
    return history

if __name__ == "__main__":
    train_model()
