import sys
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox, filedialog
from download_data import download_dataset
from train import train_model
from predict import load_trained_model, predict_email
from config import MODEL_PATH

# Set encoding for Windows console (optional)
if sys.platform == "win32":
    os.system("chcp 65001")
    sys.stdout.reconfigure(encoding="utf-8")

class SpamDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spam Detection")
        self.root.geometry("800x500")
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        # Navigation menu
        self.nav_frame = ctk.CTkFrame(self.root, width=200)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.pages = {
            "Home": self.home_page,
            "Download Dataset": self.download_dataset_page,
            "Train Model": self.train_model_page,
            "Make Prediction": self.make_prediction_page,
        }

        for page_name in self.pages:
            button = ctk.CTkButton(self.nav_frame, text=page_name, command=self.pages[page_name])
            button.pack(fill="x", pady=5)

        # Main content area
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Load the home page by default
        self.home_page()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def home_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📧 Email Spam Detection", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self.content_frame, text="Welcome! Use the navigation menu to explore the app.", wraplength=500).pack(pady=5)

        if os.path.exists(MODEL_PATH):
            ctk.CTkLabel(self.content_frame, text="✅ Model is trained and ready to use!", text_color="green").pack(pady=5)
        else:
            ctk.CTkLabel(self.content_frame, text="⚠️ Model needs training.", text_color="red").pack(pady=5)

    def download_dataset_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📥 Download Dataset", font=("Arial", 20)).pack(pady=10)

        def download_action():
            success = download_dataset()
            if success:
                messagebox.showinfo("Success", "Dataset downloaded successfully!")
            else:
                messagebox.showerror("Error", "Error downloading dataset.")

        download_button = ctk.CTkButton(self.content_frame, text="Download Dataset", command=download_action)
        download_button.pack(pady=10)

    def train_model_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="🚀 Train Model", font=("Arial", 20)).pack(pady=10)

        def train_action():
            success = train_model()
            if success:
                messagebox.showinfo("Success", "🎉 Model trained successfully!")
            else:
                messagebox.showerror("Error", "Training failed. Ensure the dataset is downloaded.")

        train_button = ctk.CTkButton(self.content_frame, text="Start Training", command=train_action)
        train_button.pack(pady=10)

    def make_prediction_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="🔍 Make a Prediction", font=("Arial", 20)).pack(pady=10)

        model = load_trained_model()
        if model:
            ctk.CTkLabel(self.content_frame, text="Upload a file containing emails (one email per line):").pack(pady=5)

            # Variable to store the uploaded file content
            uploaded_emails = []

            # Scrollable text box to display uploaded file content
            upload_text = ctk.CTkTextbox(self.content_frame, height=150)
            upload_text.pack(pady=5, fill="both", expand=True)

            def upload_file_action():
                file_path = filedialog.askopenfilename(
                    title="Select Email File",
                    filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
                )
                if file_path:
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            emails = file.readlines()

                        # Store the uploaded emails and display them in the text box
                        uploaded_emails.clear()
                        uploaded_emails.extend(emails)
                        upload_text.delete("1.0", "end")
                        upload_text.insert("1.0", "".join(emails))

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to read the file: {e}")
                else:
                    messagebox.showwarning("Warning", "No file selected.")

            upload_button = ctk.CTkButton(self.content_frame, text="Upload File", command=upload_file_action)
            upload_button.pack(pady=5)

            # Scrollable text box to display classification results
            results_text = ctk.CTkTextbox(self.content_frame, height=150)
            results_text.pack(pady=5, fill="both", expand=True)

            def make_prediction_action():
                if not uploaded_emails:
                    messagebox.showwarning("Warning", "No file uploaded. Please upload a file first.")
                    return

                try:
                    results = []
                    for email in uploaded_emails:
                        email_content = email.strip()
                        if email_content:
                            result = predict_email(model, email_content)
                            results.append(f"{result} -> {email_content}")

                    # Display classification results in the scrollable text box
                    results_text.delete("1.0", "end")
                    results_text.insert("1.0", "\n".join(results))

                    # Save results to a file
                    def save_results_action():
                        save_path = filedialog.asksaveasfilename(
                            title="Save Results",
                            defaultextension=".txt",
                            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
                        )
                        if save_path:
                            with open(save_path, "w", encoding="utf-8") as save_file:
                                save_file.write("\n".join(results))
                            messagebox.showinfo("Success", "Results saved successfully!")

                    save_button = ctk.CTkButton(self.content_frame, text="Download Results", command=save_results_action)
                    save_button.pack(pady=10)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process the file: {e}")

            make_prediction_button = ctk.CTkButton(self.content_frame, text="Make Prediction", command=make_prediction_action)
            make_prediction_button.pack(pady=5)

        else:
            ctk.CTkLabel(self.content_frame, text="Model not trained yet. Please train the model first.", text_color="red").pack(pady=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SpamDetectionApp(root)
    root.mainloop()
