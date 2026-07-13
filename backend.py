from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse  

import pdf_utils
import embedding
import chroma_db
import rag


app = FastAPI(title="AI PDF Chatbot (RAG)")
app = FastAPI()


@app.get("/")
async def serve_home():
    return FileResponse("index.html")

@app.get("/script.js")
async def serve_js():
    return FileResponse("script.js")

@app.get("/style.css")
async def serve_css():
    return FileResponse("style.css")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


pdf_uploaded = False
pdf_filename = ""
pdf_characters = 0
chat_history = []


class ChatRequest(BaseModel):
    message: str



@app.get("/")
def home():
    return {
        "message": "AI PDF Chatbot (RAG) Backend Running"
    }



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_uploaded
    global pdf_filename
    global pdf_characters

    try:
        if file.content_type != "application/pdf":
            return {
                "error": "Only PDF files are allowed."
            }

        extracted_text = pdf_utils.extract_text_from_pdf(file.file)

        if extracted_text.strip() == "":
            return {
                "error": "No text found inside PDF."
            }

        # Reset any previous PDF's vectors before indexing the new one
        chroma_db.clear_collection()

        chunks = pdf_utils.chunk_text(extracted_text, chunk_size=800, overlap=100)
        chunk_embeddings = embedding.get_embeddings_batch(chunks)

        chroma_db.add_to_collection(chunks, chunk_embeddings, file.filename)

        pdf_uploaded = True
        pdf_filename = file.filename
        pdf_characters = len(extracted_text)

        print(f"Created {len(chunks)} chunks for {file.filename}")

        return {
            "filename": file.filename,
            "characters": pdf_characters,
            "chunks": len(chunks),
            "message": "PDF uploaded and indexed successfully."
        }

    except Exception as e:
        print(e)
        return {
            "error": str(e)
        }




@app.post("/chat")
def chat(request: ChatRequest):
    global chat_history

    try:
        if not pdf_uploaded:
            return {
                "reply": "Please upload a PDF first."
            }

        if request.message.strip() == "":
            return {
                "reply": "Question cannot be empty."
            }

        # Keep only last 5 conversations as context
        history = ""
        recent_history = chat_history[-5:]

        for item in recent_history:
            history += f"User: {item['user']}\n"
            history += f"Assistant: {item['assistant']}\n\n"

        answer, sources = rag.generate_answer(request.message, history)

        chat_history.append({
            "user": request.message,
            "assistant": answer
        })

        return {
            "reply": answer,
            "sources": sources
        }

    except Exception as e:
        print(e)
        return {
            "reply": str(e)
        }



@app.get("/history")
def history():
    return {
        "history": chat_history
    }




@app.post("/clear-chat")
def clear_chat():
    global chat_history

    chat_history = []

    return {
        "message": "Chat history cleared successfully."
    }




@app.post("/clear-pdf")
def clear_pdf():
    global pdf_uploaded
    global pdf_filename
    global pdf_characters

    chroma_db.clear_collection()

    pdf_uploaded = False
    pdf_filename = ""
    pdf_characters = 0

    return {
        "message": "PDF removed successfully."
    }




@app.get("/pdf-info")
def pdf_info():
    return {
        "uploaded": pdf_uploaded,
        "filename": pdf_filename,
        "characters": pdf_characters,
        "chunks_indexed": chroma_db.collection_count()
    }