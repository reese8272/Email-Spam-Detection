import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Ensure src/ is found

import pandas as pd
from src.config import DATA_PATH
from src.download_data import download_dataset  # Import download function

def load_dataset():
    """Loads the dataset, downloading it if necessary."""
    
    # If the file is missing, download it
    if not DATA_PATH.exists():
        print("⚠️ Dataset missing. Attempting to download...")
        download_dataset()
    
    # Load the dataset with low_memory=False to avoid DtypeWarning
    try:
        df = pd.read_csv(DATA_PATH, low_memory=False)
        print(f"✅ Dataset successfully loaded! Shape: {df.shape}")  # Print confirmation
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None  # Ensures a failed load doesn’t break downstream code

    return df

if __name__ == "__main__":
    df = load_dataset()
    if df is not None:
        print(df.head())  # Show first few rows if loaded successfully
