# 📚 AI PDF Chatbot (RAG)

## Overview

AI PDF Chatbot is a Retrieval-Augmented Generation (RAG) based application that allows users to upload a PDF and ask questions related to its content. Instead of answering from general knowledge, the chatbot retrieves the most relevant information from the uploaded document and uses Google's Gemini model to generate accurate responses.

This project was built to learn how Large Language Models (LLMs), embeddings, vector databases, and Retrieval-Augmented Generation work together in a real-world application.

---

## Features

* Upload PDF documents
* Extract text from PDFs
* Split text into smaller chunks
* Generate embeddings using Gemini
* Store embeddings in ChromaDB
* Retrieve the most relevant content using semantic search
* Answer user questions using Gemini
* Display the retrieved source passages
* Maintain chat history during the session
* Clear uploaded PDF
* Clear chat history

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI

### AI & Database

* Google Gemini API
* Gemini Embedding Model
* ChromaDB

### Libraries Used

* PyPDF2
* python-dotenv
* Uvicorn

---

## Project Workflow

1. Upload a PDF document.
2. Extract text from the uploaded PDF.
3. Divide the text into smaller chunks.
4. Generate embeddings for each chunk.
5. Store the embeddings in ChromaDB.
6. Ask a question related to the document.
7. Retrieve the most relevant chunks.
8. Generate the final answer using Gemini.
9. Display the answer along with the retrieved passages.

---

## Folder Structure

```text
AI-PDF-Chatbot/
│
|
├── main.py   
├── rag.py   
├── embedding.py
|── pdf_utils.py
├── chroma_db.py
├── requirements.txt
└── .env│   
│
|
├── index.html
├── style.css
└── script.js
│
└── README.md
```

---

## How to Run

### Clone the repository

```bash
git clone <your-repository-link>
```

### Move to the project folder

```bash
cd AI-PDF-Chatbot
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

### Install the required packages

```bash
pip install -r requirements.txt
```

### Add your Gemini API Key

Create a `.env` file and add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

### Run the backend

```bash
uvicorn main:app --reload
```

After starting the backend, open the frontend and upload a PDF to start asking questions.

---

## Future Improvements

* Support multiple PDF uploads
* Improve embedding speed using batch requests
* Display page numbers for retrieved passages
* Deploy the application online
* Add user authentication

---

## What I Learned

Through this project, I learned:

* Building REST APIs using FastAPI
* Working with Google Gemini API
* Creating embeddings for semantic search
* Using ChromaDB as a vector database
* Implementing a complete RAG pipeline
* Connecting a frontend with a FastAPI backend
* Processing PDF documents and retrieving relevant information

---

## Author

**Kanishka**

This project was built as part of my learning journey in Artificial Intelligence and Large Language Models (LLMs).
