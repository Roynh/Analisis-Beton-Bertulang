import sys
import os

# Print the current working directory
print("Current working directory:", os.getcwd())

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

print("Python path:", sys.path)

from calculations.Beam import Beam
