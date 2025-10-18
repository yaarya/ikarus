import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file to get your key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the client
genai.configure(api_key=GOOGLE_API_KEY)

print("Finding available models that support 'generateContent'...\n")

# List all models and find the ones that work for our app
for model in genai.list_models():
  if 'generateContent' in model.supported_generation_methods:
    print(f"- {model.name}")

print("\nCopy one of the model names from the list above (usually the simplest one) and use it in your main.py file.")