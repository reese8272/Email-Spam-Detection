from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data and Model Paths
DATA_DIR = PROJECT_ROOT / "data"
# Remove the single DATA_PATH since we're handling multiple CSV files
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "spam_classifier.keras"
VECTORIZER_PATH = MODELS_DIR / "vectorizer"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
