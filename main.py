import os
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from nodes import (
    analyze_transcript_node,
    generate_requirements_node,
    generate_pdd_node,
    generate_user_stories_node,
    index_documents_node
)

load_dotenv()


class AgentState(TypedDict):
    transcript: str
    session_id: str
    analysis: dict
    requirements_doc: str
    pdd_doc: str
    user_stories_doc: str
    document_paths: Annotated[list[str], add]
    document_paths_docx: Annotated[list[str], add]
    indexed: bool


def create_workflow(use_checkpointer: bool = True):
    """
    Create and compile the document generation workflow.

    Args:
        use_checkpointer: If True, uses MemorySaver for persistence.
                         If False, compiles without checkpointer (for langgraph dev).
    """

    workflow = StateGraph(AgentState)

    workflow.add_node("analyze_transcript", analyze_transcript_node)
    workflow.add_node("generate_requirements", generate_requirements_node)
    workflow.add_node("generate_pdd", generate_pdd_node)
    workflow.add_node("generate_user_stories", generate_user_stories_node)
    workflow.add_node("index_documents", index_documents_node)

    workflow.add_edge(START, "analyze_transcript")

    workflow.add_edge("analyze_transcript", "generate_requirements")
    workflow.add_edge("analyze_transcript", "generate_pdd")
    workflow.add_edge("analyze_transcript", "generate_user_stories")

    workflow.add_edge("generate_requirements", "index_documents")
    workflow.add_edge("generate_pdd", "index_documents")
    workflow.add_edge("generate_user_stories", "index_documents")

    workflow.add_edge("index_documents", END)

    if use_checkpointer:
        checkpointer = MemorySaver()
        return workflow.compile(checkpointer=checkpointer)
    else:
        return workflow.compile()


# Agent for langgraph dev (without checkpointer - platform handles persistence)
agent = create_workflow(use_checkpointer=False)


def get_agent_with_checkpointer():
    """Get agent with MemorySaver checkpointer for standalone use (FastAPI, python main.py)"""
    return create_workflow(use_checkpointer=True)


def main():
    """Example usage of the document generation agent"""
    sample_transcript = """
    En nuestra reunión de hoy discutimos el desarrollo de una nueva plataforma de e-commerce.
    El proyecto se llamará "ShopFast" y tiene como objetivo crear un marketplace donde vendedores
    puedan listar sus productos y compradores puedan adquirirlos de forma segura.

    Participantes: Juan (Product Manager), María (Tech Lead), Carlos (UX Designer)

    Requerimientos principales:
    - Sistema de autenticación para vendedores y compradores
    - Catálogo de productos con búsqueda y filtros
    - Carrito de compras y proceso de checkout
    - Integración con pasarelas de pago (PayPal, Stripe)
    - Panel de administración para vendedores
    - Sistema de calificaciones y reviews
    - Notificaciones por email

    Objetivos:
    - Lanzar MVP en 3 meses
    - Soportar hasta 10,000 usuarios concurrentes
    - Garantizar seguridad en transacciones (PCI-DSS compliance)
    - Interfaz responsive para móvil y desktop
    """

    print("Generating documents from transcript...")
    print("=" * 60)

    # Use agent with checkpointer for standalone execution
    standalone_agent = get_agent_with_checkpointer()

    result = standalone_agent.invoke(
        {"transcript": sample_transcript, "session_id": "default"},
        config={"configurable": {"thread_id": "example-1"}}
    )

    print("\nDocuments generated successfully!")
    print(f"Project: {result['analysis']['project_name']}")
    print(f"\nGenerated documents:")
    for path in result['document_paths']:
        print(f"  - {path}")
    print(f"\nIndexed in vector store: {result['indexed']}")


if __name__ == "__main__":
    main()
