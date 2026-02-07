"""Pydantic argument models for area loop tools."""

from pydantic import BaseModel, Field


class ListLifeAreasArgs(BaseModel):
    """Arguments for listing life areas."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )


class GetLifeAreaArgs(BaseModel):
    """Arguments for getting a single life area."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    area_id: str = Field(..., description="UUID of the life area to fetch")


class CreateLifeAreaArgs(BaseModel):
    """Arguments for creating a life area."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    title: str = Field(..., description="Title/name for the new life area")
    parent_id: str | None = Field(
        None,
        description="Optional UUID of parent life area for hierarchical organization",
    )


class DeleteLifeAreaArgs(BaseModel):
    """Arguments for deleting a life area."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    area_id: str = Field(..., description="UUID of the life area to delete")


class ListCriteriaArgs(BaseModel):
    """Arguments for listing criteria."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    area_id: str = Field(
        ...,
        description="UUID of the life area. Use 'list_life_areas' first if you don't have the ID.",
    )


class CreateCriteriaArgs(BaseModel):
    """Arguments for creating a criteria item."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    area_id: str = Field(
        ...,
        description="UUID of the life area. Call 'list_life_areas' to get available area IDs, then extract the 'id' field from the response.",
    )
    title: str = Field(..., description="Title/name for the new criteria item")


class DeleteCriteriaArgs(BaseModel):
    """Arguments for deleting a criteria item."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    criteria_id: str = Field(..., description="UUID of the criteria item to delete")


class SetCurrentAreaArgs(BaseModel):
    """Arguments for setting the current area for interview."""

    user_id: str = Field(
        ..., description="UUID of the user (provided in system message)"
    )
    area_id: str = Field(
        ...,
        description="UUID of the life area to set as current for interview",
    )
