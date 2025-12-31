# Data Model: CLI Menu Loop

## Todo Item Entity

**Fields**:
- id: int (unique identifier for the todo item)
- title: str (the title or description of the todo item)
- completed: bool (indicates whether the todo item is completed)
- created_at: str (timestamp when the item was created, ISO 8601 format)
- updated_at: str (timestamp when the item was last updated, ISO 8601 format)

**Validation Rules**:
- id must be a positive integer
- title must not be empty
- completed must be a boolean value
- created_at and updated_at must be valid ISO 8601 timestamps

## Todo Data Collection

**Structure**: A list of TodoItem entities stored in a JSON file

**File Format**: JSON with the following structure:
```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample todo item",
      "completed": false,
      "created_at": "2025-12-31T10:00:00Z",
      "updated_at": "2025-12-31T10:00:00Z"
    }
  ]
}
```

## Menu Options Entity

**Fields**:
- id: str (unique identifier for the menu option)
- display_text: str (the text displayed to the user for this option)
- action: str (the action or function to execute when this option is selected)

## Application State Entity

**Fields**:
- current_menu: str (the current menu being displayed)
- waiting_for_confirmation: bool (whether the app is waiting for exit confirmation)
- last_key_press: str (the last key pressed, for tracking 'x'/'X' sequence)