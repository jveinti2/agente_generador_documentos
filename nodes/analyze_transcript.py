from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import TypedDict


class TranscriptAnalysis(BaseModel):
    """Structured analysis of a conversation transcript"""
    project_name: str = Field(description="Name of the project discussed")
    key_topics: list[str] = Field(description="Main topics discussed")
    stakeholders: list[str] = Field(description="Key stakeholders mentioned")
    main_requirements: list[str] = Field(description="High-level requirements identified")
    goals: list[str] = Field(description="Project goals and objectives")


class AgentState(TypedDict):
    transcript: str
    analysis: dict
    requirements_doc: str
    pdd_doc: str
    user_stories_doc: str
    document_paths: list[str]
    indexed: bool


def analyze_transcript_node(state: AgentState) -> dict:
    """
    Analyze the conversation transcript to extract key information.

    Args:
        state: Current agent state with transcript

    Returns:
        Updated state with analysis
    """
    transcript = state["transcript"]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(TranscriptAnalysis)

    system_prompt = """You are an expert business analyst. Analyze the conversation transcript and extract:
    - The project name
    - Key topics discussed
    - Stakeholders involved
    - Main requirements identified
    - Project goals and objectives

    Be thorough and precise in your analysis."""

    result = structured_llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this conversation transcript:\n\n{transcript}"}
    ])

    return {
        "analysis": result.model_dump()
    }
