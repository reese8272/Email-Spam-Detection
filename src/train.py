import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Ensure src/ is found

import tensorflow as tf
from src.model import create_model
from src.preprocess import preprocess_dataset, vectorizer

# Training parameters
EPOCHS = 10
BATCH_SIZE = 32
MODEL_PATH = Path("models/spam_classifier.keras")  # Updated model path

def prepare_tf_dataset():
    """Converts preprocessed text into a TensorFlow dataset."""
    df = preprocess_dataset()

    # Ensure vectorizer is adapted to the dataset
    vectorizer.adapt(df["text"].values)

    dataset = tf.data.Dataset.from_tensor_slices((vectorizer(df["text"].values), df["label"].values))
    
    # Properly shuffle, batch, and prefetch dataset
    dataset = dataset.shuffle(len(df)).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    return dataset

def train_model():
    """Loads data, trains the model, and saves it in `.keras` format."""
    dataset = prepare_tf_dataset()

    # Split into 80% training and 20% validation
    train_size = int(0.8 * len(dataset))
    train_dataset = dataset.take(train_size)
    val_dataset = dataset.skip(train_size)

    # Initialize the model
    model = create_model()

    # Train the model
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )

    # Save the trained model in the new Keras format
    model.save(MODEL_PATH)  # New recommended format
    print(f"✅ Model training complete! Saved as '{MODEL_PATH}'.")

    return model, history

if __name__ == "__main__":
    train_model()
