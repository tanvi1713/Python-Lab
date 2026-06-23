import os
import sys

PRACTICALS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "PythonPracticals",
)

sys.path.insert(0, PRACTICALS_DIR)
