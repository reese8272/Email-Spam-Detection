from pathlib import Path
import sys
import os

def get_base_path():
    try:
        # PyInstaller bundles the app into a temp dir and stores the path in _MEIPASS
        return Path(sys._MEIPASS)
    except AttributeError:
        return Path(__file__).resolve().parent.parent

# Project root directory (adjusted for PyInstaller)
PROJECT_ROOT = get_base_path()

# Data and Model Paths
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "spam_classifier.keras"
VECTORIZER_PATH = MODELS_DIR / "vectorizer"

# Create necessary directories (only safe outside PyInstaller)
if not hasattr(sys, '_MEIPASS'):
    DATA_DIR.mkdir(exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)
