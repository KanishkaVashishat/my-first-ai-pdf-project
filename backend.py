from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import numpy as np
from pypdf import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Store uploaded PDF text
pdf_text = ""
pdf_chunks = []
pdf_embeddings = []
chat_history = []


# Request model
class ChatRequest(BaseModel):
    message: str

def get_embedding(text):

    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )

    return response.embeddings[0].values

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    global pdf_text, pdf_chunks, chat_history

    try:
        if pdf_text == "":
            return {
                "reply": "Please upload a PDF first."
            }

        history = ""

        for chat in chat_history:
            history += f"User: {chat['user']}\n"
            history += f"Assistant: {chat['assistant']}\n\n"

        prompt = f"""
        ...
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        chat_history.append({
            "user": request.message,
            "assistant": response.text
        })

        return {
            "reply": response.text
        }

    except Exception as e:
        return {
            "reply": str(e)
        }

# -----------------------------
# PDF Upload Endpoint
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text, pdf_chunks, pdf_embeddings

    try:
        # Read PDF
        reader = PdfReader(file.file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        pdf_text = text

        pdf_chunks = []
        pdf_embeddings = []

        chunk_size = 500

        for i in range(0, len(pdf_text), chunk_size):
            chunk = pdf_text[i:i + chunk_size]
            pdf_chunks.append(chunk)

        print("\n========== CHUNKS ==========\n")

        for index, chunk in enumerate(pdf_chunks):
            print(f"Chunk {index + 1}")
            print(chunk[:200])
            print("----------------------------")

        print("\nCreating embeddings...\n")

        for chunk in pdf_chunks:
            embedding = get_embedding(chunk)
            pdf_embeddings.append(embedding)

        print(f"Created {len(pdf_embeddings)} embeddings successfully!")

        return {
            "filename": file.filename,
            "characters": len(pdf_text),
            "chunks": len(pdf_chunks),
            "embeddings": len(pdf_embeddings),
            "message": "PDF processed successfully."
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        
        return {
            "error": str(e)
        }

@app.post("/clear-chat")
def clear_chat():
    global chat_history

    chat_history = []

    return {
        "message": "Chat history cleared successfully."
    }