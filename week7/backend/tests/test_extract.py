import pytest
from backend.app.services.extract import (
    extract_action_items,
    extract_action_items_advanced,
    categorize_action_items,
    filter_action_items_by_assignee,
    get_high_priority_items,
    ExtractedActionItem
)


def test_extract_action_items():
    """Test basic extraction compatibility."""
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_checkbox_patterns():
    """Test extraction of checkbox-style tasks."""
    text = """
    - [ ] Implement new feature
    - [x] Write documentation
    - [ ] Test deployment
    """
    items = extract_action_items(text)
    assert "Implement new feature" in items
    assert "Write documentation" in items
    assert "Test deployment" in items


def test_extract_imperative_verbs():
    """Test extraction based on imperative verbs."""
    text = """
    Some notes here
    Implement the login feature
    Create user database schema
    Fix the bug in payment module
    This is just a description
    """
    items = extract_action_items(text)
    assert "Implement the login feature" in items
    assert "Create user database schema" in items
    assert "Fix the bug in payment module" in items


def test_extract_with_priority():
    """Test priority detection in action items."""
    text = """
    URGENT: Fix production bug
    TODO: Update documentation
    Maybe consider refactoring later
    """
    items = extract_action_items_advanced(text)
    
    assert len(items) == 3
    
    # Check high priority
    urgent_item = next(item for item in items if "production bug" in item.text)
    assert urgent_item.priority == "high"
    
    # Check medium priority
    todo_item = next(item for item in items if "documentation" in item.text)
    assert todo_item.priority == "medium"
    
    # Check low priority
    maybe_item = next(item for item in items if "refactoring" in item.text)
    assert maybe_item.priority == "low"


def test_extract_with_assignees():
    """Test assignee extraction."""
    text = """
    TODO: Review code @alice
    Fix bug assigned to: bob
    Update docs (charlie)
    """
    items = extract_action_items_advanced(text)
    
    assert len(items) == 3
    assert items[0].assignee == "alice"
    assert items[1].assignee == "bob"
    assert items[2].assignee == "charlie"


def test_extract_with_due_dates():
    """Test due date extraction."""
    text = """
    TODO: Complete report by 12/31/2024
    Fix bug due: January 15
    Update system deadline 01-20-2024
    """
    items = extract_action_items_advanced(text)
    
    assert len(items) == 3
    assert items[0].due_date == "12/31/2024"
    assert items[1].due_date == "January 15"
    assert items[2].due_date == "01-20-2024"


def test_categorization():
    """Test action item categorization."""
    text = """
    TODO: Write tests
    URGENT: Fix critical bug
    Maybe consider optimization
    Implement new feature
    """
    items = extract_action_items_advanced(text)
    categorized = categorize_action_items(items)
    
    assert len(categorized["high_priority"]) >= 1
    assert len(categorized["medium_priority"]) >= 1
    assert len(categorized["low_priority"]) >= 1


def test_filter_by_assignee():
    """Test filtering by assignee."""
    text = """
    TODO: Task one @alice
    TODO: Task two @bob
    TODO: Task three @alice
    """
    items = extract_action_items_advanced(text)
    alice_items = filter_action_items_by_assignee(items, "alice")
    
    assert len(alice_items) == 2
    assert all(item.assignee == "alice" for item in alice_items)


def test_get_high_priority_items():
    """Test filtering high priority items."""
    text = """
    URGENT: Critical issue
    TODO: Regular task
    ASAP: Important fix
    Maybe do this later
    """
    items = extract_action_items_advanced(text)
    high_priority = get_high_priority_items(items)
    
    assert len(high_priority) >= 2
    assert all(item.priority == "high" for item in high_priority)


def test_question_based_decisions():
    """Test extraction of decision-making questions."""
    text = """
    Should we migrate to PostgreSQL?
    Need to decide on the framework
    Can we deploy this week?
    What is the current status?
    """
    items = extract_action_items_advanced(text)
    
    # Should extract decision-making questions
    assert len(items) >= 2
    decision_items = [item for item in items if item.category == "decision"]
    assert len(decision_items) >= 1


def test_complex_extraction():
    """Test complex real-world extraction scenario."""
    text = """
    Meeting Notes - Sprint Planning
    
    URGENT: Fix login bug before release @alice due: 02/05/2026
    
    Regular tasks:
    - [ ] Implement user profile page
    - [ ] Write API documentation
    - [x] Setup CI/CD pipeline
    
    Review the new design proposal
    Should we add dark mode? @bob
    
    Maybe consider performance optimization later
    
    Deploy to staging environment!
    """
    items = extract_action_items_advanced(text)
    
    # Should extract multiple items
    assert len(items) >= 6
    
    # Check for urgent item with assignee and due date
    urgent_items = [item for item in items if item.priority == "high"]
    assert len(urgent_items) >= 2  # URGENT task and exclamation task
    
    # Check for checkbox tasks
    checkbox_items = [item for item in items if item.category == "task"]
    assert len(checkbox_items) >= 3
    
    # Check for decision item
    decision_items = [item for item in items if item.category == "decision"]
    assert len(decision_items) >= 1


def test_empty_input():
    """Test handling of empty input."""
    items = extract_action_items("")
    assert items == []
    
    items_advanced = extract_action_items_advanced("")
    assert items_advanced == []


def test_no_action_items():
    """Test text with no action items."""
    text = """
    This is just a regular note.
    It contains some information.
    But no actionable items.
    """
    items = extract_action_items(text)
    # Should extract imperative-like patterns if any
    # Or return empty list
    assert isinstance(items, list)


def test_context_extraction():
    """Test that context from surrounding lines is captured."""
    text = """
    Database Migration
    Update schema to version 2.0
    This affects user authentication
    """
    items = extract_action_items_advanced(text)
    
    # Find the update schema item
    update_item = next((item for item in items if "schema" in item.text.lower()), None)
    assert update_item is not None
    if update_item.context:
        assert "Database Migration" in update_item.context or "authentication" in update_item.context


