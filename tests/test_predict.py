import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Allow imports

from src.predict import predict_email
from src.model import create_model

def test_predict_email():
    """Test that predictions return 'Spam' or 'Not Spam' with confidence."""
    model = create_model()
    sample_text = "Congratulations! You've won a free iPhone!"
    prediction = predict_email(model, sample_text)
    
    # Check that prediction contains either "Spam" or "Not Spam" and has confidence
    assert ("Spam" in prediction or "Not Spam" in prediction), "Prediction output is invalid!"
    assert "Confidence:" in prediction, "Confidence score not included in prediction!"

    print("✅ test_predict_email passed!")

if __name__ == "__main__":
    test_predict_email()
