# Quickstart Guide: CLI Menu Loop

## Running the Application

To run the CLI menu loop application, execute the following command from the project root:

```bash
python run_todo.py
```

## Using the Menu System

Once the application starts, you will see a menu with numbered options. To select an option:

1. Read the available options displayed on the screen
2. Enter the number or letter corresponding to your desired option
3. Press Enter to confirm your selection

## Available Options

The main menu typically includes options such as:
- Add a new todo item
- List all todo items
- Update an existing todo item
- Delete a todo item
- Exit the application

## Exiting the Application

You can exit the application in several ways:
- Select the "Exit" option from the menu
- Press 'x' followed by Enter, then press 'x' again followed by Enter
- Press 'X' followed by Enter, then press 'X' again followed by Enter
- Press 'ESC' followed by Enter (if using standard input)

## Error Handling

If you enter an invalid option, the application will display an error message and return to the main menu. Simply select a valid option to continue.

## Data Persistence

Your todo items are automatically saved to a local JSON file. The data persists between application sessions, so your todos will still be there when you run the application again.