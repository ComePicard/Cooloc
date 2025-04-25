from pathlib import WindowsPath, Path

from psycopg2.extras import RealDictRow

from app.schemas.documents import Documents


def format_document_from_raw(raw_document: RealDictRow) -> Documents:
    for key in raw_document:
        if isinstance(raw_document[key], WindowsPath):
            raw_document[key] = Path(raw_document[key])
    return Documents(**raw_document)


def format_documents_from_raw(raw_documents: list[RealDictRow]) -> list[Documents]:
    """
    Formate les documents bruts en objets Documents.
    """
    return [format_document_from_raw(raw_document) for raw_document in raw_documents]
