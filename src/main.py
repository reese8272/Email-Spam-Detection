import sys
import os
from pathlib import Path
import streamlit as st
import time
from download_data import download_dataset
from train import train_model
from predict import load_trained_model, predict_email
from config import MODEL_PATH

# Set encoding for Windows console (optional)
if sys.platform == "win32":
    os.system("chcp 65001")
    sys.stdout.reconfigure(encoding="utf-8")

# Streamlit web interface
def main():
    st.set_page_config(page_title="Email Spam Detection", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select page:", ["Home", "Download Dataset", "Train Model", "Make Prediction"])

    if page == "Home":
        st.title("📧 Email Spam Detection")
        st.image("https://img.icons8.com/color/96/000000/spam-can.png", width=100)
        st.markdown("""
        ## Welcome!

        Use the sidebar to navigate:

        - **Download Dataset**: Fetch dataset for training.
        - **Train Model**: Train your spam detection model.
        - **Make Prediction:** Test the trained model.
        """)

        if os.path.exists(MODEL_PATH):
            st.success("✅ Model is trained and ready to use!")
        else:
            st.warning("⚠️ Model needs training.")

    elif page == "Download Dataset":
        st.header("📥 Download Dataset")
        if st.button("Download Dataset"):
            with st.spinner("Downloading dataset..."):
                success = download_dataset()
                if success:
                    st.success("Dataset downloaded successfully!")
                else:
                    st.error("Error downloading dataset.")

    elif page == "Train Model":
        st.header("🚀 Train Model")
        if st.button("Start Training"):
            with st.spinner("Training model..."):
                success = train_model()
                if success:
                    st.success("🎉 Model trained successfully!")
                else:
                    st.error("Training failed. Ensure the dataset is downloaded.")

    elif page == "Make Prediction":
        st.header("🔍 Make a Prediction")
        model = load_trained_model()
        if model:
            email_text = st.text_area("Enter email content:")
            if st.button("Classify"):
                if email_text.strip():
                    with st.spinner("Analyzing email..."):
                        result = predict_email(model, email_text)
                        if result == 1:
                            st.error("🚩 This email is spam.")
                        else:
                            st.success("✅ This email is legitimate.")
                else:
                    st.warning("Please enter email text to classify.")
        else:
            st.error("Model not trained yet. Please train the model first.")

if __name__ == "__main__":
    main()
