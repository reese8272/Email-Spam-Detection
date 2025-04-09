import sys
from pathlib import Path
import zipfile
import io

# Add the project root to sys.path (Allows Python to find `src/`)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
from src.config import DATA_DIR

# Define multiple dataset URLs
DATASET_SOURCES = [
    {
        "url": "https://raw.githubusercontent.com/nyu-dl/spam-detection/master/data/enron.csv",
        "filename": "enron_spam.csv",
        "type": "csv"
    },
    {
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip",
        "filename": "sms_spam.csv",
        "type": "zip",
        "extract_file": "SMSSpamCollection",
        "format": "tsv"  # Tab-separated values
    }
]

def download_dataset():
    """Downloads multiple datasets if they're missing."""
    
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    
    # Check if we have at least one dataset
    existing_files = list(DATA_DIR.glob("*.csv"))
    if existing_files:
        print(f"✅ Found {len(existing_files)} existing dataset(s). Skipping download.")
        return True
    
    success = False
    for source in DATASET_SOURCES:
        try:
            target_path = DATA_DIR / source["filename"]
            if target_path.exists():
                print(f"✅ Dataset {source['filename']} already exists. Skipping.")
                success = True
                continue
                
            print(f"📥 Attempting to download dataset from {source['url']}...")
            response = requests.get(source["url"], timeout=30)
            
            if response.status_code == 200:
                if source["type"] == "csv":
                    # Direct CSV file
                    with open(target_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Download complete! Dataset saved at {target_path}")
                    success = True
                    
                elif source["type"] == "zip":
                    # Handle ZIP file
                    z = zipfile.ZipFile(io.BytesIO(response.content))
                    
                    if "extract_file" in source:
                        # Extract specific file from zip
                        extract_file = source["extract_file"]
                        if extract_file in z.namelist():
                            content = z.read(extract_file)
                            
                            # Handle TSV format if specified
                            if source.get("format") == "tsv":
                                # Convert TSV to CSV format
                                import pandas as pd
                                # For SMS Spam Collection specifically
                                df = pd.read_csv(io.StringIO(content.decode('utf-8')), 
                                               sep='\t', header=None, names=["label", "text"])
                                df.to_csv(target_path, index=False)
                            else:
                                # Save as-is
                                with open(target_path, "wb") as f:
                                    f.write(content)
                                    
                            print(f"✅ Extracted {extract_file} from zip to {target_path}")
                            success = True
                        else:
                            print(f"⚠️ File {extract_file} not found in zip. Available files: {z.namelist()}")
                    else:
                        # Extract all files from zip
                        z.extractall(DATA_DIR)
                        print(f"✅ Extracted all files from zip to {DATA_DIR}")
                        success = True
            else:
                print(f"⚠️ Failed to download from {source['url']}. HTTP Status: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error downloading from {source['url']}: {str(e)}")
    
    if success:
        print("✅ Successfully downloaded at least one dataset.")
        return True
    else:
        print("❌ Failed to download any datasets.")
        return False

if __name__ == "__main__":
    download_dataset()
