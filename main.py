import sys
import json
import os
from sys import argv
from datetime import datetime

DEFAULT_SECTION = "GENERAL"
EMPTY_DATE = ""

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + "/data.json"


def readTasks():
    """Read tasks from the JSON file with comprehensive error handling."""
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        # First run - data.json doesn't exist yet, return empty structure
        print(f"Info: Creating new data file at {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: The data file is corrupted or contains invalid JSON.")
        print(f"Details: {str(e)}")
        print(f"Please fix or delete {file_path} to start fresh.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read {file_path}")
        print("Please check file permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the data file.")
        print(f"Details: {str(e)}")
        sys.exit(1)


def writeTasks(info):
    """Write tasks to the JSON file with comprehensive error handling."""
    try:
        with open(file_path, 'w') as outfile:
            json.dump(info, outfile, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"Error: Permission denied when trying to write to {file_path}")
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


def newTask(info, section, task, date):
    """Create a new task with validation."""
    try:
        # Validate that section exists and is a list
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
        writeTasks(info)
    except Exception as e:
        print(f"Error: Unable to create task.")
        print(f"Details: {str(e)}")
        sys.exit(1)


def normalize(info):
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


def are_there_tasks(data):
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


def prettyprint(data):
    """Display tasks in a formatted table with error handling for corrupted data."""
    if (are_there_tasks(data) is False):
        print("No data. Try adding some tasks! Use \"todo help\" for more info.")
        return

    table = []
    section_width = 8
    task_width = 5

    try:
        for x, y in data.items():
            identifier = 1
            # Validate that section contains a list
            if not isinstance(y, list):
                print(f"Warning: Section '{x}' has invalid data format, skipping...")
                continue

            for i in y:
                # Defensive programming: handle missing or invalid fields
                if not isinstance(i, dict):
                    print(f"Warning: Invalid task data in section '{x}', skipping...")
                    continue

                is_done = i.get('done', False)
                checkbox = "[✓]" if is_done else "[ ]"
                task_text = i.get('task', '[Missing task description]')
                date_text = i.get('date', '')

                task_display = f"{checkbox} {identifier} - {task_text}"
                table.append([x, task_display, date_text, is_done])

                if len(x) > section_width:
                    section_width = len(x)
                if len(task_display) > task_width:
                    task_width = len(task_display)
                identifier += 1

        if not table:
            print("No valid tasks to display.")
            return

        print()
        print(f" {'Section':<{section_width}} | {'Task':<{task_width}} | {'Date':<6}")

        last_section = ""
        for i in table:
            if i[0] != last_section:
                print("-" * (section_width+2) + "+" + "-" * (task_width+2) + "+" + "-" * 9)
                print(f" {i[0]:<{section_width}} | {i[1]:<{task_width}} | {i[2]:<7}")
                last_section = i[0]
            else:
                print(f" {' ':<{section_width}} | {i[1]:<{task_width}} | {i[2]:<7}")
        print()

    except Exception as e:
        print(f"Error: Unable to display tasks due to data corruption.")
        print(f"Details: {str(e)}")
        print(f"Please check or repair {file_path}")


