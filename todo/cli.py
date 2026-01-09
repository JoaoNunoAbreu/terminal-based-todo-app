"""Command-line interface for the todo application."""

import sys

from . import commands


def main():
    """Parse command-line arguments and dispatch to appropriate handler."""
    args = sys.argv[1:]  # Skip program name
    argc = len(args)

    if argc == 0:
        # No arguments: show all tasks
        commands.cmd_show()

    elif args[0] == "add" and argc in [2, 3, 4]:
        # add command with 1-3 additional arguments
        commands.cmd_add(args[1:])

    elif args[0] == "rs" and argc == 2:
        # Remove section
        commands.cmd_remove_section(args[1])

    elif args[0] == "rm" and argc == 3:
        # Remove task
        commands.cmd_remove_task(args[1], args[2])

    elif args[0] == "done" and argc == 3:
        # Toggle done status
        commands.cmd_toggle_done(args[1], args[2])

    elif args[0] == "dates" and argc == 1:
        # Show tasks with dates
        commands.cmd_show_with_dates()

    elif args[0] == "today" and argc == 1:
        # Show today's tasks
        commands.cmd_show_today()

    elif args[0] == "pending" and argc == 1:
        # Show pending tasks
        commands.cmd_show_pending()

    elif args[0] == "completed" and argc == 1:
        # Show completed tasks
        commands.cmd_show_completed()

    elif args[0] == "overdue" and argc == 1:
        # Show overdue tasks
        commands.cmd_show_overdue()

    elif args[0] == "help" and argc == 1:
        # Show help
        commands.cmd_help()

    else:
        print(sys.argv)
        print("Invalid arguments!")
