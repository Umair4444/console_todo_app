# Quickstart Guide: Task Management CLI

## Installation

The task management CLI application is a Python application that can be run directly:

```bash
# Make sure you have Python 3.8+ installed
python --version

# Clone or download the application
git clone <repository-url>
cd <repository-directory>

# Run the application directly
python -m src.cli.cli_app --help
```

## Basic Usage

### Adding a Task
```bash
# Add a new task
python -m src.cli.cli_app add "Buy groceries"
```

### Viewing Tasks
```bash
# View all tasks
python -m src.cli.cli_app list

# View only incomplete tasks
python -m src.cli.cli_app list --incomplete

# View only completed tasks
python -m src.cli.cli_app list --completed
```

### Updating a Task
```bash
# Update a task description
python -m src.cli.cli_app update 1 "Buy groceries and cook dinner"
```

### Marking Tasks as Complete
```bash
# Mark a task as complete
python -m src.cli.cli_app complete 1

# Mark a task as incomplete
python -m src.cli.cli_app incomplete 1
```

### Deleting a Task
```bash
# Delete a task
python -m src.cli.cli_app delete 1
```

### Importing and Exporting Tasks
```bash
# Export tasks to JSON
python -m src.cli.cli_app export tasks.json

# Import tasks from JSON
python -m src.cli.cli_app import tasks.json
```

## Command Reference

```
Usage: cli_app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add        Add a new task
  list       List all tasks
  update     Update a task
  complete   Mark a task as complete
  incomplete Mark a task as incomplete
  delete     Delete a task
  export     Export tasks to JSON file
  import     Import tasks from JSON file
```

## Examples

```bash
# Add multiple tasks
python -m src.cli.cli_app add "Write report"
python -m src.cli.cli_app add "Schedule meeting"
python -m src.cli.cli_app add "Review code"

# View all tasks
python -m src.cli.cli_app list

# Mark the first task as complete
python -m src.cli.cli_app complete 1

# Update a task
python -m src.cli.cli_app update 2 "Schedule team meeting"

# Export your tasks
python -m src.cli.cli_app export my_tasks.json
```