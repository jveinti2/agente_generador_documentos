# Generador de Documentos - LangGraph

Genera automáticamente Requerimientos, PDD e Historias de Usuario desde transcripciones de reuniones.

## Características

- Generación automática de 3 documentos: Requerimientos, PDD, Historias de Usuario
- Plantillas personalizables (.md)
- Exportación a Word (.docx) para compartir
- Chat RAG sobre documentos generados
- Interfaz web con Gradio

## Instalación

```bash
uv sync
cp .env.example .env
# Agregar OPENAI_API_KEY en .env
```

## Uso

```bash
uv run python gradio_app.py  # Interfaz web: http://localhost:7860
langgraph dev                # Studio visual para desarrollo
```

## Flujo de Trabajo

1. **Tab 1 - Cargar Transcripción**: Sube archivo .txt ’ Genera documentos ’ Descarga archivos .docx
2. **Tab 2 - Visualizar Documentos**: Ve el contenido markdown de los documentos
3. **Tab 3 - Plantillas**: Sube plantillas .md personalizadas (opcional)
4. **Tab 4 - Consultar Documentos**: Chat con los documentos generados usando RAG

## Archivos Generados

Los documentos se guardan en formato dual:

- `output/REQUERIMIENTOS-{nombre}.md` y `.docx`
- `output/PDD-{nombre}.md` y `.docx`
- `output/HISTORIAS_USUARIO-{nombre}.md` y `.docx`

Los archivos `.md` se usan para visualización interna, y los `.docx` están listos para descargar y compartir.

## Tecnologías

- **LangGraph**: Orquestación del workflow con patrón fan-out/fan-in
- **OpenAI GPT-4o**: Generación de documentos basada en plantillas
- **Gradio**: Interfaz web interactiva
- **python-docx**: Conversión Markdown ’ Word
- **InMemoryVectorStore**: RAG para consultas sobre documentos
