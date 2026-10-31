
from dotenv import load_dotenv
from google import genai
import os

load_dotenv(override=True)

key = os.getenv("GEMINI_API_KEY", "").strip()

if not key:
    print("Gemini API key not found!")
else:
    try:
        client = genai.Client(api_key=key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Say hello to Sandarbh's AI!"
        )

        print("GEMINI CONNECTION SUCCESSFUL!")
        print(response.text)

    except Exception as error:
        print("GEMINI CONNECTION FAILED!")
        print(type(error).__name__, str(error))
