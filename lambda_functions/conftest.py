# conftest.py
import sys
import os

# Help pytest with absoult imports of common directory
# while also allowing AWS to import them
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
