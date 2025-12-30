# API Contracts: Task Management

## CLI Command Contracts

### Add Task
```
Command: add <description>
Input: Task description (string)
Output: Task ID (integer) and success message
Error: If description is empty or only whitespace
```

### List Tasks
```
Command: list [options]
Input: Optional filters (--completed, --incomplete)
Output: Formatted list of tasks with ID, description, and completion status
Error: None (empty list if no tasks)
```

### Update Task
```
Command: update <id> <new_description>
Input: Task ID (integer), new description (string)
Output: Success message
Error: If task ID doesn't exist or description is empty
```

### Complete Task
```
Command: complete <id>
Input: Task ID (integer)
Output: Success message
Error: If task ID doesn't exist
```

### Incomplete Task
```
Command: incomplete <id>
Input: Task ID (integer)
Output: Success message
Error: If task ID doesn't exist
```

### Delete Task
```
Command: delete <id>
Input: Task ID (integer)
Output: Success message
Error: If task ID doesn't exist
```

### Export Tasks
```
Command: export <filename>
Input: Output filename (string)
Output: Success message
Error: If file cannot be written
```

### Import Tasks
```
Command: import <filename>
Input: Input filename (string)
Output: Success message and number of tasks imported
Error: If file cannot be read or is not valid JSON
```