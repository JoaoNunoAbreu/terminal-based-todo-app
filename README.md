# To-do App

## Functionalities

* Create/remove to-do's.
* Create/remove a section (ex: School, Movies, Daily tasks, etc).
* Show the tasks for each section.

<img src="https://i.imgur.com/05jNN4e.png" alt="drawing" width="500"/>

## Installation

- Move this folder to a definitive directory, otherwise it will be necessary to run the install script again.

```bash 
$ git clone https://github.com/JoaoNunoAbreu/terminal-based-todo-app
$ cd terminal-based-todo-app-main
$ chmod +x install
$ sh install
```

## Commands

* Show the tasks for each section

```bash
$ todo
```

* Adds a new task to the "GENERAL" section, and creates it if it didn't exist yet. Deadline date is optional.

```bash
$ todo add "task" ["date"]
```

* Adds a new task to a section, and creates it if it didn't exist yet. Deadline date is optional.

```bash
$ todo add "section_name" "task" ["date"]
```

* Removes a task from a section.

```bash
$ todo rm "section_name" "id-task"
```

* Removes a section, and all the tasks belonging to that section.

```bash
$ todo rs "section_name"
```

* Shows the tasks with deadline dates.

```bash
$ todo dates
```

* Shows all the possible commands.

```bash
$ todo help
```
