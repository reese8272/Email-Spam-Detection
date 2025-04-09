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

        # Handle different column naming conventions
        text_column = None
        label_column = None

        # Common column names for text content
        text_columns = ['text', 'message', 'content', 'email', 'body', 'sms']
        # Common column names for labels
        label_columns = ['label', 'class', 'category', 'spam', 'target', 'type']
        
        # Find the text column
        for col in text_columns:
            if col in df.columns:
                text_column = col
                break
        
        # Find the label column
        for col in label_columns:
            if col in df.columns:
                label_column = col
                break
        
        # If required columns not found, try to guess based on data types
        if text_column is None and len(df.columns) >= 2:
            # Assume the column with string/object type is the text column
            for col in df.columns:
                if df[col].dtype == 'object' or df[col].dtype == 'string':
                    text_column = col
                    break
        
        if label_column is None and text_column is not None and len(df.columns) >= 2:
            # Take the first column that's not the text column
            for col in df.columns:
                if col != text_column:
                    label_column = col
                    break

        # Skip if we couldn't identify needed columns
        if text_column is None or label_column is None:
            print(f"⚠️ Dataset {file.name} missing identifiable text/label columns. Skipping.")
            continue

        # Create a standardized dataframe with 'text' and 'label' columns
        temp_df = pd.DataFrame()
        temp_df['text'] = df[text_column]
        temp_df['label'] = df[label_column]
        dfs.append(temp_df)
        print(f"✓ Loaded {file.name} with {len(temp_df)} rows.")

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True).dropna()
        print(f"✅ Combined dataset shape: {combined_df.shape}")
    else:
        raise ValueError("No valid datasets loaded. Check CSV files.")

    return combined_df

if __name__ == "__main__":
    df = load_dataset()
    print(df.head())
