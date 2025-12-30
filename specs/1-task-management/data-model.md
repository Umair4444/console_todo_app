# Data Model: Task Management

## Task Entity

### Fields
- **id** (int): Unique identifier for the task, auto-incremented
- **description** (str): The task description text
- **completed** (bool): Whether the task is completed (default: False)
- **created_at** (datetime): Timestamp when the task was created
- **updated_at** (datetime): Timestamp when the task was last modified

### Validation Rules
- **id**: Must be unique, auto-generated
- **description**: Required, must not be empty or whitespace only
- **completed**: Boolean value, default False
- **created_at**: Auto-generated on creation
- **updated_at**: Auto-generated/updated on any modification

### State Transitions
- **New Task**: created_at set, completed = False
- **Updated Task**: updated_at updated, other fields modified as needed
- **Completed Task**: completed = True, updated_at updated
- **Reopened Task**: completed = False, updated_at updated

## Storage Model

### File Format
- **Format**: JSON
- **Structure**: Array of Task objects
- **Location**: Local file (tasks.json in user's home directory or app directory)

### Example
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false,
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z"
  },
  {
    "id": 2,
    "description": "Finish report",
    "completed": true,
    "created_at": "2025-12-30T09:30:00Z",
    "updated_at": "2025-12-30T11:15:00Z"
  }
]
```