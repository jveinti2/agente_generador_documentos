import gradio as gr
from main import get_agent_with_checkpointer
from utils.template_manager import TemplateManager
from utils.vector_store import get_vector_store
from langchain_openai import ChatOpenAI
import uuid
import os

agent = get_agent_with_checkpointer()
template_manager = TemplateManager()


def upload_template(template_file, doc_type, session_id):
    if template_file is None:
        return "No se ha cargado ningún archivo"

    try:
        with open(template_file.name, 'r', encoding='utf-8') as f:
            content = f.read()

        template_manager.save_template(session_id, doc_type, content)
        return f"✓ Plantilla {doc_type} cargada exitosamente"
    except Exception as e:
        return f"Error: {str(e)}"


def generate_documents_with_content(transcript_file, session_id):
    if transcript_file is None:
        return (
            "Error: Debes cargar un archivo .txt",
            None, None, None, None, [],
            "", "", ""
        )

    try:
        with open(transcript_file.name, 'r', encoding='utf-8') as f:
            transcript = f.read()

        result = agent.invoke(
            {"transcript": transcript, "session_id": session_id},
            config={"configurable": {"thread_id": str(uuid.uuid4())}}
        )

        paths_md = result['document_paths']
        paths_docx = result['document_paths_docx']
        project_name = result['analysis']['project_name']

        return (
            "✓ Documentos generados exitosamente",
            paths_docx[0] if len(paths_docx) > 0 else None,
            paths_docx[1] if len(paths_docx) > 1 else None,
            paths_docx[2] if len(paths_docx) > 2 else None,
            project_name,
            paths_md,
            result['requirements_doc'],
            result['pdd_doc'],
            result['user_stories_doc']
        )
    except Exception as e:
        return (
            f"Error al generar documentos: {str(e)}",
            None, None, None, None, [],
            "", "", ""
        )


def view_document(selection, req, pdd, stories):
    if selection == "Requerimientos":
        return req if req else "No hay contenido disponible. Genera documentos primero en la pestaña 'Cargar Transcripción'."
    elif selection == "PDD":
        return pdd if pdd else "No hay contenido disponible. Genera documentos primero en la pestaña 'Cargar Transcripción'."
    else:
        return stories if stories else "No hay contenido disponible. Genera documentos primero en la pestaña 'Cargar Transcripción'."


def chat_fn(message, history):
    try:
        vector_store = get_vector_store()

        docs = vector_store.similarity_search(message, k=4)

        if not docs:
            return "No hay documentos indexados. Genera documentos primero en la pestaña 'Cargar Transcripción'."

        context = "\n\n".join([doc.page_content for doc in docs])

        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        response = llm.invoke([
            {"role": "system", "content": f"Contexto:\n{context}"},
            {"role": "user", "content": message}
        ])

        return response.content
    except Exception as e:
        return f"Error: {str(e)}"


def create_interface():
    with gr.Blocks(title="Generador de Documentos") as interface:
        gr.Markdown("# Generador de Documentos desde Transcripciones")

        session_id = gr.State(lambda: str(uuid.uuid4()))
        project_name = gr.State(None)
        doc_paths = gr.State([])

        req_content = gr.State("")
        pdd_content = gr.State("")
        stories_content = gr.State("")

        with gr.Tabs():
            with gr.Tab("1. Cargar Transcripción"):
                gr.Markdown("### Genera documentos desde una transcripción")

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("#### Cargar Archivo")
                        transcript_file = gr.File(
                            label="Subir transcripción (.txt)",
                            file_types=[".txt"]
                        )
                        generate_btn = gr.Button(
                            "Generar Documentos",
                            variant="primary",
                            size="lg"
                        )
                        status_output = gr.Textbox(
                            label="Estado",
                            interactive=False
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("#### Documentos Generados")
                        req_download = gr.File(
                            label="📄 Descargar Requerimientos",
                            interactive=False
                        )
                        pdd_download = gr.File(
                            label="📄 Descargar PDD",
                            interactive=False
                        )
                        stories_download = gr.File(
                            label="📄 Descargar Historias de Usuario",
                            interactive=False
                        )

                generate_btn.click(
                    fn=generate_documents_with_content,
                    inputs=[transcript_file, session_id],
                    outputs=[
                        status_output,
                        req_download, pdd_download, stories_download,
                        project_name, doc_paths,
                        req_content, pdd_content, stories_content
                    ]
                )

            with gr.Tab("2. Visualizar Documentos"):
                gr.Markdown("### Ver contenido de documentos generados")

                doc_selector = gr.Radio(
                    choices=["Requerimientos", "PDD", "Historias de Usuario"],
                    value="Requerimientos",
                    label="Seleccionar documento"
                )

                doc_viewer = gr.Markdown(
                    label="Contenido",
                    value="Genera documentos primero en la pestaña 'Cargar Transcripción'"
                )

                doc_selector.change(
                    fn=view_document,
                    inputs=[doc_selector, req_content, pdd_content, stories_content],
                    outputs=[doc_viewer]
                )

            with gr.Tab("3. Plantillas"):
                gr.Markdown("### Gestionar Plantillas de Documentos")
                gr.Markdown("Sube las 3 plantillas en formato .md que servirán como referencia para generar los documentos")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### Plantilla Requerimientos")
                        req_template = gr.File(label="Archivo .md", file_types=[".md"])
                        req_status = gr.Textbox(label="Estado", interactive=False, value="Pendiente")

                    with gr.Column():
                        gr.Markdown("#### Plantilla PDD")
                        pdd_template = gr.File(label="Archivo .md", file_types=[".md"])
                        pdd_status = gr.Textbox(label="Estado", interactive=False, value="Pendiente")

                    with gr.Column():
                        gr.Markdown("#### Plantilla Historias de Usuario")
                        stories_template = gr.File(label="Archivo .md", file_types=[".md"])
                        stories_status = gr.Textbox(label="Estado", interactive=False, value="Pendiente")

                req_template.upload(
                    fn=lambda f, s: upload_template(f, "REQUERIMIENTOS", s),
                    inputs=[req_template, session_id],
                    outputs=[req_status]
                )

                pdd_template.upload(
                    fn=lambda f, s: upload_template(f, "PDD", s),
                    inputs=[pdd_template, session_id],
                    outputs=[pdd_status]
                )

                stories_template.upload(
                    fn=lambda f, s: upload_template(f, "HISTORIAS_USUARIO", s),
                    inputs=[stories_template, session_id],
                    outputs=[stories_status]
                )

            with gr.Tab("4. Consultar Documentos"):
                gr.Markdown("### Chat con tus documentos generados")
                gr.Markdown("Haz preguntas sobre los documentos generados.")

                gr.ChatInterface(
                    fn=chat_fn,
                    chatbot=gr.Chatbot(height=400),
                    textbox=gr.Textbox(placeholder="¿Qué requiere el sistema?", scale=4)
                )

    return interface


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=8000)
