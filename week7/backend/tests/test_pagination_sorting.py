"""
Task 4: Comprehensive tests for pagination and sorting functionality.

This module provides enhanced test coverage for pagination and sorting across
notes, action items, and tags endpoints.
"""

import time


class TestNotesPagination:
    """Test pagination functionality for notes endpoints."""

    def test_notes_default_pagination(self, client):
        """Test that notes list returns with default pagination settings."""
        # Create multiple notes
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        
        r = client.get("/notes/")
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 5

    def test_notes_pagination_with_limit(self, client):
        """Test notes pagination with explicit limit."""
        # Create 10 notes
        for i in range(10):
            client.post("/notes/", json={"title": f"Limit Note {i}", "content": f"Content {i}"})
        
        # Request with limit=3
        r = client.get("/notes/", params={"limit": 3})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 3

    def test_notes_pagination_with_skip(self, client):
        """Test notes pagination with skip (offset)."""
        # Create notes with unique titles
        created_ids = []
        for i in range(5):
            r = client.post("/notes/", json={"title": f"Skip Note {i}", "content": f"Content {i}"})
            created_ids.append(r.json()["id"])
        
        # Get all notes first (to establish baseline)
        r_all = client.get("/notes/", params={"limit": 100})
        all_items = r_all.json()
        
        # Skip first 2
        r = client.get("/notes/", params={"skip": 2, "limit": 100})
        assert r.status_code == 200
        skipped_items = r.json()
        assert len(skipped_items) == len(all_items) - 2

    def test_notes_pagination_skip_and_limit_combined(self, client):
        """Test notes pagination with both skip and limit."""
        # Create 10 notes
        for i in range(10):
            client.post("/notes/", json={"title": f"Combined Note {i}", "content": f"Content {i}"})
        
        # Skip 2, limit 3
        r = client.get("/notes/", params={"skip": 2, "limit": 3})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 3

    def test_notes_pagination_empty_result(self, client):
        """Test notes pagination when skip exceeds available items."""
        r = client.get("/notes/", params={"skip": 10000})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 0

    def test_notes_pagination_max_limit(self, client):
        """Test that notes respects maximum limit constraint (200)."""
        r = client.get("/notes/", params={"limit": 200})
        assert r.status_code == 200

    def test_notes_pagination_exceeds_max_limit(self, client):
        """Test that requesting more than max limit is rejected."""
        r = client.get("/notes/", params={"limit": 201})
        assert r.status_code == 422  # Validation error


