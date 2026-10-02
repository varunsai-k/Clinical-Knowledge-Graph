from typing import List
from pydantic import BaseModel

from src.ingestion.loader import Document


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    source: str
    document_type: str
    chunk_index: int
    text: str


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 800,
    overlap: int = 100
) -> List[DocumentChunk]:

    chunks = []

    for document in documents:

        text = document.text

        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunk_id = (
                f"{document.document_id}"
                f"_chunk_{chunk_index}"
            )

            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    source=document.source,
                    document_type=document.document_type,
                    chunk_index=chunk_index,
                    text=chunk_text
                )
            )

            if end >= len(text):
                break

            start = end - overlap
            chunk_index += 1

    return chunks
