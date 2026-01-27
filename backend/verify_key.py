from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"Key present: {bool(key)}")

client = genai.Client(api_key=key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hello",
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
