from langchain_openai import ChatOpenAI
from utils.file_manager import save_markdown_document
from utils.template_manager import TemplateManager
from typing import TypedDict

template_manager = TemplateManager()


class AgentState(TypedDict):
    transcript: str
    session_id: str
    analysis: dict
    requirements_doc: str
    pdd_doc: str
    user_stories_doc: str
    document_paths: list[str]
    indexed: bool


def generate_requirements_node(state: AgentState) -> dict:
    """
    Generate Requirements document from transcript and analysis using template.

    Args:
        state: Current agent state

    Returns:
        Updated state with requirements document
    """
    transcript = state["transcript"]
    analysis = state["analysis"]
    session_id = state["session_id"]

    template_content = template_manager.load_template(session_id, "REQUERIMIENTOS")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    system_prompt = f"""Eres un ingeniero de requerimientos experto.
Genera un documento de Requerimientos siguiendo EXACTAMENTE la estructura de esta plantilla:

--- PLANTILLA ---
{template_content}
--- FIN PLANTILLA ---

Usa la misma estructura, formato markdown y estilo.
Genera contenido basado en el análisis proporcionado."""

    context = f"""
Transcripción:
{transcript}

Análisis:
- Proyecto: {analysis['project_name']}
- Temas clave: {', '.join(analysis['key_topics'])}
- Stakeholders: {', '.join(analysis['stakeholders'])}
- Requerimientos: {', '.join(analysis['main_requirements'])}
- Objetivos: {', '.join(analysis['goals'])}
"""

    result = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Genera el documento:\n{context}"}
    ])

    markdown_content = result.content

    filepath = save_markdown_document(
        content=markdown_content,
        project_name=analysis['project_name'],
        doc_type="REQUERIMIENTOS"
    )

    return {
        "requirements_doc": markdown_content,
        "document_paths": [filepath]
    }
