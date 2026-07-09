"""
embedding.py
Wraps Gemini's embedding API (models/embedding-001) so the rest of the
app only ever deals with plain lists of floats.
"""

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-001"

def get_embedding(text: str) -> list[float]:
    """
    Returns the embedding vector for a single piece of text.
    """
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )
    return result.embeddings[0].values


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Returns embedding vectors for a list of texts.
    Calls the API once per chunk to keep this simple and reliable.
    """
    embeddings = []

    for text in texts:
        embeddings.append(get_embedding(text))

    return embeddings