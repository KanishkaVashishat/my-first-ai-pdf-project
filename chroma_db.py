"""
chroma_db.py
Thin wrapper around a persistent ChromaDB collection that stores
PDF chunks and their embeddings, and supports similarity search.
"""

import chromadb

CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "pdf_chunks"

_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(name=COLLECTION_NAME)


def get_collection():
    return _collection


def add_to_collection(chunks: list[str], embeddings: list[list[float]], filename: str):
    """
    Adds chunks + their embeddings to the collection.
    Each chunk gets a unique id based on the filename and its index.
    """
    if not chunks:
        return

    ids = [f"{filename}-{i}" for i in range(len(chunks))]
    metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]

    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )


def query_collection(query_embedding: list[float], top_k: int = 4):
    """
    Returns the top_k most relevant chunks for a given query embedding.
    Returns a list of chunk text strings.
    """
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])
    return documents[0] if documents else []


def clear_collection():
    """
    Wipes the collection so a new PDF can be uploaded fresh.
    """
    global _collection

    _client.delete_collection(name=COLLECTION_NAME)
    _collection = _client.get_or_create_collection(name=COLLECTION_NAME)


def collection_count() -> int:
    return _collection.count()