import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.dirname(__file__))

# Add the project root to Python path
sys.path.insert(0, project_root) 