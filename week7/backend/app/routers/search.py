from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import SearchResult, NoteRead, ActionItemRead

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=SearchResult)
def search_all(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    db: Session = Depends(get_db),
    limit: int = Query(50, le=200, description="Maximum results per type")
) -> SearchResult:
    """Search across notes and action items."""
    # Search notes
    notes_stmt = select(Note).where(
        or_(
            Note.title.icontains(q),
            Note.content.icontains(q)
        )
    ).limit(limit)
    
    notes = db.execute(notes_stmt).scalars().all()
    notes_data = [NoteRead.model_validate(note) for note in notes]
    
    # Search action items
    action_items_stmt = select(ActionItem).where(
        ActionItem.description.icontains(q)
    ).limit(limit)
    
    action_items = db.execute(action_items_stmt).scalars().all()
    action_items_data = [ActionItemRead.model_validate(item) for item in action_items]
    
    return SearchResult(
        notes=notes_data,
        action_items=action_items_data,
        total_count=len(notes_data) + len(action_items_data),
        notes_count=len(notes_data),
        action_items_count=len(action_items_data)
    )


@router.get("/notes", response_model=list[NoteRead])
def search_notes(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    db: Session = Depends(get_db),
    limit: int = Query(50, le=200),
    in_title: bool = Query(True, description="Search in title"),
    in_content: bool = Query(True, description="Search in content")
) -> list[NoteRead]:
    """Search notes with detailed filtering options."""
    conditions = []
    
    if in_title:
        conditions.append(Note.title.icontains(q))
    
    if in_content:
        conditions.append(Note.content.icontains(q))
    
    if not conditions:
        # If both are disabled, search in both
        conditions = [Note.title.icontains(q), Note.content.icontains(q)]
    
    stmt = select(Note).where(or_(*conditions)).limit(limit)
    notes = db.execute(stmt).scalars().all()
    
    return [NoteRead.model_validate(note) for note in notes]


@router.get("/action-items", response_model=list[ActionItemRead])
def search_action_items(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    db: Session = Depends(get_db),
    limit: int = Query(50, le=200),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
) -> list[ActionItemRead]:
    """Search action items with completion filtering."""
    stmt = select(ActionItem).where(ActionItem.description.icontains(q))
    
    if completed is not None:
        stmt = stmt.where(ActionItem.completed == completed)
    
    stmt = stmt.limit(limit)
    action_items = db.execute(stmt).scalars().all()
    
    return [ActionItemRead.model_validate(item) for item in action_items]