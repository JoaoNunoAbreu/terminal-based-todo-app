# To-do App

## Functionalities

- Create/remove to-do's.
- Create/remove a section (ex: School, Movies, Daily tasks, etc).
- Show the tasks for each section.

<img src="https://i.imgur.com/gj8IdkJ.png" alt="drawing" width="500"/>

<img src="https://i.imgur.com/KRlFGty.png" alt="drawing" width="500"/>

## Installation

1. Type `cd` in your terminal to go to your home directory.
2. Clone the repo.
3. Add the following line to your `.bashrc` or `.zshrc` file:

```bash
alias todo="python3 ~/terminal-based-todo-app/main.py"
```
4. Restart your terminal.
5. Done!

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

- Shows the tasks with deadline dates.

```bash
$ todo dates
```

- Shows the tasks with today's deadline date

```bash
$ todo today
```

- Shows all the possible commands.

```bash
$ todo help
```
