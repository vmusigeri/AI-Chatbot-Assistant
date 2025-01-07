import uvicorn
from pathlib import Path
import sys

# Add the project root to Python path
root_path = str(Path(__file__).parent)
if root_path not in sys.path:
    sys.path.append(root_path)

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(Path(__file__).parent)]
    ) 