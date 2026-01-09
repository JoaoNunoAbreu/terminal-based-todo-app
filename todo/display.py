"""Display formatting for tasks."""

from .config import DATA_FILE_PATH
from .utils import has_tasks


def prettyprint(data):
    """Display tasks in a formatted table with error handling for corrupted data."""
    if not has_tasks(data):
        print("No data. Try adding some tasks! Use \"todo help\" for more info.")
        return

    table = []
    section_width = 8
    task_width = 5

    try:
        for section_name, tasks in data.items():
            identifier = 1
            if not isinstance(tasks, list):
                print(f"Warning: Section '{section_name}' has invalid data format, skipping...")
                continue

            for task in tasks:
                if not isinstance(task, dict):
                    print(f"Warning: Invalid task data in section '{section_name}', skipping...")
                    continue

                is_done = task.get('done', False)
                checkbox = "[✓]" if is_done else "[ ]"
                task_text = task.get('task', '[Missing task description]')
                date_text = task.get('date', '')

                task_display = f"{checkbox} {identifier} - {task_text}"
                table.append([section_name, task_display, date_text, is_done])

                if len(section_name) > section_width:
                    section_width = len(section_name)
                if len(task_display) > task_width:
                    task_width = len(task_display)
                identifier += 1

        if not table:
            print("No valid tasks to display.")
            return

        print()
        print(f" {'Section':<{section_width}} | {'Task':<{task_width}} | {'Date':<6}")

        last_section = ""
        for row in table:
            if row[0] != last_section:
                print("-" * (section_width + 2) + "+" + "-" * (task_width + 2) + "+" + "-" * 9)
                print(f" {row[0]:<{section_width}} | {row[1]:<{task_width}} | {row[2]:<7}")
                last_section = row[0]
            else:
                print(f" {' ':<{section_width}} | {row[1]:<{task_width}} | {row[2]:<7}")
        print()

    except Exception as e:
        print(f"Error: Unable to display tasks due to data corruption.")
        print(f"Details: {str(e)}")
        print(f"Please check or repair {DATA_FILE_PATH}")
