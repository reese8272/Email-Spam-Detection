import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Allow imports

from src.preprocess import clean_text, preprocess_dataset

def test_clean_text():
    """Test that text cleaning removes unnecessary characters."""
    sample_text = "Hello!!! Visit http://example.com NOW!!!"
    cleaned_text = clean_text(sample_text)
    
    assert "http" not in cleaned_text, "URLs were not removed!"
    assert "!" not in cleaned_text, "Punctuation was not removed!"
    assert cleaned_text == "hello visit now", "Lowercasing or cleaning failed!"

    print("✅ test_clean_text passed!")

def test_preprocess_dataset():
    """Test that dataset preprocessing works."""
    df = preprocess_dataset()
    
    assert df is not None, "Preprocessed dataset is None!"
    assert "text" in df.columns, "Missing column: 'text'"
    assert "label" in df.columns, "Missing column: 'label'"

    print("✅ test_preprocess_dataset passed!")

if __name__ == "__main__":
    test_clean_text()
    test_preprocess_dataset()
