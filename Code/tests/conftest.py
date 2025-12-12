"""
Minimal conftest.py for pytest path setup.
This adds the project root to sys.path so imports work.
"""
import sys
import os

# Add the project root to Python path (for "from Code.xxx import yyy")
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also add the Code directory to Python path (for relative imports like "import config.config")
code_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if code_dir not in sys.path:
    sys.path.insert(0, code_dir)
