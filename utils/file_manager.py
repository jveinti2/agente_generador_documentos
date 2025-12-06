import os
from pathlib import Path


def save_markdown_document(content: str, project_name: str, doc_type: str, output_dir: str = "./output") -> str:
    """
    Save markdown content to a file with Spanish naming convention.

    Args:
        content: Markdown content to save
        project_name: Name of the project
        doc_type: Type of document (REQUERIMIENTOS, PDD, HISTORIAS_USUARIO)
        output_dir: Directory to save the document

    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)

    nombre = project_name.lower().replace(" ", "-").replace("_", "-")
    filename = f"{doc_type}-{nombre}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def load_document(filepath: str) -> str:
    """
    Load document content from file.

    Args:
        filepath: Path to the document

    Returns:
        Document content as string
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
