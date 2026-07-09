"""
rag.py
Ties retrieval (Chroma) and generation (Gemini) together into a single
RAG pipeline used by the /chat route.
"""

from google import genai
from dotenv import load_dotenv
import os

import embedding
import chroma_db

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

GENERATION_MODEL = "gemini-2.5-flash"

TOP_K = 4


def retrieve_relevant_chunks(question: str, top_k: int = TOP_K) -> list[str]:
    """
    Embeds the question and retrieves the top_k most relevant PDF chunks.
    """
    query_embedding = embedding.get_embedding(question)
    return chroma_db.query_collection(query_embedding, top_k=top_k)


def build_prompt(question: str, context_chunks: list[str], history: str) -> str:
    context = "\n\n---\n\n".join(context_chunks) if context_chunks else "No relevant context found."

    prompt = f"""
You are an AI Tutor.

Rules:

1. Answer ONLY using the provided PDF context below.

2. If the answer is not present say:

'I couldn't find that information in the uploaded PDF.'

3. If the user asks for a summary,
summarize only the provided context.

4. Be concise.

PDF Context:

{context}

Conversation:

{history}

Question:

{question}

"""
    return prompt


def generate_answer(question: str, history: str, top_k: int = TOP_K):
    """
    Full RAG flow: retrieve relevant chunks, build the prompt, call Gemini.
    Returns a tuple of (answer_text, source_chunks_used).
    """
    context_chunks = retrieve_relevant_chunks(question, top_k=top_k)

    prompt = build_prompt(question, context_chunks, history)

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt
    )

    answer = response.text

    return answer, context_chunks