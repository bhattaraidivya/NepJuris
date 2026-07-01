import os
import sys

# Allow `import pipeline.x` / `import rag.x` regardless of the directory
# pytest is invoked from.
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