def main():
    if ((len(sys.argv) in [3,4,5]) and sys.argv[1] == "add"):

        info = readTasks()

        # Cria a seccção, caso não exista
        if (len(sys.argv) == 3 or (len(sys.argv) == 4 and "/" in sys.argv[3])):
            if (DEFAULT_SECTION not in info):
                info[DEFAULT_SECTION] = []
        else:
            if (argv[2] not in info and "/" not in sys.argv[3]):
                info[sys.argv[2]] = []

        # Adiciona nova task ao ficheiro
        if (len(sys.argv) == 3):
            newTask(info, DEFAULT_SECTION, sys.argv[2], EMPTY_DATE)

        elif (len(sys.argv) == 4):
            # Caso tenha data sem seção
            if ("/" in sys.argv[3]):
                newTask(info, DEFAULT_SECTION, sys.argv[2], sys.argv[3])
            # Caso tenha secção sem data
            else:
                newTask(info, sys.argv[2], sys.argv[3], EMPTY_DATE)

        elif (len(sys.argv) == 5):
            if ("/" not in sys.argv[4]):
                print("Invalid date...")
                sys.exit()
            newTask(info, sys.argv[2], sys.argv[3], sys.argv[4])

        prettyprint(readTasks())

    elif (len(sys.argv) == 1):
        prettyprint(readTasks())
    elif (len(sys.argv) == 3 and sys.argv[1] == "rs"):
        info = readTasks()
        seccao = sys.argv[2]
        if (seccao not in info):
            print("Section doesn't exist...")
            sys.exit(0)
        del info[seccao]
        writeTasks(info)
    elif (len(sys.argv) == 4 and sys.argv[1] == "rm"):
        info = readTasks()
        seccao = sys.argv[2]
        if (seccao not in info):
            print("Section doesn't exist...")
            sys.exit(0)

        # Validate task ID is a valid integer
        try:
            task_id = int(sys.argv[3])
        except ValueError:
            print(f"Error: Task ID must be a number, got '{sys.argv[3]}'")
            sys.exit(1)

        if (task_id > len(info[seccao]) or task_id <= 0):
            print("Invalid id...")
            sys.exit(0)

        found = False
        for i in range(len(info[seccao])):
            if (info[seccao][i]['id'] == task_id):
                del info[seccao][i]
                found = True
                break

        if (found is False):
            print("Invalid id...")
        else:
            info = normalize(info)
            writeTasks(info)
    elif (len(sys.argv) == 4 and sys.argv[1] == "done"):
        info = readTasks()
        seccao = sys.argv[2]
        if (seccao not in info):
            print("Section doesn't exist...")
            sys.exit(0)

        # Validate task ID is a valid integer
        try:
            task_id = int(sys.argv[3])
        except ValueError:
            print(f"Error: Task ID must be a number, got '{sys.argv[3]}'")
            sys.exit(1)

        if (task_id > len(info[seccao]) or task_id <= 0):
            print("Invalid id...")
            sys.exit(0)

        found = False
        for i in range(len(info[seccao])):
            if (info[seccao][i]['id'] == task_id):
                # Toggle done status (backwards compatible)
                current_status = info[seccao][i].get('done', False)
                info[seccao][i]['done'] = not current_status
                found = True
                break

        if (found is False):
            print("Invalid id...")
        else:
            writeTasks(info)
            prettyprint(readTasks())
    elif (len(sys.argv) == 2 and sys.argv[1] == "dates"):
        info = readTasks()
        info_with_dates = {}

        try:
            for sec in info:
                if not isinstance(info[sec], list):
                    continue
                for i in info[sec]:
                    if isinstance(i, dict) and i.get("date", EMPTY_DATE) != EMPTY_DATE:
                        if (sec not in info_with_dates):
                            info_with_dates[sec] = []
                        info_with_dates[sec].append(i)
            prettyprint(info_with_dates)
        except Exception as e:
            print(f"Error: Unable to filter tasks by date.")
            print(f"Details: {str(e)}")

    elif (len(sys.argv) == 2 and sys.argv[1] == "today"):
        info = readTasks()
        info_with_dates = {}
        todays_date = datetime.now().strftime("%d/%m")

        try:
            for sec in info:
                if not isinstance(info[sec], list):
                    continue
                for i in info[sec]:
                    if isinstance(i, dict) and i.get("date", "") == todays_date:
                        if (sec not in info_with_dates):
                            info_with_dates[sec] = []
                        info_with_dates[sec].append(i)
            prettyprint(info_with_dates)
        except Exception as e:
            print(f"Error: Unable to filter tasks by today's date.")
            print(f"Details: {str(e)}")
    elif (len(sys.argv) == 2 and sys.argv[1] == "pending"):
        info = readTasks()
        info_pending = {}

        try:
            for sec in info:
                if not isinstance(info[sec], list):
                    continue
                for i in info[sec]:
                    # Backwards compatibility: treat tasks without 'done' field as pending
                    if isinstance(i, dict) and not i.get('done', False):
                        if (sec not in info_pending):
                            info_pending[sec] = []
                        info_pending[sec].append(i)
            prettyprint(info_pending)
        except Exception as e:
            print(f"Error: Unable to filter pending tasks.")
            print(f"Details: {str(e)}")
    elif (len(sys.argv) == 2 and sys.argv[1] == "help"):
        print("$ todo" + " " * 39 + "-> Show the tasks for each section")
        print("$ todo add \"task\" [\"date\"]" + " " * 19 + f"-> New task to the \"{DEFAULT_SECTION}\" section")
        print("$ todo add \"section_name\" \"task\" [\"date\"]" + " " * 4 + "-> New task to a section")
        print("$ todo rm \"section_name\" \"id-task\"" + " " * 11 + "-> Removes task from a section")
        print("$ todo rs \"section_name\"" + " " * 21 + "-> Removes a section")
        print("$ todo done \"section_name\" \"id-task\"" + " " * 9 + "-> Toggles task completion status")
        print("$ todo dates" + " " * 33 + "-> Shows the tasks with deadline dates")
        print("$ todo today" + " " * 33 + "-> Shows the tasks with today's deadline date")
        print("$ todo pending" + " " * 31 + "-> Shows only incomplete tasks")
    else:
        print(sys.argv)
        print("Invalid arguments!")


if __name__ == '__main__':
    main()
