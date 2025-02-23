import tensorflow as tf

def create_model(vocab_size=10000, max_length=100):
    """Creates and returns a text classification model."""
    
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=128),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Reduce learning rate to stabilize training
    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model

if __name__ == "__main__":
    model = create_model()
    model.summary()  # Print model architecture
