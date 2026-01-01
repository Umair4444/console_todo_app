# Console Todo App

A command-line interface application for managing to-do tasks. This application allows you to add, view, update, complete, and delete tasks directly from your terminal.

## Features

- Add new tasks with descriptions
- List all tasks with completion status
- Mark tasks as complete/incomplete
- Update task descriptions
- Delete tasks
- Import/export tasks to/from JSON files
- Persistent local storage using JSON format
- Atomic write operations to prevent data corruption

## Installation

1. Make sure you have Python 3.8+ installed
2. Clone or download this repository
3. Install the package in development mode:

```bash
pip install -e .
```

## Usage

### Adding a Task
```bash
todo add "Buy groceries"
```

### Viewing Tasks
```bash
# View all tasks
todo list

# View only incomplete tasks
todo list --incomplete

# View only completed tasks
todo list --completed
```

### Updating a Task
```bash
# Update a task description
todo update 1 "Buy groceries and cook dinner"
```

### Marking Tasks as Complete
```bash
# Mark a task as complete
todo complete 1

# Mark a task as incomplete
todo incomplete 1
```

### Deleting a Task
```bash
# Delete a task
todo delete 1
```

### Importing and Exporting Tasks
```bash
# Export tasks to JSON
todo export tasks.json

# Import tasks from JSON
todo import tasks.json
```

### Help
```bash
# Show help information
todo --help
```

## Examples

```bash
# Add multiple tasks
todo add "Write report"
todo add "Schedule meeting"
todo add "Review code"

# View all tasks
todo list

# Mark the first task as complete
todo complete 1

# Update a task
todo update 2 "Schedule team meeting"

# Export your tasks
todo export my_tasks.json
```

## Data Storage

Tasks are stored in a JSON file. By default, this file is located at `~/.todo_app/tasks.json` (in your home directory). You can change this location by setting the `TODO_TASKS_FILE` environment variable.

## Architecture

The application follows a modular architecture:
- **Models**: Define the data structures (TodoItem)
- **Services**: Handle business logic (TodoService)
- **Storage**: Manage data persistence (FileStorage)
- **CLI**: Handle command-line interface (CLIApp)
- **Utils**: Provide helper functions (validation, performance monitoring, etc.)