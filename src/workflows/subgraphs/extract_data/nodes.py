"""Nodes for extract_data workflow."""

import json
import logging
from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.infrastructure.db import repositories as db
from src.shared.ids import new_id
from src.shared.timestamp import get_timestamp

from .state import ExtractDataState

logger = logging.getLogger(__name__)

# Sentinel value used in LLM prompts for criteria without user responses
NO_RESPONSE_SENTINEL = "No response provided"


class CriterionSummary(BaseModel):
    """Summary of user responses for a single criterion."""

    criterion: str
    summary: str


class ExtractionResult(BaseModel):
    """Structured extraction result from LLM."""

    summaries: list[CriterionSummary]


async def load_area_data(state: ExtractDataState) -> dict:
    """Load area data including title, criteria, and messages."""
    area_id = state.area_id

    area = db.LifeAreaManager.get_by_id(area_id)
    if area is None:
        logger.warning("Area not found for extraction", extra={"area_id": str(area_id)})
        return {"success": False}

    criteria = db.CriteriaManager.list_by_area(area_id)
    messages = db.LifeAreaMessagesManager.list_by_area(area_id)

    logger.info(
        "Loaded area data for extraction",
        extra={
            "area_id": str(area_id),
            "criteria_count": len(criteria),
            "message_count": len(messages),
        },
    )

    return {
        "area_title": area.title,
        "criteria_titles": [c.title for c in criteria],
        "messages": [m.data for m in messages],
    }


async def extract_summaries(state: ExtractDataState, llm: ChatOpenAI) -> dict:
    """Use LLM to extract and summarize user responses for each criterion.

    Note: The check for empty criteria/messages is handled by the router,
    so this function assumes valid data is present.
    """
    system_prompt = (
        "You are an interview data extraction agent.\n"
        "Your task is to summarize what the user said about each criterion.\n\n"
        "Rules:\n"
        "- For each criterion, extract a concise summary of the user's responses\n"
        "- Focus on facts and specific details the user shared\n"
        f"- If a criterion has no relevant responses, set summary to '{NO_RESPONSE_SENTINEL}'\n"
        "- Keep summaries brief but informative (1-3 sentences)\n"
    )

    user_prompt = {
        "area": state.area_title,
        "criteria": state.criteria_titles,
        "interview_messages": state.messages,
    }

    structured_llm = llm.with_structured_output(ExtractionResult)

    try:
        result = await structured_llm.ainvoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)},
            ]
        )

        if not isinstance(result, ExtractionResult):
            result = ExtractionResult.model_validate(result)

        extracted = {s.criterion: s.summary for s in result.summaries}

        logger.info(
            "Extracted summaries",
            extra={
                "area_id": str(state.area_id),
                "criteria_extracted": len(extracted),
            },
        )

        return {"extracted_summary": extracted, "success": True}

    except Exception:
        logger.exception(
            "Failed to extract summaries", extra={"area_id": str(state.area_id)}
        )
        return {"success": False}


async def save_extracted_data(state: ExtractDataState) -> dict:
    """Save extracted data to the database (deprecated, kept for compatibility).

    Note: This function is deprecated. Use save_summary instead.
    The success/summary check is now handled by the router.
    """
    data_id = new_id()
    extracted = db.ExtractedData(
        id=data_id,
        area_id=state.area_id,
        data=json.dumps(state.extracted_summary),
        created_ts=get_timestamp(),
    )
    db.ExtractedDataManager.create(data_id, extracted)

    logger.info(
        "Saved extracted data",
        extra={
            "area_id": str(state.area_id),
            "data_id": str(data_id),
        },
    )

    return {}


def _build_summary_content(extracted_summary: dict[str, str]) -> str:
    """Combine extracted summaries into a single text for embedding."""
    parts = []
    for criterion, summary in extracted_summary.items():
        if summary and summary != NO_RESPONSE_SENTINEL:
            parts.append(f"{criterion}: {summary}")
    return "\n".join(parts)


async def save_summary(state: ExtractDataState) -> dict:
    """Save summary with embedding to area_summaries table.

    This node:
    1. Combines extracted summaries into a single content string
    2. Generates an embedding vector for the content
    3. Saves to area_summaries table

    Note: The success check is handled by the router before this node.
    """
    from src.infrastructure.embeddings import get_embedding_client

    summary_content = _build_summary_content(state.extracted_summary)

    if not summary_content:
        logger.info(
            "Skipping summary save - no meaningful content",
            extra={"area_id": str(state.area_id)},
        )
        return {"summary_content": ""}

    embed_client = get_embedding_client()
    embedding = await embed_client.aembed_query(summary_content)

    summary_id = new_id()
    area_summary = db.AreaSummary(
        id=summary_id,
        area_id=state.area_id,
        content=summary_content,
        vector=embedding,
        created_ts=get_timestamp(),
    )
    db.AreaSummariesManager.create(summary_id, area_summary)

    logger.info(
        "Saved area summary with embedding",
        extra={
            "area_id": str(state.area_id),
            "summary_id": str(summary_id),
            "content_length": len(summary_content),
        },
    )

    return {"summary_content": summary_content}


