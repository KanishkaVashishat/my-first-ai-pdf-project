from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents="Hello world"
    )

    print(response)

except Exception as e:
    print(e)