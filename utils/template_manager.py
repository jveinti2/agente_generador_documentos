import os
from pathlib import Path


class TemplateManager:
    def __init__(self, templates_dir: str = "./templates"):
        self.templates_dir = templates_dir
        os.makedirs(templates_dir, exist_ok=True)

    def save_template(self, session_id: str, doc_type: str, content: str) -> str:
        session_dir = os.path.join(self.templates_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)

        if not content.strip():
            raise ValueError("Template content cannot be empty")

        filename = f"{doc_type}.md"
        filepath = os.path.join(session_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def load_template(self, session_id: str, doc_type: str) -> str:
        filepath = os.path.join(self.templates_dir, session_id, f"{doc_type}.md")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()

        default_filepath = os.path.join(self.templates_dir, "default", f"{doc_type}.md")
        if os.path.exists(default_filepath):
            with open(default_filepath, "r", encoding="utf-8") as f:
                return f.read()

        return self._get_builtin_template(doc_type)

    def _get_builtin_template(self, doc_type: str) -> str:
        templates = {
            "REQUERIMIENTOS": """# Documento de Requerimientos

## Requerimientos Funcionales
### RF-001: [Título]
**Prioridad**: Alta
**Descripción**: [Descripción]
**Criterios de Aceptación**:
- Criterio 1

## Requerimientos No Funcionales
### RNF-001: [Categoría]
**Descripción**: [Descripción]
**Métricas**: [Métricas]""",

            "PDD": """# Documento de Diseño de Producto

## Resumen Ejecutivo
[Descripción del producto]

## Planteamiento del Problema
[Problema a resolver]

## Objetivos
- Objetivo 1

## Características Principales
- Característica 1

## Métricas de Éxito
- Métrica 1""",

            "HISTORIAS_USUARIO": """# Historias de Usuario

**Épica**: [Nombre de la épica]

## Historias

### HU-001
**Como** [rol]
**Quiero** [acción]
**Para** [beneficio]

**Puntos de Historia**: 5

**Criterios de Aceptación**:
- Criterio 1"""
        }
        return templates.get(doc_type, "# Documento sin plantilla")

    def has_templates(self, session_id: str) -> dict[str, bool]:
        doc_types = ["REQUERIMIENTOS", "PDD", "HISTORIAS_USUARIO"]
        return {
            doc_type: os.path.exists(os.path.join(self.templates_dir, session_id, f"{doc_type}.md"))
            for doc_type in doc_types
        }