class KnowledgeItem(BaseModel):
    """A single piece of extracted knowledge."""

    content: str = Field(description="The skill or fact description")
    kind: Literal["skill", "fact"] = Field(
        description="Type of knowledge: 'skill' for abilities/competencies, 'fact' for other information"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score based on how explicitly stated"
    )


class KnowledgeExtractionResult(BaseModel):
    """Result of knowledge extraction from a summary."""

    items: list[KnowledgeItem] = Field(
        default_factory=list, description="List of extracted knowledge items"
    )


async def extract_knowledge(state: ExtractDataState, llm: ChatOpenAI) -> dict:
    """Extract skills and facts from the summary content using LLM.

    This node uses structured output to extract:
    - Skills: abilities, competencies, tools, technologies
    - Facts: employment, education, preferences, experiences, relationships
    """
    if not state.summary_content:
        logger.info(
            "Skipping knowledge extraction - no summary content",
            extra={"area_id": str(state.area_id)},
        )
        return {"extracted_knowledge": []}

    system_prompt = (
        "You are a knowledge extraction agent.\n"
        "Your task is to extract discrete pieces of knowledge about the user "
        "from interview summaries.\n\n"
        "Extract two types of knowledge:\n"
        "1. SKILLS: Abilities, competencies, tools, technologies, languages, "
        "methodologies the user knows or is learning.\n"
        "   Examples: 'Python programming', 'project management', 'Spanish language'\n\n"
        "2. FACTS: Concrete information about the user's life.\n"
        "   Examples: 'Works at Google', 'Has 5 years experience', "
        "'Lives in San Francisco', 'Prefers remote work'\n\n"
        "Rules:\n"
        "- Be specific: 'Python backend development' not just 'programming'\n"
        "- Extract only what is clearly stated or strongly implied\n"
        "- Set confidence based on how explicitly the information was stated:\n"
        "  - 1.0: Directly stated ('I work at Google')\n"
        "  - 0.7-0.9: Strongly implied or mostly clear\n"
        "  - 0.5-0.7: Inferred but less certain\n"
        "- Do not invent or assume information not present in the summary\n"
    )

    user_prompt = {
        "area": state.area_title,
        "summary": state.summary_content,
    }

    structured_llm = llm.with_structured_output(KnowledgeExtractionResult)

    try:
        result = await structured_llm.ainvoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)},
            ]
        )

        if not isinstance(result, KnowledgeExtractionResult):
            result = KnowledgeExtractionResult.model_validate(result)

        extracted = [item.model_dump() for item in result.items]

        logger.info(
            "Extracted knowledge items",
            extra={
                "area_id": str(state.area_id),
                "items_count": len(extracted),
            },
        )

        return {"extracted_knowledge": extracted}

    except Exception:
        logger.exception(
            "Failed to extract knowledge", extra={"area_id": str(state.area_id)}
        )
        return {"extracted_knowledge": []}


async def save_knowledge(state: ExtractDataState) -> dict:
    """Save extracted knowledge items to database.

    This node:
    1. For each extracted item, saves to user_knowledge table
    2. Links knowledge to user and area via user_knowledge_areas table

    Note: Duplicate detection is not implemented yet - each extraction
    creates new records. Future versions may implement fuzzy matching.
    """
    from src.infrastructure.db.connection import get_connection

    if not state.extracted_knowledge or not state.user_id:
        logger.info(
            "Skipping knowledge save - no knowledge or user_id",
            extra={
                "area_id": str(state.area_id),
                "has_user_id": state.user_id is not None,
                "knowledge_count": len(state.extracted_knowledge),
            },
        )
        return {}

    saved_count = 0
    with get_connection() as conn:
        for item in state.extracted_knowledge:
            knowledge_id = new_id()
            knowledge = db.UserKnowledge(
                id=knowledge_id,
                content=item["content"],
                kind=item["kind"],
                confidence=item["confidence"],
                created_ts=get_timestamp(),
            )
            db.UserKnowledgeManager.create(
                knowledge_id, knowledge, conn, auto_commit=False
            )

            link = db.UserKnowledgeArea(
                user_id=state.user_id,
                knowledge_id=knowledge_id,
                area_id=state.area_id,
            )
            db.UserKnowledgeAreasManager.create_link(link, conn, auto_commit=False)
            saved_count += 1
        conn.commit()

    logger.info(
        "Saved knowledge items",
        extra={
            "area_id": str(state.area_id),
            "user_id": str(state.user_id),
            "saved_count": saved_count,
        },
    )

    return {}
