"""Utility functions for task management."""

import sys

from .storage import write_tasks


def create_task(info, section, task, date):
    """Create a new task with validation."""
    try:
        if section not in info:
            info[section] = []
        if not isinstance(info[section], list):
            print(f"Error: Section '{section}' has invalid data format.")
            sys.exit(1)

        next_id = len(info[section]) + 1
        info[section].append({
            "id": next_id,
            "task": task,
            "date": date,
            "done": False
        })
        write_tasks(info)
    except Exception as e:
        print(f"Error: Unable to create task.")
        print(f"Details: {str(e)}")
        sys.exit(1)


def normalize_ids(info):
    """Reindex task IDs with validation."""
    try:
        for section in info:
            if not isinstance(info[section], list):
                print(f"Warning: Section '{section}' has invalid format, skipping normalization...")
                continue

            count = 1
            for elem in info[section]:
                if isinstance(elem, dict):
                    elem['id'] = count
                    count += 1
        return info
    except Exception as e:
        print(f"Error: Unable to normalize task IDs.")
        print(f"Details: {str(e)}")
        return info


def has_tasks(data):
    """Check if there are any tasks in the data structure."""
    try:
        if not isinstance(data, dict):
            return False
        for section in data:
            if isinstance(data[section], list) and data[section] != []:
                return True
        return False
    except Exception:
        return False
