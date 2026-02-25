import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent

# Add project root to Python path
sys.path.insert(0, str(project_root))

# Change working directory to project root
os.chdir(project_root)

# Now import and run the app
if __name__ == "__main__":
    import uvicorn
    from backend.app.main import app
    
    print("=" * 70)
    print("  Task 3: Tags Model with Relationships")
    print("=" * 70)
    print(f"Starting server from directory: {os.getcwd()}")
    print("\nNew features:")
    print("  ✓ Tag model with many-to-many relationships")
    print("  ✓ Full CRUD operations for tags")
    print("  ✓ Associate tags with notes")
    print("  ✓ Filter notes by tags")
    print("\nNew endpoints:")
    print("  • GET    /tags/ - List all tags")
    print("  • POST   /tags/ - Create a new tag")
    print("  • GET    /tags/{id} - Get a specific tag")
    print("  • PATCH  /tags/{id} - Update a tag")
    print("  • DELETE /tags/{id} - Delete a tag")
    print("  • GET    /tags/{id}/notes - Get notes with tag")
    print("  • POST   /tags/{id}/notes/{note_id} - Add tag to note")
    print("  • DELETE /tags/{id}/notes/{note_id} - Remove tag from note")
    print("  • GET    /notes/{id}/with-tags - Get note with tags")
    print("\nServer: http://127.0.0.1:8083")
    print("API Docs: http://127.0.0.1:8083/docs")
    print("=" * 70 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8083, reload=False)
