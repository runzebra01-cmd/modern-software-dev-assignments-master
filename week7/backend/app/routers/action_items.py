from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemPatch, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(ActionItem, sort_field):
        stmt = stmt.order_by(order_fn(getattr(ActionItem, sort_field)))
    else:
        stmt = stmt.order_by(desc(ActionItem.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    """Create a new action item."""
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    """Mark an action item as completed."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    if item.completed:
        raise HTTPException(status_code=400, detail="Action item is already completed")
    
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ActionItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    """Get a specific action item by ID."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)) -> ActionItemRead:
    """Update specific fields of an action item."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    if payload.description is not None:
        item.description = payload.description
    
    if payload.completed is not None:
        item.completed = payload.completed
    
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an action item."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    db.delete(item)


@router.put("/{item_id}", response_model=ActionItemRead)
def update_item(item_id: int, payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    """Fully update an action item."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    item.description = payload.description
    item.completed = False  # Reset to incomplete when fully updating
    
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/bulk/complete", response_model=dict)
def bulk_complete_items(
    item_ids: list[int], 
    db: Session = Depends(get_db)
) -> dict:
    """Mark multiple action items as completed."""
    if not item_ids:
        raise HTTPException(status_code=400, detail="No item IDs provided")
    
    if any(item_id <= 0 for item_id in item_ids):
        raise HTTPException(status_code=400, detail="All item IDs must be positive integers")
    
    # Check if all items exist
    items = db.execute(
        select(ActionItem).where(ActionItem.id.in_(item_ids))
    ).scalars().all()
    
    found_ids = {item.id for item in items}
    missing_ids = set(item_ids) - found_ids
    
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Action items not found: {sorted(missing_ids)}"
        )
    
    # Update items
    updated_count = 0
    for item in items:
        if not item.completed:
            item.completed = True
            db.add(item)
            updated_count += 1
    
    return {
        "message": f"Successfully updated {updated_count} items",
        "updated_count": updated_count,
        "total_requested": len(item_ids)
    }


@router.delete("/bulk", status_code=200)
def bulk_delete_items(
    item_ids: list[int],
    db: Session = Depends(get_db)
) -> dict:
    """Delete multiple action items."""
    if not item_ids:
        raise HTTPException(status_code=400, detail="No item IDs provided")
    
    if any(item_id <= 0 for item_id in item_ids):
        raise HTTPException(status_code=400, detail="All item IDs must be positive integers")
    
    # Check if all items exist and delete them
    items = db.execute(
        select(ActionItem).where(ActionItem.id.in_(item_ids))
    ).scalars().all()
    
    found_ids = {item.id for item in items}
    missing_ids = set(item_ids) - found_ids
    
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Action items not found: {sorted(missing_ids)}"
        )
    
    # Delete items
    for item in items:
        db.delete(item)
    
    return {
        "message": f"Successfully deleted {len(items)} items",
        "deleted_count": len(items),
        "deleted_ids": sorted(item_ids)
    }