class TestNotesSorting:
    """Test sorting functionality for notes endpoints."""

    def test_notes_sort_by_created_at_desc(self, client):
        """Test sorting notes by created_at descending (default)."""
        # Create notes with slight delay to ensure different timestamps
        for i in range(3):
            client.post("/notes/", json={"title": f"Sort Note {i}", "content": f"Content {i}"})
        
        r = client.get("/notes/", params={"sort": "-created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            # Verify descending order
            for i in range(len(items) - 1):
                assert items[i]["created_at"] >= items[i + 1]["created_at"]

    def test_notes_sort_by_created_at_asc(self, client):
        """Test sorting notes by created_at ascending."""
        for i in range(3):
            client.post("/notes/", json={"title": f"Asc Note {i}", "content": f"Content {i}"})
        
        r = client.get("/notes/", params={"sort": "created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            # Verify ascending order
            for i in range(len(items) - 1):
                assert items[i]["created_at"] <= items[i + 1]["created_at"]

    def test_notes_sort_by_updated_at_desc(self, client):
        """Test sorting notes by updated_at descending."""
        r = client.get("/notes/", params={"sort": "-updated_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["updated_at"] >= items[i + 1]["updated_at"]

    def test_notes_sort_by_updated_at_asc(self, client):
        """Test sorting notes by updated_at ascending."""
        r = client.get("/notes/", params={"sort": "updated_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["updated_at"] <= items[i + 1]["updated_at"]

    def test_notes_sort_by_title_desc(self, client):
        """Test sorting notes by title descending."""
        client.post("/notes/", json={"title": "Alpha", "content": "A"})
        client.post("/notes/", json={"title": "Zeta", "content": "Z"})
        client.post("/notes/", json={"title": "Beta", "content": "B"})
        
        r = client.get("/notes/", params={"sort": "-title", "limit": 100})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["title"] >= items[i + 1]["title"]

    def test_notes_sort_by_title_asc(self, client):
        """Test sorting notes by title ascending."""
        client.post("/notes/", json={"title": "Zebra", "content": "Z"})
        client.post("/notes/", json={"title": "Apple", "content": "A"})
        client.post("/notes/", json={"title": "Banana", "content": "B"})
        
        r = client.get("/notes/", params={"sort": "title", "limit": 100})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["title"] <= items[i + 1]["title"]

    def test_notes_sort_by_id_desc(self, client):
        """Test sorting notes by id descending."""
        for i in range(3):
            client.post("/notes/", json={"title": f"ID Note {i}", "content": f"Content {i}"})
        
        r = client.get("/notes/", params={"sort": "-id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] > items[i + 1]["id"]

    def test_notes_sort_by_id_asc(self, client):
        """Test sorting notes by id ascending."""
        r = client.get("/notes/", params={"sort": "id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] < items[i + 1]["id"]

    def test_notes_invalid_sort_field_fallback(self, client):
        """Test that invalid sort field falls back to default sorting."""
        client.post("/notes/", json={"title": "Test", "content": "Content"})
        
        r = client.get("/notes/", params={"sort": "invalid_field"})
        assert r.status_code == 200  # Should not error, falls back to default

    def test_notes_sort_with_search_filter(self, client):
        """Test sorting combined with search query."""
        client.post("/notes/", json={"title": "Search A", "content": "Find me"})
        client.post("/notes/", json={"title": "Search B", "content": "Find me too"})
        
        r = client.get("/notes/", params={"q": "Find", "sort": "-title"})
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 2


class TestActionItemsPagination:
    """Test pagination functionality for action items endpoints."""

    def test_action_items_default_pagination(self, client):
        """Test that action items list returns with default pagination."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})
        
        r = client.get("/action-items/")
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 5

    def test_action_items_pagination_with_limit(self, client):
        """Test action items pagination with explicit limit."""
        for i in range(10):
            client.post("/action-items/", json={"description": f"Limit Task {i}"})
        
        r = client.get("/action-items/", params={"limit": 4})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 4

    def test_action_items_pagination_with_skip(self, client):
        """Test action items pagination with skip."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Skip Task {i}"})
        
        r_all = client.get("/action-items/", params={"limit": 100})
        all_count = len(r_all.json())
        
        r = client.get("/action-items/", params={"skip": 3, "limit": 100})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == all_count - 3

    def test_action_items_pagination_combined(self, client):
        """Test action items pagination with skip and limit combined."""
        for i in range(8):
            client.post("/action-items/", json={"description": f"Combined Task {i}"})
        
        r = client.get("/action-items/", params={"skip": 2, "limit": 3})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 3

    def test_action_items_pagination_empty(self, client):
        """Test action items pagination when skip exceeds count."""
        r = client.get("/action-items/", params={"skip": 99999})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 0

    def test_action_items_pagination_with_filter(self, client):
        """Test action items pagination combined with completed filter."""
        # Create some items
        for i in range(4):
            r = client.post("/action-items/", json={"description": f"Filter Task {i}"})
            if i < 2:
                item_id = r.json()["id"]
                client.put(f"/action-items/{item_id}/complete")
        
        # Get only completed items with pagination
        r = client.get("/action-items/", params={"completed": True, "limit": 10})
        assert r.status_code == 200
        items = r.json()
        assert all(item["completed"] for item in items)

    def test_action_items_max_limit(self, client):
        """Test that action items respects max limit."""
        r = client.get("/action-items/", params={"limit": 200})
        assert r.status_code == 200

    def test_action_items_exceeds_max_limit(self, client):
        """Test that requesting more than max limit is rejected."""
        r = client.get("/action-items/", params={"limit": 201})
        assert r.status_code == 422


class TestActionItemsSorting:
    """Test sorting functionality for action items endpoints."""

    def test_action_items_sort_by_created_at_desc(self, client):
        """Test sorting action items by created_at descending."""
        for i in range(3):
            client.post("/action-items/", json={"description": f"Sort Task {i}"})
        
        r = client.get("/action-items/", params={"sort": "-created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["created_at"] >= items[i + 1]["created_at"]

    def test_action_items_sort_by_created_at_asc(self, client):
        """Test sorting action items by created_at ascending."""
        r = client.get("/action-items/", params={"sort": "created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["created_at"] <= items[i + 1]["created_at"]

    def test_action_items_sort_by_id_desc(self, client):
        """Test sorting action items by id descending."""
        for i in range(3):
            client.post("/action-items/", json={"description": f"ID Task {i}"})
        
        r = client.get("/action-items/", params={"sort": "-id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] > items[i + 1]["id"]

    def test_action_items_sort_by_id_asc(self, client):
        """Test sorting action items by id ascending."""
        r = client.get("/action-items/", params={"sort": "id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] < items[i + 1]["id"]

    def test_action_items_sort_by_description_desc(self, client):
        """Test sorting action items by description descending."""
        client.post("/action-items/", json={"description": "Alpha task"})
        client.post("/action-items/", json={"description": "Zeta task"})
        
        r = client.get("/action-items/", params={"sort": "-description", "limit": 100})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["description"] >= items[i + 1]["description"]

    def test_action_items_sort_by_description_asc(self, client):
        """Test sorting action items by description ascending."""
        r = client.get("/action-items/", params={"sort": "description"})
        assert r.status_code == 200

    def test_action_items_sort_with_completed_filter(self, client):
        """Test sorting combined with completed filter."""
        for i in range(3):
            r = client.post("/action-items/", json={"description": f"Filter Sort {i}"})
            item_id = r.json()["id"]
            client.put(f"/action-items/{item_id}/complete")
        
        r = client.get("/action-items/", params={"completed": True, "sort": "-id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] > items[i + 1]["id"]

    def test_action_items_invalid_sort_field(self, client):
        """Test that invalid sort field falls back to default."""
        r = client.get("/action-items/", params={"sort": "nonexistent"})
        assert r.status_code == 200


class TestTagsPagination:
    """Test pagination functionality for tags endpoints."""

    def test_tags_default_pagination(self, client):
        """Test that tags list returns with default pagination."""
        for i in range(5):
            client.post("/tags/", json={"name": f"Tag{i}", "color": f"#0000{i:02d}"})
        
        r = client.get("/tags/")
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 5

    def test_tags_pagination_with_limit(self, client):
        """Test tags pagination with explicit limit."""
        for i in range(10):
            client.post("/tags/", json={"name": f"LimitTag{i}", "color": f"#00{i:02d}00"})
        
        r = client.get("/tags/", params={"limit": 5})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 5

    def test_tags_pagination_with_skip(self, client):
        """Test tags pagination with skip."""
        for i in range(6):
            client.post("/tags/", json={"name": f"SkipTag{i}", "color": f"#{i:02d}0000"})
        
        r_all = client.get("/tags/", params={"limit": 100})
        all_count = len(r_all.json())
        
        r = client.get("/tags/", params={"skip": 2, "limit": 100})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == all_count - 2

    def test_tags_pagination_combined(self, client):
        """Test tags pagination with skip and limit."""
        for i in range(8):
            client.post("/tags/", json={"name": f"CombTag{i}", "color": "#FFFFFF"})
        
        r = client.get("/tags/", params={"skip": 1, "limit": 4})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 4

    def test_tags_pagination_empty(self, client):
        """Test tags pagination when skip exceeds count."""
        r = client.get("/tags/", params={"skip": 99999})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 0

    def test_tags_max_limit(self, client):
        """Test that tags respects max limit."""
        r = client.get("/tags/", params={"limit": 200})
        assert r.status_code == 200

    def test_tags_exceeds_max_limit(self, client):
        """Test that requesting more than max limit is rejected."""
        r = client.get("/tags/", params={"limit": 201})
        assert r.status_code == 422


class TestTagsSorting:
    """Test sorting functionality for tags endpoints."""

    def test_tags_sort_by_created_at_desc(self, client):
        """Test sorting tags by created_at descending."""
        for i in range(3):
            client.post("/tags/", json={"name": f"SortTag{i}", "color": "#000000"})
        
        r = client.get("/tags/", params={"sort": "-created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["created_at"] >= items[i + 1]["created_at"]

    def test_tags_sort_by_created_at_asc(self, client):
        """Test sorting tags by created_at ascending."""
        r = client.get("/tags/", params={"sort": "created_at"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["created_at"] <= items[i + 1]["created_at"]

    def test_tags_sort_by_name_desc(self, client):
        """Test sorting tags by name descending."""
        client.post("/tags/", json={"name": "AlphaTag", "color": "#AA0000"})
        client.post("/tags/", json={"name": "ZetaTag", "color": "#ZZ0000"})
        
        r = client.get("/tags/", params={"sort": "-name", "limit": 100})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["name"] >= items[i + 1]["name"]

    def test_tags_sort_by_name_asc(self, client):
        """Test sorting tags by name ascending."""
        r = client.get("/tags/", params={"sort": "name"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["name"] <= items[i + 1]["name"]

    def test_tags_sort_by_id_desc(self, client):
        """Test sorting tags by id descending."""
        r = client.get("/tags/", params={"sort": "-id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] > items[i + 1]["id"]

    def test_tags_sort_by_id_asc(self, client):
        """Test sorting tags by id ascending."""
        r = client.get("/tags/", params={"sort": "id"})
        assert r.status_code == 200
        items = r.json()
        if len(items) >= 2:
            for i in range(len(items) - 1):
                assert items[i]["id"] < items[i + 1]["id"]

    def test_tags_sort_with_search_filter(self, client):
        """Test sorting combined with search query."""
        client.post("/tags/", json={"name": "SearchA", "color": "#111111"})
        client.post("/tags/", json={"name": "SearchB", "color": "#222222"})
        
        r = client.get("/tags/", params={"q": "Search", "sort": "-name"})
        assert r.status_code == 200
        items = r.json()
        assert len(items) >= 2

    def test_tags_invalid_sort_field(self, client):
        """Test that invalid sort field falls back to default."""
        r = client.get("/tags/", params={"sort": "invalid"})
        assert r.status_code == 200


class TestPaginationEdgeCases:
    """Test edge cases for pagination across all endpoints."""

    def test_notes_skip_zero(self, client):
        """Test notes with skip=0 (should be same as default)."""
        client.post("/notes/", json={"title": "Edge Note", "content": "Content"})
        
        r = client.get("/notes/", params={"skip": 0})
        assert r.status_code == 200

    def test_notes_limit_one(self, client):
        """Test notes with limit=1."""
        for i in range(3):
            client.post("/notes/", json={"title": f"One Note {i}", "content": f"Content {i}"})
        
        r = client.get("/notes/", params={"limit": 1})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 1

    def test_action_items_skip_negative_validation(self, client):
        """Test that negative skip values are handled."""
        # Depending on implementation, might be 422 or handled gracefully
        r = client.get("/action-items/", params={"skip": -1})
        # Should either reject or treat as 0
        assert r.status_code in [200, 422]

    def test_action_items_limit_zero_validation(self, client):
        """Test that limit=0 is handled."""
        r = client.get("/action-items/", params={"limit": 0})
        # Should either return empty or reject
        assert r.status_code in [200, 422]

    def test_tags_large_skip(self, client):
        """Test tags with very large skip value."""
        r = client.get("/tags/", params={"skip": 1000000})
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 0

    def test_notes_pagination_consistency(self, client):
        """Test that pagination results are consistent."""
        # Create 5 notes
        created_ids = []
        for i in range(5):
            r = client.post("/notes/", json={"title": f"Consistent {i}", "content": f"C {i}"})
            created_ids.append(r.json()["id"])
        
        # Get page 1 (items 0-2) and page 2 (items 3-4)
        r1 = client.get("/notes/", params={"skip": 0, "limit": 3, "sort": "id"})
        r2 = client.get("/notes/", params={"skip": 3, "limit": 3, "sort": "id"})
        
        page1_ids = [item["id"] for item in r1.json()]
        page2_ids = [item["id"] for item in r2.json()]
        
        # No overlap between pages
        assert len(set(page1_ids) & set(page2_ids)) == 0


class TestSortingEdgeCases:
    """Test edge cases for sorting across all endpoints."""

    def test_notes_empty_sort_string(self, client):
        """Test notes with empty sort string."""
        r = client.get("/notes/", params={"sort": ""})
        assert r.status_code == 200

    def test_action_items_sort_only_minus(self, client):
        """Test action items with sort='-' (just the minus sign)."""
        r = client.get("/action-items/", params={"sort": "-"})
        assert r.status_code == 200  # Should fallback to default

    def test_tags_sort_special_characters(self, client):
        """Test tags with special characters in sort field."""
        r = client.get("/tags/", params={"sort": "-id; DROP TABLE tags;--"})
        assert r.status_code == 200  # Should handle safely (SQL injection prevention)

    def test_notes_sort_case_sensitivity(self, client):
        """Test that sort field is case-insensitive or handled correctly."""
        r = client.get("/notes/", params={"sort": "-CREATED_AT"})
        # Might fallback to default if case-sensitive
        assert r.status_code == 200

    def test_action_items_multiple_sort_fields(self, client):
        """Test action items with multiple sort fields (not supported, should work with first)."""
        r = client.get("/action-items/", params={"sort": "-created_at,id"})
        assert r.status_code == 200


class TestCombinedPaginationAndSorting:
    """Test pagination and sorting combined scenarios."""

    def test_notes_paginate_sorted_results(self, client):
        """Test paginating through sorted notes."""
        # Create notes
        for i in range(6):
            client.post("/notes/", json={"title": f"Combo {i}", "content": f"Content {i}"})
        
        # Get sorted pages
        page1 = client.get("/notes/", params={"sort": "id", "skip": 0, "limit": 3}).json()
        page2 = client.get("/notes/", params={"sort": "id", "skip": 3, "limit": 3}).json()
        
        # Last item of page 1 should have smaller id than first item of page 2
        if len(page1) > 0 and len(page2) > 0:
            assert page1[-1]["id"] < page2[0]["id"]

    def test_action_items_filter_sort_paginate(self, client):
        """Test filtering, sorting, and pagination together."""
        # Create items with some completed
        for i in range(6):
            r = client.post("/action-items/", json={"description": f"FSP Task {i}"})
            if i % 2 == 0:
                client.put(f"/action-items/{r.json()['id']}/complete")
        
        # Filter completed, sort by id, paginate
        r = client.get("/action-items/", params={
            "completed": True,
            "sort": "-id",
            "skip": 0,
            "limit": 2
        })
        assert r.status_code == 200
        items = r.json()
        assert len(items) <= 2
        assert all(item["completed"] for item in items)

    def test_tags_search_sort_paginate(self, client):
        """Test search, sorting, and pagination for tags."""
        # Create searchable tags
        for i in range(4):
            client.post("/tags/", json={"name": f"SearchTest{i}", "color": "#000000"})
        
        r = client.get("/tags/", params={
            "q": "SearchTest",
            "sort": "name",
            "skip": 1,
            "limit": 2
        })
        assert r.status_code == 200
        items = r.json()
        assert len(items) <= 2
