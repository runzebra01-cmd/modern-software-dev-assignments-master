"""Tests for Tag endpoints (Task 3: New model with relationships)."""


def test_create_tag(client):
    """Test creating a new tag."""
    payload = {"name": "Urgent", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Urgent"
    assert data["color"] == "#FF0000"
    assert "created_at" in data and "updated_at" in data
    assert "id" in data


def test_list_tags(client):
    """Test listing all tags."""
    # Create a tag first
    payload = {"name": "TestTag", "color": "#00FF00"}
    client.post("/tags/", json=payload)
    
    r = client.get("/tags/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(tag["name"] == "TestTag" for tag in items)


def test_get_tag(client):
    """Test getting a specific tag by ID."""
    # Create a tag first
    payload = {"name": "GetTest", "color": "#0000FF"}
    r = client.post("/tags/", json=payload)
    tag_id = r.json()["id"]
    
    # Get the tag
    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "GetTest"
    assert data["color"] == "#0000FF"


def test_patch_tag(client):
    """Test updating a tag."""
    # Create a tag first
    payload = {"name": "PatchTest", "color": "#FFFF00"}
    r = client.post("/tags/", json=payload)
    tag_id = r.json()["id"]
    
    # Update the tag
    r = client.patch(f"/tags/{tag_id}", json={"name": "Updated", "color": "#FF00FF"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Updated"
    assert data["color"] == "#FF00FF"


def test_delete_tag(client):
    """Test deleting a tag."""
    # Create a tag first
    payload = {"name": "DeleteTest", "color": "#00FFFF"}
    r = client.post("/tags/", json=payload)
    tag_id = r.json()["id"]
    
    # Delete the tag
    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204
    
    # Verify it's deleted
    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 404


def test_add_tag_to_note(client):
    """Test adding a tag to a note."""
    # Create a note
    note_payload = {"title": "Test Note", "content": "Content"}
    r = client.post("/notes/", json=note_payload)
    note_id = r.json()["id"]
    
    # Create a tag
    tag_payload = {"name": "AssocTest", "color": "#123456"}
    r = client.post("/tags/", json=tag_payload)
    tag_id = r.json()["id"]
    
    # Add tag to note
    r = client.post(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 204
    
    # Verify the association
    r = client.get(f"/notes/{note_id}/with-tags")
    assert r.status_code == 200
    data = r.json()
    assert any(tag["id"] == tag_id for tag in data["tags"])


def test_remove_tag_from_note(client):
    """Test removing a tag from a note."""
    # Create a note
    note_payload = {"title": "Test Note 2", "content": "Content 2"}
    r = client.post("/notes/", json=note_payload)
    note_id = r.json()["id"]
    
    # Create a tag
    tag_payload = {"name": "RemoveTest", "color": "#654321"}
    r = client.post("/tags/", json=tag_payload)
    tag_id = r.json()["id"]
    
    # Add tag to note
    client.post(f"/tags/{tag_id}/notes/{note_id}")
    
    # Remove tag from note
    r = client.delete(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 204
    
    # Verify the association is removed
    r = client.get(f"/notes/{note_id}/with-tags")
    assert r.status_code == 200
    data = r.json()
    assert not any(tag["id"] == tag_id for tag in data["tags"])


def test_get_notes_by_tag(client):
    """Test getting all notes with a specific tag."""
    # Create a tag
    tag_payload = {"name": "FilterTest", "color": "#AABBCC"}
    r = client.post("/tags/", json=tag_payload)
    tag_id = r.json()["id"]
    
    # Create two notes
    note1 = client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
    note1_id = note1.json()["id"]
    note2 = client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})
    note2_id = note2.json()["id"]
    
    # Add tag to both notes
    client.post(f"/tags/{tag_id}/notes/{note1_id}")
    client.post(f"/tags/{tag_id}/notes/{note2_id}")
    
    # Get notes by tag
    r = client.get(f"/tags/{tag_id}/notes")
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) >= 2
    note_ids = [note["id"] for note in notes]
    assert note1_id in note_ids
    assert note2_id in note_ids


def test_duplicate_tag_name_error(client):
    """Test that creating a tag with duplicate name fails."""
    payload = {"name": "DuplicateTest", "color": "#111111"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    
    # Try to create another tag with the same name
    r = client.post("/tags/", json=payload)
    assert r.status_code == 400
    assert "already exists" in r.text.lower()


def test_tag_validation(client):
    """Test tag validation."""
    # Empty name should fail
    r = client.post("/tags/", json={"name": "", "color": "#000000"})
    assert r.status_code == 422
    
    # Whitespace-only name should fail
    r = client.post("/tags/", json={"name": "   ", "color": "#000000"})
    assert r.status_code == 422
