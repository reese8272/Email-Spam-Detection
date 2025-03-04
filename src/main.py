import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Ensure src/ is found

from src.download_data import download_dataset
from src.train import train_model
from src.predict import load_trained_model, predict_email
from src.config import MODEL_PATH

# Force UTF-8 encoding for Windows (fix UnicodeEncodeError)
if sys.platform == "win32":
    os.system("chcp 65001")  # Set Windows console to UTF-8
    sys.stdout.reconfigure(encoding="utf-8")  # Force Python to use UTF-8

def main():
    """Main menu for running different parts of the spam detection project."""
    while True:
        print("\n📌 Email Spam Detection System")  # Now UTF-8 should work
        print("1️⃣  Download Dataset")
        print("2️⃣  Train Model")
        print("3️⃣  Make a Prediction")
        print("4️⃣  Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            print("\n📥 Downloading dataset...")
            download_dataset()
        elif choice == "2":
            print("\n🚀 Training model...")
            train_model()
        elif choice == "3":
            print("\n🔍 Making a prediction...")
            model = load_trained_model()
            if model:
                email_text = input("📩 Enter an email to classify: ")
                result = predict_email(model, email_text)
                print(f"🛑 Prediction: {result}")
            else:
                print("⚠️ Please train the model first.")
        elif choice == "4":
            print("\n✅ Exiting... Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-4.")

if __name__ == "__main__":
    main()
