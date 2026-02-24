from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, Tag
from ..schemas import NoteReadWithTags, TagCreate, TagPatch, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagRead])
def list_tags(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[TagRead]:
    """List all tags with optional filtering and sorting."""
    stmt = select(Tag)
    if q:
        stmt = stmt.where(Tag.name.contains(q))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Tag, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Tag, sort_field)))
    else:
        stmt = stmt.order_by(desc(Tag.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [TagRead.model_validate(row) for row in rows]


@router.post("/", response_model=TagRead, status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    """Create a new tag."""
    # Check if tag with same name already exists
    existing_tag = db.execute(select(Tag).where(Tag.name == payload.name)).scalar_one_or_none()
    if existing_tag:
        raise HTTPException(status_code=400, detail=f"Tag with name '{payload.name}' already exists")
    
    tag = Tag(name=payload.name, color=payload.color)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    
    return TagRead.model_validate(tag)


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagRead:
    """Get a specific tag by ID."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    return TagRead.model_validate(tag)


@router.patch("/{tag_id}", response_model=TagRead)
def patch_tag(tag_id: int, payload: TagPatch, db: Session = Depends(get_db)) -> TagRead:
    """Update specific fields of a tag."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    if payload.name is not None:
        # Check if another tag with same name exists
        existing_tag = db.execute(
            select(Tag).where(Tag.name == payload.name, Tag.id != tag_id)
        ).scalar_one_or_none()
        if existing_tag:
            raise HTTPException(status_code=400, detail=f"Tag with name '{payload.name}' already exists")
        tag.name = payload.name
    
    if payload.color is not None:
        tag.color = payload.color
    
    db.commit()
    db.refresh(tag)
    
    return TagRead.model_validate(tag)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a tag."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()


@router.get("/{tag_id}/notes", response_model=list[NoteReadWithTags])
def get_notes_by_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(50, le=200),
) -> list[NoteReadWithTags]:
    """Get all notes associated with a specific tag."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Get notes with this tag
    stmt = select(Note).join(Note.tags).where(Tag.id == tag_id).offset(skip).limit(limit)
    notes = db.execute(stmt).scalars().all()
    
    return [NoteReadWithTags.model_validate(note) for note in notes]


@router.post("/{tag_id}/notes/{note_id}", status_code=204)
def add_tag_to_note(tag_id: int, note_id: int, db: Session = Depends(get_db)) -> None:
    """Add a tag to a note (create association)."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    if note_id <= 0:
        raise HTTPException(status_code=400, detail="Note ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check if association already exists
    if tag in note.tags:
        raise HTTPException(status_code=400, detail="Tag is already associated with this note")
    
    note.tags.append(tag)
    db.commit()


@router.delete("/{tag_id}/notes/{note_id}", status_code=204)
def remove_tag_from_note(tag_id: int, note_id: int, db: Session = Depends(get_db)) -> None:
    """Remove a tag from a note (delete association)."""
    if tag_id <= 0:
        raise HTTPException(status_code=400, detail="Tag ID must be a positive integer")
    if note_id <= 0:
        raise HTTPException(status_code=400, detail="Note ID must be a positive integer")
    
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check if association exists
    if tag not in note.tags:
        raise HTTPException(status_code=400, detail="Tag is not associated with this note")
    
    note.tags.remove(tag)
    db.commit()
