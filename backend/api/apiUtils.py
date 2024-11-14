import sys
import os

# Get the path to the scripts directory
def set_scr_path() -> None:
    scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    sys.path.append(scripts_path)

def set_data_path() -> None:
    data_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')
    sys.path.append(data_path)