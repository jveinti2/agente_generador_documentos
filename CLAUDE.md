# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-document generator from conversation transcripts using LangGraph. Generates Requirements (functional/non-functional), Product Design Documents (PDD), and User Stories from meeting transcripts.

## Development Commands

**Setup:**
- `uv sync` - Install/sync dependencies from pyproject.toml
- `cp .env.example .env` - Create environment file and add your OPENAI_API_KEY

**Running the Application:**
- `uv run python gradio_app.py` - Start Gradio interface (defaults to http://0.0.0.0:8000)
- `uv run python main.py` - Run standalone example with hardcoded transcript
- `langgraph dev` - Start LangGraph Studio for visual debugging (requires LangSmith configured)

**Gradio Interface:**
- Tab 1 (Cargar Transcripción): Upload transcript (.txt), generate documents, download .docx files
- Tab 2 (Visualizar Documentos): View generated markdown content in-app
- Tab 3 (Plantillas): Upload custom .md templates (REQUERIMIENTOS, PDD, HISTORIAS_USUARIO)
- Tab 4 (Consultar Documentos): RAG chat interface to query generated documents

## Architecture

**Project Structure:**
```
├── main.py                    # LangGraph workflow definition
├── gradio_app.py              # Gradio web interface
├── nodes/                     # Graph nodes
│   ├── analyze_transcript.py # Extract key info from transcript
│   ├── generate_requirements.py  # Template-based generation
│   ├── generate_pdd.py
│   ├── generate_user_stories.py
│   └── index_documents.py    # Vector store indexing
├── utils/                     # Utilities
│   ├── file_manager.py       # Save/load markdown documents (Spanish naming)
│   ├── vector_store.py       # InMemoryVectorStore manager
│   └── template_manager.py   # Manage user-uploaded templates
├── templates/                 # User templates (session-based storage)
└── output/                    # Generated markdown documents (TIPO-nombre.md)
```

**Workflow (LangGraph):**
1. `analyze_transcript` - Extracts project info, topics, stakeholders using structured output (TranscriptAnalysis)
2. Parallel generation (fan-out):
   - `generate_requirements` - Generates functional/non-functional requirements
   - `generate_pdd` - Generates product design document
   - `generate_user_stories` - Generates epics and user stories
3. Fan-in to `index_documents` - Saves .md/.docx files, chunks content, indexes in vector store for RAG

**Tech Stack:**
- LangGraph for orchestration (StateGraph with MemorySaver checkpointer)
- OpenAI GPT-4o for LLM generation (via ChatOpenAI)
- Template-based generation: TemplateManager loads user/default/builtin templates, LLM follows structure
- python-docx for markdown → Word conversion
- InMemoryVectorStore (LangChain) for RAG with RecursiveCharacterTextSplitter
- Gradio for web interface

**Key Architectural Decisions:**
- Dual checkpointer setup: main.py exports `agent` without checkpointer (for langgraph dev), `get_agent_with_checkpointer()` for standalone/Gradio use
- Session-based templates: Each Gradio session gets unique UUID, templates stored in `templates/{session_id}/`
- Dual file format: .md for in-app viewing, .docx for downloads/sharing
- AgentState uses `Annotated[list[str], add]` for document_paths to accumulate results from parallel nodes

**File Naming Convention:**
- `REQUERIMIENTOS-{nombre}.md` and `.docx` - Requirements document
- `PDD-{nombre}.md` and `.docx` - Product Design Document
- `HISTORIAS_USUARIO-{nombre}.md` and `.docx` - User Stories document
- Project name normalized: lowercase, spaces/underscores → hyphens

## Environment Setup

Required in `.env`:
- `OPENAI_API_KEY` - OpenAI API key

Optional (LangSmith tracing):
- `LANGSMITH_API_KEY`
- `LANGSMITH_TRACING=true`
- `LANGSMITH_PROJECT=agente-generador-documentos`
