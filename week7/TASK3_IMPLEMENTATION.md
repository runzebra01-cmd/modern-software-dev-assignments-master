# Task 3 Implementation: Tags Model with Relationships

## Overview
This implementation adds a new **Tag** model with many-to-many relationships to Notes, fulfilling Task 3 requirements.

## What Was Implemented

### 1. Database Schema (models.py)
- **Tag Model**: New table with `id`, `name` (unique), `color`, and timestamps
- **Association Table**: `note_tags` for many-to-many relationship between Notes and Tags
- **Relationships**: 
  - One Note can have multiple Tags
  - One Tag can be applied to multiple Notes

### 2. API Schemas (schemas.py)
- `TagCreate`: Schema for creating new tags
- `TagRead`: Schema for reading tag data
- `TagPatch`: Schema for updating tags
- `NoteReadWithTags`: Extended note schema that includes associated tags

### 3. REST API Endpoints (routers/tags.py)
Full CRUD operations for tags:
- `GET /tags/` - List all tags (with filtering, sorting, pagination)
- `POST /tags/` - Create a new tag
- `GET /tags/{tag_id}` - Get a specific tag
- `PATCH /tags/{tag_id}` - Update a tag
- `DELETE /tags/{tag_id}` - Delete a tag
- `GET /tags/{tag_id}/notes` - Get all notes with a specific tag
- `POST /tags/{tag_id}/notes/{note_id}` - Add a tag to a note
- `DELETE /tags/{tag_id}/notes/{note_id}` - Remove a tag from a note

### 4. Extended Notes Endpoints (routers/notes.py)
- `GET /notes/{note_id}/with-tags` - Get a note with its associated tags

### 5. Database Seed Data (seed.sql)
- Sample tags: Important, Work, Personal, Ideas
- Sample associations between notes and tags

### 6. Comprehensive Tests (test_tags.py)
10 test cases covering:
- Tag CRUD operations
- Tag-Note associations
- Validation and error handling
- Duplicate prevention

## Example Usage

### Create a Tag
```bash
curl -X POST http://127.0.0.1:8002/tags/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Important", "color": "#FF5733"}'
```

### Add Tag to Note
```bash
curl -X POST http://127.0.0.1:8002/tags/1/notes/1
```

### Get Note with Tags
```bash
curl http://127.0.0.1:8002/notes/1/with-tags
```

### Get All Notes with a Specific Tag
```bash
curl http://127.0.0.1:8002/tags/1/notes
```

## Features
✅ Many-to-many relationships using SQLAlchemy  
✅ Full REST API with proper HTTP status codes  
✅ Input validation with Pydantic  
✅ Proper error handling (404, 400, 422)  
✅ Duplicate name prevention  
✅ Cascade delete for associations  
✅ Comprehensive test coverage  
✅ Query parameters for filtering and sorting  
✅ Pagination support  

## Test Results
All 10 tests passed successfully:
- test_create_tag ✅
- test_list_tags ✅
- test_get_tag ✅
- test_patch_tag ✅
- test_delete_tag ✅
- test_add_tag_to_note ✅
- test_remove_tag_from_note ✅
- test_get_notes_by_tag ✅
- test_duplicate_tag_name_error ✅
- test_tag_validation ✅

## Database Schema
```sql
CREATE TABLE tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  color TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE note_tags (
  note_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY (note_id, tag_id),
  FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

## Files Modified/Created
1. ✏️ `backend/app/models.py` - Added Tag model and association table
2. ✏️ `backend/app/schemas.py` - Added Tag schemas
3. ✨ `backend/app/routers/tags.py` - New router with full CRUD
4. ✏️ `backend/app/main.py` - Registered tags router
5. ✏️ `backend/app/routers/notes.py` - Added with-tags endpoint
6. ✏️ `data/seed.sql` - Added tags tables and sample data
7. ✨ `backend/tests/test_tags.py` - Comprehensive test suite

## Running the Application
```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Run tests
pytest backend/tests/test_tags.py -v

# Start server
uvicorn backend.app.main:app --reload --port 8002

# Access API docs
http://127.0.0.1:8002/docs
```
