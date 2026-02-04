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
    print("  Task 2: Enhanced Extraction Logic Server")
    print("=" * 70)
    print(f"Starting server from directory: {os.getcwd()}")
    print("\nNew features:")
    print("  ✓ Auto-extract action items from notes")
    print("  ✓ Priority, assignee, date detection")
    print("\nServer: http://127.0.0.1:8002")
    print("=" * 70 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)
