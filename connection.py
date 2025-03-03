import random

# Simulated function to mock an API call
def fake_api_predict(email_text):
    print(f"Simulating API call with email: {email_text[:30]}...")  # Just printing part of the email
    return "Spam" if random.choice([True, False]) else "Ham"
