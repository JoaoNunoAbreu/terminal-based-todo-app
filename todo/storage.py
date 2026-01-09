"""File I/O operations for task persistence."""

import sys
import json

from .config import DATA_FILE_PATH


def read_tasks():
    """Read tasks from the JSON file with comprehensive error handling."""
    try:
        with open(DATA_FILE_PATH) as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"Info: Creating new data file at {DATA_FILE_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: The data file is corrupted or contains invalid JSON.")
        print(f"Details: {str(e)}")
        print(f"Please fix or delete {DATA_FILE_PATH} to start fresh.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read {DATA_FILE_PATH}")
        print("Please check file permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the data file.")
        print(f"Details: {str(e)}")
        sys.exit(1)


def write_tasks(info):
    """Write tasks to the JSON file with comprehensive error handling."""
    try:
        with open(DATA_FILE_PATH, 'w') as outfile:
            json.dump(info, outfile, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"Error: Permission denied when trying to write to {DATA_FILE_PATH}")
        print("Please check file permissions.")
        sys.exit(1)
    except OSError as e:
        print(f"Error: Unable to write to the data file.")
        print(f"Details: {str(e)}")
        print("This may be due to disk space, read-only filesystem, or other system issues.")
        sys.exit(1)
    except TypeError as e:
        print(f"Error: Invalid data structure cannot be saved to JSON.")
        print(f"Details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while writing the data file.")
        print(f"Details: {str(e)}")
        sys.exit(1)
