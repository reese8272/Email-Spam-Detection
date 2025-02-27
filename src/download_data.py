import sys
from pathlib import Path

# Add the project root to sys.path (Allows Python to find `src/`)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
from src.config import DATA_PATH

# Define the dataset URL (Use a valid source)
URL = "https://raw.githubusercontent.com/nyu-dl/spam-detection/master/data/enron.csv"

def download_dataset():
    """Downloads the dataset if it's missing."""
    
    # Check if the file already exists
    if DATA_PATH.exists():
        print(f"✅ Dataset already exists at {DATA_PATH}. Skipping download.")
        return

    print(f"📥 Downloading dataset from {URL}...")

    # Send HTTP request to download the dataset
    response = requests.get(URL)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(DATA_PATH, "wb") as f:
            f.write(response.content)
        print(f"✅ Download complete! Dataset saved at {DATA_PATH}")
    else:
        print(f"❌ Failed to download dataset. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    download_dataset()
