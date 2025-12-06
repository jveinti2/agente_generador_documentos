# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-document generator from conversation transcripts using LangGraph. Generates Requirements (functional/non-functional), Product Design Documents (PDD), and User Stories from meeting transcripts.

## Development Commands

**Setup:**
- `uv sync` - Install/sync dependencies from pyproject.toml
- `cp .env.example .env` - Create environment file and add your OPENAI_API_KEY

**Running the Application:**
- `uv run python gradio_app.py` - Start Gradio interface on http://localhost:7860
- `langgraph dev` - Start LangGraph Studio for visual debugging (development with LangSmith)

**Gradio Interface:**
- Tab 1: Upload transcript (.txt) and generate documents
- Tab 2: Upload/manage templates (.md files for each document type)
- Tab 3: Chat playground to query generated documents with RAG (shows sources)

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

**Workflow:**
1. `analyze_transcript` - Extracts project info, topics, stakeholders
2. Parallel generation of 3 documents using template-based prompts
3. `index_documents` - Chunks and indexes documents for RAG

**Tech Stack:**
- LangGraph for orchestration (parallel fan-out/fan-in pattern)
- Template-based generation (user uploads .md templates, LLM follows structure)
- OpenAI GPT-4o for generation
- InMemoryVectorStore for RAG Q&A
- Gradio for web interface

**File Naming Convention:**
- `REQUERIMIENTOS-{nombre}.md` - Requirements document
- `PDD-{nombre}.md` - Product Design Document
- `HISTORIAS_USUARIO-{nombre}.md` - User Stories document

## Environment Setup

Required in `.env`:
- `OPENAI_API_KEY` - OpenAI API key

Optional (LangSmith tracing):
- `LANGSMITH_API_KEY`
- `LANGSMITH_TRACING=true`
- `LANGSMITH_PROJECT=agente-generador-documentos`
