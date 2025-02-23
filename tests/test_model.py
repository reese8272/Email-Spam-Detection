import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Allow imports

from src.model import create_model
import tensorflow as tf

def test_create_model():
    """Test that the model initializes correctly."""
    model = create_model()
    
    assert isinstance(model, tf.keras.Model), "Model is not a Keras Model!"
    assert len(model.layers) > 1, "Model has too few layers!"
    
    print("✅ test_create_model passed!")

if __name__ == "__main__":
    test_create_model()
