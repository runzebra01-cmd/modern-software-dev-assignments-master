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
    print("  Task 4: Pagination and Sorting Test Coverage")
    print("=" * 70)
    print(f"Starting server from directory: {os.getcwd()}")
    print("\nPagination & Sorting features:")
    print("  ✓ skip/limit pagination on all list endpoints")
    print("  ✓ Ascending/descending sort with - prefix")
    print("  ✓ Sort by multiple fields (id, created_at, updated_at, title, etc.)")
    print("  ✓ Combined filtering, sorting, and pagination")
    print("  ✓ Max limit validation (200)")
    print("\nPagination parameters:")
    print("  • skip: int    - Number of items to skip (default: 0)")
    print("  • limit: int   - Max items to return (default: 50, max: 200)")
    print("  • sort: str    - Sort field, prefix with - for desc (e.g., -created_at)")
    print("\nExample requests:")
    print("  • GET /notes/?skip=0&limit=10&sort=-created_at")
    print("  • GET /action-items/?completed=true&sort=id&limit=5")
    print("  • GET /tags/?q=urgent&sort=-name&skip=0&limit=20")
    print("\nTest file: backend/tests/test_pagination_sorting.py (62 tests)")
    print("\nServer: http://127.0.0.1:8005")
    print("API Docs: http://127.0.0.1:8005/docs")
    print("=" * 70 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=False)
