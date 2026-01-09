# To-do App

## Functionalities

- Create/remove to-do's.
- Create/remove a section (ex: School, Movies, Daily tasks, etc).
- Show the tasks for each section.

<img src="https://i.imgur.com/gj8IdkJ.png" alt="drawing" width="500"/>

<img src="https://i.imgur.com/KRlFGty.png" alt="drawing" width="500"/>

## Prerequisites

- Python 3.x

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/JoaoNunoAbreu/terminal-based-todo-app.git
cd terminal-based-todo-app
./install.sh
```

The install script will:
- Automatically detect your shell (bash/zsh)
- Set up the `todo` command pointing to wherever you cloned the repo
- Work from any directory - no need to clone to a specific location

### Manual Install

1. Clone the repo anywhere you like
2. Add this line to your `.bashrc` or `.zshrc` (adjust the path):
   ```bash
   alias todo="python3 /path/to/terminal-based-todo-app/main.py"
   ```
3. Restart your terminal or run `source ~/.bashrc`

## Uninstall

Run `./uninstall.sh` from the repo directory. This removes the alias but preserves your tasks in `data.json`.

## Troubleshooting

- **"command not found: todo"** - Run `source ~/.bashrc` (or `~/.zshrc`) or restart your terminal
- **"python3: command not found"** - Install Python 3 for your system
- **Permission denied** - Run `chmod +x install.sh` first

## Commands

- Show the tasks for each section

```bash
$ todo
```

- Adds a new task to the "GENERAL" section, and creates it if it didn't exist yet. Deadline date is optional.

```bash
$ todo add "task" ["date"]
```

- Adds a new task to a section, and creates it if it didn't exist yet. Deadline date is optional.

```bash
$ todo add "section_name" "task" ["date"]
```

- Removes a task from a section.

```bash
$ todo rm "section_name" "id-task"
```

- Removes a section, and all the tasks belonging to that section.

```bash
$ todo rs "section_name"
```

- Toggles the completion status of a task (marks as done/undone).

```bash
$ todo done "section_name" "id-task"
```

- Shows the tasks with deadline dates.

```bash
$ todo dates
```

- Shows the tasks with today's deadline date

```bash
$ todo today
```

- Shows only incomplete (pending) tasks

```bash
$ todo pending
```

- Shows all the possible commands.

```bash
$ todo help
```
