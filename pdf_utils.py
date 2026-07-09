"""
pdf_utils.py
Handles PDF text extraction and text chunking for the RAG pipeline.
"""

from pypdf import PdfReader


def extract_text_from_pdf(file) -> str:
    """
    Extracts all text from an uploaded PDF file object.
    `file` should be a file-like object (e.g. UploadFile.file from FastAPI).
    """
    reader = PdfReader(file)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    return extracted_text


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks so that context isn't lost
    at chunk boundaries. Returns a list of chunk strings.
    """
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks