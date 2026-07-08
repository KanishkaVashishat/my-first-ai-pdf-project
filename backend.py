from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from pypdf import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

pdf_text = ""
chat_history = []


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    global pdf_text, chat_history

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
You are an AI Tutor.

Answer ONLY using the information provided in the PDF below.

If the answer is not present in the PDF, reply exactly:

"I couldn't find that information in the uploaded PDF."

---------------- PDF ----------------

{pdf_text}

-------------------------------------

Previous Conversation:

{history}

User Question:

{request.message}
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
        print("CHAT ERROR:", e)

        return {
            "reply": str(e)
        }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text

    try:
        reader = PdfReader(file.file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        pdf_text = text

        return {
            "filename": file.filename,
            "characters": len(pdf_text),
            "message": "PDF uploaded successfully."
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