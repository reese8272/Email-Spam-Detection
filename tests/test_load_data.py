import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Ensure src/ is found

from src.load_data import load_dataset

def test_load_dataset():
    """Test that the dataset loads correctly."""
    df = load_dataset()

    # Ensure that it's not empty
    assert df is not None, "Dataset failed to load!"
    assert not df.empty, "Dataset is empty!"

    # Ensure it has expected columns
    assert "text" in df.columns, "Column 'text' is missing!"
    assert "label" in df.columns, "Column 'label' is missing!"

    print("✅ test_load_dataset passed!")

if __name__ == "__main__":
    test_load_dataset()
