from pathlib import Path
from typing import List
from pydantic import BaseModel


class Document(BaseModel):
    document_id: str
    source: str
    document_type: str
    text: str


def detect_document_type(filename: str) -> str:
    filename = filename.lower()

    if "drug_label" in filename:
        return "drug_label"

    if "clinical_trial" in filename:
        return "clinical_trial"

    return "unknown"


def load_documents(data_dir: str = "data/raw") -> List[Document]:

    data_path = Path(data_dir)

    documents = []

    for file_path in sorted(data_path.glob("*.txt")):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        document = Document(
            document_id=file_path.stem,
            source=file_path.name,
            document_type=detect_document_type(
                file_path.name
            ),
            text=text
        )

        documents.append(document)

    return documents
