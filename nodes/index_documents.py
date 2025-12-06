import os
from utils.vector_store import index_document
from utils.file_manager import load_document
from typing import TypedDict


class AgentState(TypedDict):
    transcript: str
    session_id: str
    analysis: dict
    requirements_doc: str
    pdd_doc: str
    user_stories_doc: str
    document_paths: list[str]
    indexed: bool


def index_documents_node(state: AgentState) -> dict:
    """
    Index all generated documents into the vector store.

    Args:
        state: Current agent state

    Returns:
        Updated state with indexed=True
    """
    document_paths = state.get("document_paths", [])
    analysis = state["analysis"]
    project_name = analysis["project_name"]

    for filepath in document_paths:
        if not filepath:
            continue

        filename = os.path.basename(filepath)
        doc_type = filename.split("-")[0]
        content = load_document(filepath)

        metadata = {
            "project_name": project_name,
            "doc_type": doc_type,
            "filepath": filepath
        }

        index_document(content, metadata)

    return {
        "indexed": True
    }
