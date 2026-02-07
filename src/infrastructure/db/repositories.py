"""Repository facade - re-exports all database models and managers.

This module provides backward-compatible imports for all database entities.
"""

# Domain Models
# Area Data Managers
from .area_data_managers import (
    AreaSummariesManager,
    ExtractedDataManager,
    LifeAreaMessagesManager,
)

# Core Managers
from .core_managers import (
    CriteriaManager,
    HistoryManager,
    LifeAreaManager,
    UsersManager,
)

# Knowledge Managers
from .knowledge_managers import (
    UserKnowledgeAreasManager,
    UserKnowledgeManager,
)
from .models import (
    AreaSummary,
    Criteria,
    ExtractedData,
    History,
    LifeArea,
    LifeAreaMessage,
    User,
    UserKnowledge,
    UserKnowledgeArea,
)

__all__ = [
    # Models
    "AreaSummary",
    "Criteria",
    "ExtractedData",
    "History",
    "LifeArea",
    "LifeAreaMessage",
    "User",
    "UserKnowledge",
    "UserKnowledgeArea",
    # Managers
    "AreaSummariesManager",
    "CriteriaManager",
    "ExtractedDataManager",
    "HistoryManager",
    "LifeAreaManager",
    "LifeAreaMessagesManager",
    "UserKnowledgeAreasManager",
    "UserKnowledgeManager",
    "UsersManager",
]
