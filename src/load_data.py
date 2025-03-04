import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import DATA_DIR

def load_dataset():
    all_files = DATA_DIR.glob("*.csv")
    dfs = []

    for file in all_files:
        print(f"🔄 Loading dataset: {file.name}")
        try:
            df = pd.read_csv(file, low_memory=False, on_bad_lines='skip')  # fixes tokenizing errors
        except Exception as e:
            print(f"⚠️ Error reading {file.name}: {e}. Skipping file.")
            continue

        if 'label' not in df.columns or 'text' not in df.columns:
            print(f"⚠️ Dataset {file.name} missing required columns ('text', 'label'). Skipping.")
            continue

        dfs.append(df[['text', 'label']])

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True).dropna()
        print(f"✅ Combined dataset shape: {combined_df.shape}")
    else:
        raise ValueError("No valid datasets loaded. Check CSV files.")

    return combined_df

if __name__ == "__main__":
    df = load_dataset()
    print(df.head())
