import sys
import os

# Get the path to the scripts directory
def set_scr_path() -> None:
    scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    sys.path.append(scripts_path)