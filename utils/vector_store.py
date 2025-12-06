from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import Optional

_vector_store: Optional[InMemoryVectorStore] = None


def get_vector_store() -> InMemoryVectorStore:
    """
    Get or create the global vector store instance.

    Returns:
        InMemoryVectorStore instance
    """
    global _vector_store

    if _vector_store is None:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        _vector_store = InMemoryVectorStore(embeddings)

    return _vector_store


def index_document(
    content: str,
    metadata: dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> int:
    """
    Index a document into the vector store.

    Args:
        content: Document content to index
        metadata: Metadata for the document (doc_type, project_name, etc.)
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks

    Returns:
        Number of chunks created
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks = text_splitter.split_text(content)

    documents = [
        Document(
            page_content=chunk,
            metadata={**metadata, "chunk_index": i}
        )
        for i, chunk in enumerate(chunks)
    ]

    vector_store = get_vector_store()
    vector_store.add_documents(documents)

    return len(documents)
