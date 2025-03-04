import sys
from pathlib import Path

# Add the project root to sys.path (Allows Python to find `src/`)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
from src.config import DATA_PATH, DATA_DIR

# Define multiple dataset URLs in case one fails
URLS = [
    "https://raw.githubusercontent.com/nyu-dl/spam-detection/master/data/enron.csv",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
]

def download_dataset():
    """Downloads the dataset if it's missing."""
    
    # Check if the file already exists
    if DATA_PATH.exists():
        print(f"✅ Dataset already exists at {DATA_PATH}. Skipping download.")
        return

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    
    for url in URLS:
        try:
            print(f"📥 Attempting to download dataset from {url}...")
            
            # Send HTTP request to download the dataset
            response = requests.get(url, timeout=30)
            
            # Check if the request was successful
            if response.status_code == 200:
                with open(DATA_PATH, "wb") as f:
                    f.write(response.content)
                print(f"✅ Download complete! Dataset saved at {DATA_PATH}")
                return
            else:
                print(f"⚠️ Failed to download from {url}. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error downloading from {url}: {str(e)}")
    
    print("❌ Failed to download dataset from all sources.")

if __name__ == "__main__":
    download_dataset()
