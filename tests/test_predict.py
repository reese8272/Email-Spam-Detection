import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Allow imports

from src.predict import predict_email
from src.model import create_model

def test_predict_email():
    """Test that predictions return 'Spam' or 'Not Spam'."""
    model = create_model()
    sample_text = "Congratulations! You've won a free iPhone!"
    prediction = predict_email(model, sample_text)
    
    assert prediction in ["Spam", "Not Spam"], "Prediction output is invalid!"

    print("✅ test_predict_email passed!")

if __name__ == "__main__":
    test_predict_email()
