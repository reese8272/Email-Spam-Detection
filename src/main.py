import sys
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox, filedialog
from download_data import download_dataset
from train import train_model
from predict import load_trained_model, predict_email
from config import MODEL_PATH
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set encoding for Windows console (optional)
if sys.platform == "win32":
    os.system("chcp 65001")
    sys.stdout.reconfigure(encoding="utf-8")

class SpamDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spam Detection")
        self.root.geometry("1200x1000")
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        # Instance variables to store uploaded emails and processed results
        self.uploaded_emails = []  # Stores the content of the uploaded file
        self.processed_results = []  # Stores the prediction results
        self.confidence_scores = []  # Stores confidence scores for predictions
        self.model = None  # Stores the loaded model

        # Load the model when the application starts
        if os.path.exists(MODEL_PATH):
            try:
                self.model = load_trained_model()
                self.model_status = "✅ Model is trained and ready to use!"
                self.model_status_color = "green"
            except Exception as e:
                self.model = None
                self.model_status = f"⚠️ Failed to load the model: {e}"
                self.model_status_color = "red"
        else:
            self.model = None
            self.model_status = "⚠️ Model needs training."
            self.model_status_color = "red"

        # Navigation menu
        self.nav_frame = ctk.CTkFrame(self.root, width=200)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.pages = {
            "Home": self.home_page,
            "Make Prediction": self.make_prediction_page,
            # Development
            # "Download Dataset": self.download_dataset_page,
            # "Train Model": self.train_model_page,
            "Visualize Results": self.visualize_results_page,
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

        # Display model status
        ctk.CTkLabel(self.content_frame, text=self.model_status, text_color=self.model_status_color).pack(pady=5)

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

        if self.model:
            ctk.CTkLabel(self.content_frame, text="Upload a file containing emails (one email per line):").pack(pady=5)

            # Scrollable text box to display uploaded file content
            upload_text = ctk.CTkTextbox(self.content_frame, height=150)
            upload_text.pack(pady=5, fill="both", expand=True)

            # Repopulate the uploaded emails if they exist
            if self.uploaded_emails:
                upload_text.insert("1.0", "".join(self.uploaded_emails))

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
                        self.uploaded_emails = emails
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

            # Repopulate the processed results if they exist
            if self.processed_results:
                results_text.insert("1.0", "\n".join(self.processed_results))

            def make_prediction_action():
                if not self.uploaded_emails:
                    messagebox.showwarning("Warning", "No file uploaded. Please upload a file first.")
                    return

                try:
                    results = []
                    confidence_scores = []
                    for email in self.uploaded_emails:
                        email_content = email.strip()
                        if email_content:
                            result, confidence = predict_email(self.model, email_content)

                            # Calculate adjusted confidence as the distance from 0.5
                            adjusted_confidence = abs(confidence - 0.5) * 2  # Scale to 0-100%

                            # Adjust confidence display based on the prediction
                            if result == "Spam":
                                confidence_display = f"{adjusted_confidence:.2%} confident in Spam"
                            else:
                                confidence_display = f"{adjusted_confidence:.2%} confident in Not Spam"

                            results.append(f"{result} ({confidence_display}) -> {email_content}")
                            confidence_scores.append(adjusted_confidence)

                    # Save results and confidence scores to the instance variables
                    self.processed_results = results
                    self.confidence_scores = confidence_scores

                    # Display classification results in the scrollable text box
                    results_text.delete("1.0", "end")
                    results_text.insert("1.0", "\n".join(results))

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process the file: {e}")

            make_prediction_button = ctk.CTkButton(self.content_frame, text="Make Prediction", command=make_prediction_action)
            make_prediction_button.pack(pady=5)

            # Always display the "Download Results" button
            def save_results_action():
                if not self.processed_results:
                    messagebox.showerror("Error", "No results available to download.")
                    return

                save_path = filedialog.asksaveasfilename(
                    title="Save Results",
                    defaultextension=".txt",
                    filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
                )
                if save_path:
                    try:
                        with open(save_path, "w", encoding="utf-8") as save_file:
                            save_file.write("\n".join(self.processed_results))
                        messagebox.showinfo("Success", "Results saved successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save the file: {e}")

            save_button = ctk.CTkButton(self.content_frame, text="Download Results", command=save_results_action)
            save_button.pack(pady=10)

        else:
            ctk.CTkLabel(self.content_frame, text="Model not trained yet. Please train the model first.", text_color="red").pack(pady=10)

    def visualize_results_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📊 Data Visualization", font=("Arial", 20)).pack(pady=10)

        # Process the stored results to count spam and not spam
        spam_count = sum(1 for result in self.processed_results if result.lower().startswith("spam"))
        not_spam_count = sum(1 for result in self.processed_results if result.lower().startswith("not spam"))

        # Create a pie chart
        labels = ['Spam', 'Not Spam']
        values = [spam_count, not_spam_count]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Spam vs Not Spam")

        # Embed the matplotlib figure in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

        # Create a bar chart for confidence scores if available
        if hasattr(self, "confidence_scores") and self.confidence_scores:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(range(len(self.confidence_scores)), self.confidence_scores, color='skyblue')
            ax.set_title("Confidence Scores for Predictions")
            ax.set_xlabel("Email Index")
            ax.set_ylabel("Confidence Score")
            ax.set_ylim(0, 1)  # Confidence scores are between 0 and 1
            ax.set_xticks(range(len(self.confidence_scores)))
            ax.set_xticklabels([f"Email {i+1}" for i in range(len(self.confidence_scores))], rotation=45, ha="right")

            # Embed the bar chart in the Tkinter frame
            canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SpamDetectionApp(root)
    root.mainloop()
