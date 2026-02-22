"""Run all tests from the project root."""

import subprocess
import sys
import os

# Ensure we run from the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

sys.exit(subprocess.call([sys.executable, "-m", "pytest", "tests/", "-v", *sys.argv[1:]]))
