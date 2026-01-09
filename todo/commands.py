"""Command handlers for todo operations."""

import sys
from datetime import datetime

from .config import DEFAULT_SECTION, EMPTY_DATE
from .storage import read_tasks, write_tasks
from .utils import create_task, normalize_ids
from .display import prettyprint


def cmd_show():
    """Display all tasks."""
    prettyprint(read_tasks())


def cmd_add(args):
    """Add a new task.

    Args format:
        ["task"]                           -> task to GENERAL section
        ["task", "DD/MM"]                  -> task with date to GENERAL section
        ["section", "task"]                -> task to custom section
        ["section", "task", "DD/MM"]       -> task with date to custom section
    """
    info = read_tasks()

    if len(args) == 1:
        # Just task, no section, no date
        if DEFAULT_SECTION not in info:
            info[DEFAULT_SECTION] = []
        create_task(info, DEFAULT_SECTION, args[0], EMPTY_DATE)

    elif len(args) == 2:
        # Could be (task, date) or (section, task)
        if "/" in args[1]:
            # task with date
            if DEFAULT_SECTION not in info:
                info[DEFAULT_SECTION] = []
            create_task(info, DEFAULT_SECTION, args[0], args[1])
        else:
            # section and task
            section = args[0]
            if section not in info:
                info[section] = []
            create_task(info, section, args[1], EMPTY_DATE)

    elif len(args) == 3:
        # section, task, date
        if "/" not in args[2]:
            print("Invalid date...")
            sys.exit(1)
        section = args[0]
        if section not in info:
            info[section] = []
        create_task(info, section, args[1], args[2])

    prettyprint(read_tasks())


def cmd_remove_section(section):
    """Remove an entire section and all its tasks."""
    info = read_tasks()
    if section not in info:
        print("Section doesn't exist...")
        sys.exit(0)
    del info[section]
    write_tasks(info)


def cmd_remove_task(section, task_id_str):
    """Remove a specific task from a section."""
    info = read_tasks()
    if section not in info:
        print("Section doesn't exist...")
        sys.exit(0)

    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"Error: Task ID must be a number, got '{task_id_str}'")
        sys.exit(1)

    if task_id > len(info[section]) or task_id <= 0:
        print("Invalid id...")
        sys.exit(0)

    found = False
    for i in range(len(info[section])):
        if info[section][i]['id'] == task_id:
            del info[section][i]
            found = True
            break

    if not found:
        print("Invalid id...")
    else:
        info = normalize_ids(info)
        write_tasks(info)


def cmd_toggle_done(section, task_id_str):
    """Toggle the completion status of a task."""
    info = read_tasks()
    if section not in info:
        print("Section doesn't exist...")
        sys.exit(0)

    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"Error: Task ID must be a number, got '{task_id_str}'")
        sys.exit(1)

    if task_id > len(info[section]) or task_id <= 0:
        print("Invalid id...")
        sys.exit(0)

    found = False
    for i in range(len(info[section])):
        if info[section][i]['id'] == task_id:
            current_status = info[section][i].get('done', False)
            info[section][i]['done'] = not current_status
            found = True
            break

    if not found:
        print("Invalid id...")
    else:
        write_tasks(info)
        prettyprint(read_tasks())


def cmd_show_with_dates():
    """Show only tasks that have deadline dates."""
    info = read_tasks()
    info_with_dates = {}

    try:
        for sec in info:
            if not isinstance(info[sec], list):
                continue
            for task in info[sec]:
                if isinstance(task, dict) and task.get("date", EMPTY_DATE) != EMPTY_DATE:
                    if sec not in info_with_dates:
                        info_with_dates[sec] = []
                    info_with_dates[sec].append(task)
        prettyprint(info_with_dates)
    except Exception as e:
        print(f"Error: Unable to filter tasks by date.")
        print(f"Details: {str(e)}")


def cmd_show_today():
    """Show tasks with today's deadline date."""
    info = read_tasks()
    info_with_dates = {}
    todays_date = datetime.now().strftime("%d/%m")

    try:
        for sec in info:
            if not isinstance(info[sec], list):
                continue
            for task in info[sec]:
                if isinstance(task, dict) and task.get("date", "") == todays_date:
                    if sec not in info_with_dates:
                        info_with_dates[sec] = []
                    info_with_dates[sec].append(task)
        prettyprint(info_with_dates)
    except Exception as e:
        print(f"Error: Unable to filter tasks by today's date.")
        print(f"Details: {str(e)}")


def cmd_show_pending():
    """Show only incomplete (pending) tasks."""
    info = read_tasks()
    info_pending = {}

    try:
        for sec in info:
            if not isinstance(info[sec], list):
                continue
            for task in info[sec]:
                if isinstance(task, dict) and not task.get('done', False):
                    if sec not in info_pending:
                        info_pending[sec] = []
                    info_pending[sec].append(task)
        prettyprint(info_pending)
    except Exception as e:
        print(f"Error: Unable to filter pending tasks.")
        print(f"Details: {str(e)}")


def cmd_show_completed():
    """Show only completed tasks."""
    info = read_tasks()
    info_completed = {}

    try:
        for sec in info:
            if not isinstance(info[sec], list):
                continue
            for task in info[sec]:
                if isinstance(task, dict) and task.get('done', False):
                    if sec not in info_completed:
                        info_completed[sec] = []
                    info_completed[sec].append(task)
        prettyprint(info_completed)
    except Exception as e:
        print(f"Error: Unable to filter completed tasks.")
        print(f"Details: {str(e)}")


def cmd_show_overdue():
    """Show tasks that are past their deadline date."""
    info = read_tasks()
    info_overdue = {}
    today = datetime.now()

    try:
        for sec in info:
            if not isinstance(info[sec], list):
                continue
            for task in info[sec]:
                task_date = task.get("date", EMPTY_DATE)
                if isinstance(task, dict) and task_date != EMPTY_DATE:
                    try:
                        task_datetime = datetime.strptime(f"{task_date}/{today.year}", "%d/%m/%Y")
                        if task_datetime.date() < today.date():
                            if sec not in info_overdue:
                                info_overdue[sec] = []
                            info_overdue[sec].append(task)
                    except ValueError:
                        continue
        prettyprint(info_overdue)
    except Exception as e:
        print(f"Error: Unable to filter overdue tasks.")
        print(f"Details: {str(e)}")


def cmd_help():
    """Display help message with all available commands."""
    print("$ todo" + " " * 39 + "-> Show the tasks for each section")
    print(f"$ todo add \"task\" [\"date\"]" + " " * 19 + f"-> New task to the \"{DEFAULT_SECTION}\" section")
    print("$ todo add \"section_name\" \"task\" [\"date\"]" + " " * 4 + "-> New task to a section")
    print("$ todo rm \"section_name\" \"id-task\"" + " " * 11 + "-> Removes task from a section")
    print("$ todo rs \"section_name\"" + " " * 21 + "-> Removes a section")
    print("$ todo done \"section_name\" \"id-task\"" + " " * 9 + "-> Toggles task completion status")
    print("$ todo dates" + " " * 33 + "-> Shows the tasks with deadline dates")
    print("$ todo today" + " " * 33 + "-> Shows the tasks with today's deadline date")
    print("$ todo overdue" + " " * 31 + "-> Shows tasks with past deadline dates")
    print("$ todo pending" + " " * 31 + "-> Shows only incomplete tasks")
    print("$ todo completed" + " " * 29 + "-> Shows only completed tasks")
