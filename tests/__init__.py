from pathlib import Path
import sys

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))