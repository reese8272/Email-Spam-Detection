# config.py
from pathlib import Path

# Define project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Moves up one level to project root

# Define dataset path
DATA_PATH = PROJECT_ROOT / "data" / "enron_spam_dataset.csv"
