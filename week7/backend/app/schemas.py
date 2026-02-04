from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=1, max_length=10000, description="Note content")

    @field_validator('title', 'content')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Field cannot be empty or contain only whitespace')
        return v.strip()


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, description="Note title")
    content: str | None = Field(None, min_length=1, max_length=10000, description="Note content")

    @field_validator('title', 'content')
    @classmethod
    def validate_not_empty_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('Field cannot be empty or contain only whitespace')
        return v.strip() if v is not None else v


class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=1000, description="Action item description")

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Description cannot be empty or contain only whitespace')
        return v.strip()


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    # Task 2 增强字段
    note_id: int | None = None
    priority: str | None = None
    category: str | None = None
    assignee: str | None = None
    due_date: str | None = None

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = Field(None, min_length=1, max_length=1000, description="Action item description")
    completed: bool | None = Field(None, description="Completion status")

    @field_validator('description')
    @classmethod
    def validate_description_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('Description cannot be empty or contain only whitespace')
        return v.strip() if v is not None else v


# Search schemas
class SearchResult(BaseModel):
    """Combined search result for notes and action items."""
    notes: list[NoteRead] = []
    action_items: list[ActionItemRead] = []
    total_count: int = 0
    notes_count: int = 0
    action_items_count: int = 0


