import argparse
import sys
from typing import List, Optional
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItem


class CLIApp:
    """
    Command-line interface application for managing to-do tasks.
    """

    def __init__(self, service: TodoService = None):
        """
        Initialize the CLI application.

        Args:
            service: TodoService instance to handle business logic
        """
        self.service = service or TodoService()
        self.parser = self._create_parser()
        # For menu loop functionality
        self.running = True
        self.waiting_for_confirmation = False
        self.last_key_press = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.

        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog='todo',
            description='A command-line interface application for managing to-do tasks',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  todo add "Buy groceries"
  todo list
  todo list --completed
  todo list --incomplete
  todo complete 1
  todo incomplete 1
  todo update 1 "Buy groceries and cook dinner"
  todo delete 1
  todo export tasks.json
  todo import tasks.json
            """.strip()
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('description', nargs='+', help='Task description')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')
        list_group = list_parser.add_mutually_exclusive_group()
        list_group.add_argument('--completed', action='store_true', help='Show only completed tasks')
        list_group.add_argument('--incomplete', action='store_true', help='Show only incomplete tasks')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('id', type=int, help='Task ID')
        update_parser.add_argument('description', nargs='+', help='New task description')

        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
        complete_parser.add_argument('id', type=int, help='Task ID')

        # Incomplete command
        incomplete_parser = subparsers.add_parser('incomplete', help='Mark a task as incomplete')
        incomplete_parser.add_argument('id', type=int, help='Task ID')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='Task ID')

        # Export command
        export_parser = subparsers.add_parser('export', help='Export tasks to JSON file')
        export_parser.add_argument('filename', help='Output filename')

        # Import command
        import_parser = subparsers.add_parser('import', help='Import tasks from JSON file')
        import_parser.add_argument('filename', help='Input filename')

        return parser

    def run_menu_loop(self):
        """
        Run the interactive menu loop for the CLI application.
        """
        print("Welcome to the To-Do List Application!")
        print("Please select an option from the menu below:")

        while self.running:
            self.display_menu()
            try:
                user_input = input("\nEnter your choice: ").strip().lower()
                self.process_menu_selection(user_input)
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\nEnd of input. Goodbye!")
                break

    def display_menu(self):
        """
        Display the menu options to the user.
        """
        print("\n" + "="*40)
        print("TO-DO LIST APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Export Tasks")
        print("8. Import Tasks")
        print("9. Exit")
        print("="*40)
        print("Tip: Press 'x' or 'X' twice to exit quickly, or 'ESC' key to exit")
        print("Current status: " + ("Waiting for exit confirmation" if self.waiting_for_confirmation else "Running normally"))
    
    def process_menu_selection(self, user_input: str):
        """
        Process the user's menu selection.

        Args:
            user_input: The user's input from the menu
        """
        # Handle exit confirmation logic
        if self.waiting_for_confirmation:
            if user_input in ['x', 'yes', 'y']:
                print("Exiting application...")
                self.running = False
                return
            else:
                print("Exit cancelled.")
                self.waiting_for_confirmation = False
                return

        # Handle special exit keys
        if user_input == 'x':
            if self.last_key_press == 'x':
                # Double 'x' pressed, exit immediately
                print("Exiting application...")
                self.running = False
                return
            else:
                # First 'x' pressed, wait for confirmation or set flag
                print("Press 'x' again to confirm exit, or any other key to cancel")
                self.waiting_for_confirmation = True
                self.last_key_press = 'x'
                return
        else:
            # Reset the last key press if it wasn't an 'x'
            self.last_key_press = None

        # Handle ESC key (represented as \x1b in Python)
        if user_input == '\x1b':  # ESC character
            print("ESC pressed. Exiting application...")
            self.running = False
            return

        # Handle menu options
        try:
            choice = int(user_input)
        except ValueError:
            print(f"Invalid option: '{user_input}'. Please enter a number between 1-9.")
            return

        if choice == 1:
            self._handle_menu_add()
        elif choice == 2:
            self._handle_menu_list()
        elif choice == 3:
            self._handle_menu_update()
        elif choice == 4:
            self._handle_menu_delete()
        elif choice == 5:
            self._handle_menu_complete()
        elif choice == 6:
            self._handle_menu_incomplete()
        elif choice == 7:
            self._handle_menu_export()
        elif choice == 8:
            self._handle_menu_import()
        elif choice == 9:
            self._handle_menu_exit()
        else:
            print(f"Invalid option: {choice}. Please enter a number between 1-9.")

    def _handle_menu_add(self):
        """Handle adding a task via the menu."""
        try:
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task = self.service.add_task(description)
            print(f"Added task #{task.id}: {task.description}")
        except Exception as e:
            print(f"Error adding task: {e}")

    def _handle_menu_list(self):
        """Handle listing tasks via the menu."""
        try:
            print("\nSelect list option:")
            print("1. All tasks")
            print("2. Completed tasks only")
            print("3. Incomplete tasks only")

            list_choice = input("Enter your choice (1-3): ").strip()

            if list_choice == '1':
                tasks = self.service.get_all_tasks()
            elif list_choice == '2':
                tasks = self.service.get_completed_tasks()
            elif list_choice == '3':
                tasks = self.service.get_incomplete_tasks()
            else:
                print("Invalid choice. Showing all tasks.")
                tasks = self.service.get_all_tasks()

            if not tasks:
                print("No tasks found.")
                return

            # Print formatted task list
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"{task.id}. [{status}] {task.description}")
        except Exception as e:
            print(f"Error listing tasks: {e}")

    def _handle_menu_update(self):
        """Handle updating a task via the menu."""
        try:
            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task_id = int(task_id)
            description = input("Enter new task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task = self.service.update_task(task_id, description)
            print(f"Updated task #{task.id}: {task.description}")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error updating task: {e}")

    def _handle_menu_complete(self):
        """Handle marking a task as complete via the menu."""
        try:
            task_id = input("Enter task ID to mark complete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task_id = int(task_id)
            task = self.service.mark_task_complete(task_id)
            print(f"Marked task #{task.id} as complete: {task.description}")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error marking task complete: {e}")

    def _handle_menu_incomplete(self):
        """Handle marking a task as incomplete via the menu."""
        try:
            task_id = input("Enter task ID to mark incomplete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task_id = int(task_id)
            task = self.service.mark_task_incomplete(task_id)
            print(f"Marked task #{task.id} as incomplete: {task.description}")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error marking task incomplete: {e}")

    def _handle_menu_delete(self):
        """Handle deleting a task via the menu."""
        try:
            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task_id = int(task_id)
            task = self.service.delete_task(task_id)
            print(f"Deleted task #{task.id}: {task.description}")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def _handle_menu_export(self):
        """Handle exporting tasks via the menu."""
        try:
            filename = input("Enter filename to export to: ").strip()
            if not filename:
                print("Filename cannot be empty.")
                return

            count = self.service.export_tasks(filename)
            print(f"Exported {count} tasks to {filename}")
        except Exception as e:
            print(f"Error exporting tasks: {e}")

    def _handle_menu_import(self):
        """Handle importing tasks via the menu."""
        try:
            filename = input("Enter filename to import from: ").strip()
            if not filename:
                print("Filename cannot be empty.")
                return

            count = self.service.import_tasks(filename)
            print(f"Imported {count} tasks from {filename}")
        except Exception as e:
            print(f"Error importing tasks: {e}")

    def _handle_menu_exit(self):
        """Handle exiting the application via the menu."""
        print("Exiting application...")
        self.running = False

    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI application with the given arguments.
        If no arguments are provided, run the interactive menu loop.

        Args:
            args: List of command-line arguments. If None, uses sys.argv.

        Returns:
            Exit code (0 for success, non-zero for errors)
        """
        try:
            if args is None:
                args = sys.argv[1:]

            # If arguments are provided, use the original CLI command approach
            if args:
                parsed_args = self.parser.parse_args(args)

                # Handle each command
                if parsed_args.command == 'add':
                    return self._handle_add(parsed_args)
                elif parsed_args.command == 'list':
                    return self._handle_list(parsed_args)
                elif parsed_args.command == 'update':
                    return self._handle_update(parsed_args)
                elif parsed_args.command == 'complete':
                    return self._handle_complete(parsed_args)
                elif parsed_args.command == 'incomplete':
                    return self._handle_incomplete(parsed_args)
                elif parsed_args.command == 'delete':
                    return self._handle_delete(parsed_args)
                elif parsed_args.command == 'export':
                    return self._handle_export(parsed_args)
                elif parsed_args.command == 'import':
                    return self._handle_import(parsed_args)
                else:
                    self.parser.print_help()
                    return 1
            else:
                # No arguments provided, run the interactive menu loop
                self.run_menu_loop()
                return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_add(self, args) -> int:
        """Handle the 'add' command."""
        description = ' '.join(args.description)
        task = self.service.add_task(description)
        print(f"Added task #{task.id}: {task.description}")
        return 0
    
    def _handle_list(self, args) -> int:
        """Handle the 'list' command."""
        if args.completed:
            tasks = self.service.get_completed_tasks()
        elif args.incomplete:
            tasks = self.service.get_incomplete_tasks()
        else:
            tasks = self.service.get_all_tasks()
        
        if not tasks:
            print("No tasks found.")
            return 0
        
        # Print formatted task list
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"{task.id}. [{status}] {task.description}")
        
        return 0
    
    def _handle_update(self, args) -> int:
        """Handle the 'update' command."""
        description = ' '.join(args.description)
        try:
            task = self.service.update_task(args.id, description)
            print(f"Updated task #{task.id}: {task.description}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_complete(self, args) -> int:
        """Handle the 'complete' command."""
        try:
            task = self.service.mark_task_complete(args.id)
            print(f"Marked task #{task.id} as complete: {task.description}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_incomplete(self, args) -> int:
        """Handle the 'incomplete' command."""
        try:
            task = self.service.mark_task_incomplete(args.id)
            print(f"Marked task #{task.id} as incomplete: {task.description}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_delete(self, args) -> int:
        """Handle the 'delete' command."""
        try:
            task = self.service.delete_task(args.id)
            print(f"Deleted task #{task.id}: {task.description}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_export(self, args) -> int:
        """Handle the 'export' command."""
        try:
            count = self.service.export_tasks(args.filename)
            print(f"Exported {count} tasks to {args.filename}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_import(self, args) -> int:
        """Handle the 'import' command."""
        try:
            count = self.service.import_tasks(args.filename)
            print(f"Imported {count} tasks from {args.filename}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point for the CLI application."""
    app = CLIApp()
    # Pass command line arguments to the run method
    sys.exit(app.run())


if __name__ == "__main__":
    main()