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
    
    print(f"Starting server from directory: {os.getcwd()}")
    print(f"Python path includes: {sys.path[0]}")
    
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)