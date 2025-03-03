import tkinter as tk
from tkinter import messagebox
from connection import fake_api_predict

# Function to handle the "Check Spam" button click
def check_spam():
    email_text = email_input.get("1.0", tk.END).strip()
    if not email_text:
        messagebox.showwarning("Input Error", "Please enter email content.")
        return
    
    # Simulate the API call
    result = fake_api_predict(email_text)
    
    # Show the result in a message box
    messagebox.showinfo("Prediction", f"The email is classified as: {result}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Spam Detection System")
root.geometry("400x300")

# Create and pack the widgets
label = tk.Label(root, text="Enter email content below:")
label.pack(pady=5)

email_input = tk.Text(root, height=10, width=40)
email_input.pack(pady=5)

check_button = tk.Button(root, text="Check Spam", command=check_spam)
check_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
