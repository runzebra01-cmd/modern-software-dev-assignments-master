from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def get_statistics(db: Session = Depends(get_db)) -> dict:
    """Get general statistics about the application."""
    # Count total notes
    total_notes = db.scalar(select(func.count(Note.id))) or 0
    
    # Count total action items
    total_action_items = db.scalar(select(func.count(ActionItem.id))) or 0
    
    # Count completed action items
    completed_action_items = db.scalar(
        select(func.count(ActionItem.id)).where(ActionItem.completed == True)
    ) or 0
    
    # Count pending action items
    pending_action_items = total_action_items - completed_action_items
    
    # Calculate completion percentage
    completion_percentage = (
        round((completed_action_items / total_action_items) * 100, 2)
        if total_action_items > 0
        else 0.0
    )
    
    return {
        "notes": {
            "total": total_notes
        },
        "action_items": {
            "total": total_action_items,
            "completed": completed_action_items,
            "pending": pending_action_items,
            "completion_percentage": completion_percentage
        }
    }


@router.get("/action-items")
def get_action_item_stats(db: Session = Depends(get_db)) -> dict:
    """Get detailed statistics about action items."""
    # Get completed vs pending counts
    completed_count = db.scalar(
        select(func.count(ActionItem.id)).where(ActionItem.completed == True)
    ) or 0
    
    pending_count = db.scalar(
        select(func.count(ActionItem.id)).where(ActionItem.completed == False)
    ) or 0
    
    # Get average description length
    avg_description_length = db.scalar(
        select(func.avg(func.length(ActionItem.description)))
    ) or 0.0
    
    return {
        "completed_count": completed_count,
        "pending_count": pending_count,
        "total_count": completed_count + pending_count,
        "completion_rate": round(
            (completed_count / (completed_count + pending_count) * 100) 
            if (completed_count + pending_count) > 0 else 0.0,
            2
        ),
        "average_description_length": round(float(avg_description_length), 2)
    }


@router.get("/notes") 
def get_note_stats(db: Session = Depends(get_db)) -> dict:
    """Get detailed statistics about notes."""
    # Get total count
    total_count = db.scalar(select(func.count(Note.id))) or 0
    
    # Get average title and content lengths
    avg_title_length = db.scalar(
        select(func.avg(func.length(Note.title)))
    ) or 0.0
    
    avg_content_length = db.scalar(
        select(func.avg(func.length(Note.content)))
    ) or 0.0
    
    return {
        "total_count": total_count,
        "average_title_length": round(float(avg_title_length), 2),
        "average_content_length": round(float(avg_content_length), 2)
    }