import argparse
import sys
from typing import List, Optional
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItem
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import print as rich_print

import functools

# Initialize rich console
console = Console()

# Create a custom print function that handles encoding properly
def safe_print(*args, **kwargs):
    """Print function that handles Unicode characters properly on all platforms."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Replace Unicode characters with ASCII equivalents
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Replace common Unicode characters with ASCII equivalents
                arg = arg.replace('✓', 'X').replace('✗', 'O')
            safe_args.append(arg)
        print(*safe_args, **kwargs)


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
            exit_on_error=False,  # Don't exit on error, raise exception instead
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
        Run the interactive menu loop for the CLI application with rich formatting.
        """
        console.print("[bold green]Welcome to the To-Do List Application![/bold green]")
        console.print("[blue]Please select an option from the menu below:[/blue]")

        while self.running:
            self.display_menu()
            try:
                user_input = input("\nEnter your choice: ").strip().lower()
                self.process_menu_selection(user_input)
            except KeyboardInterrupt:
                console.print("\n\n[red]Application interrupted. Goodbye![/red]")
                break
            except EOFError:
                console.print("\n\n[red]End of input. Goodbye![/red]")
                break

    def execute_menu_option(self, option_num):
        """
        Execute the menu option based on the selected number.

        Args:
            option_num: The selected menu option number (1-9)
        """
        if option_num == 1:
            self._handle_menu_add()
        elif option_num == 2:
            self._handle_menu_list()
        elif option_num == 3:
            self._handle_menu_update()
        elif option_num == 4:
            self._handle_menu_delete()
        elif option_num == 5:
            self._handle_menu_complete()
        elif option_num == 6:
            self._handle_menu_incomplete()
        elif option_num == 7:
            self._handle_menu_export()
        elif option_num == 8:
            self._handle_menu_import()
        elif option_num == 9:
            self._handle_menu_exit()
        else:
            console.print(f"[red]Invalid option: {option_num}. Please enter a number between 1-9.[/red]")

    def display_menu(self):
        """
        Display the menu options to the user with rich formatting.
        """
        console.print("\n[bold blue]┌─────────────────────────────────────┐[/bold blue]")
        console.print("[bold blue]│        📋 TO-DO LIST APP           │[/bold blue]")
        console.print("[bold blue]└─────────────────────────────────────┘[/bold blue]")

        # Create a rich table for menu options
        table = Table(show_header=False, box=None)
        table.add_column(style="dim cyan", no_wrap=True)
        table.add_column(style="green")

        table.add_row("1", "➕ Add Task")
        table.add_row("2", "📋 List Tasks")
        table.add_row("3", "✏️ Update Task")
        table.add_row("4", "🗑️ Delete Task")
        table.add_row("5", "✅ Mark Task Complete")
        table.add_row("6", "↩️ Mark Task Incomplete")
        table.add_row("7", "📤 Export Tasks")
        table.add_row("8", "📥 Import Tasks")
        table.add_row("9", "🚪 Exit")

        console.print(table)

        console.print("\n[yellow]💡 Tip:[/yellow] Enter option number (1-9) to select")
        console.print("       Press 'x' twice or 'Ctrl+C' to exit")

        status_text = "⚠️ WAITING FOR EXIT CONFIRMATION" if self.waiting_for_confirmation else "✅ RUNNING"
        console.print(f"\n[bold]Status:[/bold] {status_text}")
        console.print(f"[bold blue]┌─────────────────────────────────────────────────────────┐[/bold blue]")
        console.print(f"[bold blue]│[/bold blue] [bold]Enter number to select option[/bold]                         [bold blue]│[/bold blue]")
        console.print(f"[bold blue]└─────────────────────────────────────────────────────────┘[/bold blue]")
    
    def process_menu_selection(self, user_input: str):
        """
        Process the user's menu selection with rich formatting.

        Args:
            user_input: The user's input from the menu
        """
        # Handle exit confirmation logic
        if self.waiting_for_confirmation:
            if user_input in ['x', 'yes', 'y']:
                console.print("[red]Exiting application...[/red]")
                self.running = False
                return
            else:
                console.print("[yellow]Exit cancelled.[/yellow]")
                self.waiting_for_confirmation = False
                return

        # Handle special exit keys
        if user_input == 'x':
            if self.last_key_press == 'x':
                # Double 'x' pressed, exit immediately
                console.print("[red]Exiting application...[/red]")
                self.running = False
                return
            else:
                # First 'x' pressed, wait for confirmation or set flag
                console.print("[yellow]Press 'x' again to confirm exit, or any other key to cancel[/yellow]")
                self.waiting_for_confirmation = True
                self.last_key_press = 'x'
                return
        else:
            # Reset the last key press if it wasn't an 'x'
            self.last_key_press = None

        # Handle ESC key (represented as \x1b in Python)
        # On Windows and other systems, ESC might be captured as a standalone character
        # or as part of a sequence
        if user_input == '\x1b' or user_input.startswith('\x1b'):  # ESC character or sequence
            console.print("[red]ESC pressed. Exiting application...[/red]")
            self.running = False
            return

        # Handle menu options
        try:
            choice = int(user_input)
        except ValueError:
            console.print(f"[red]Invalid option: '{user_input}'. Please enter a number between 1-9.[/red]")
            return

        # Execute the selected menu option
        self.execute_menu_option(choice)

    def _handle_menu_add(self):
        """Handle adding a task via the menu with rich formatting."""
        try:
            description = input("Enter task description: ").strip()
            if not description:
                console.print("[red]Task description cannot be empty.[/red]")
                return

            task = self.service.add_task(description)
            console.print(f"[green]Added task #[/green][bold]{task.id}[/bold][green]: {task.description}[/green]")
        except Exception as e:
            console.print(f"[red]Error adding task: {e}[/red]")

    def _handle_menu_list(self):
        """Handle listing tasks via the menu with rich formatting."""
        try:
            console.print("\n[bold]Select list option:[/bold]")
            console.print("1. All tasks")
            console.print("2. Completed tasks only")
            console.print("3. Incomplete tasks only")

            list_choice = input("Enter your choice (1-3): ").strip()

            if list_choice == '1':
                tasks = self.service.get_all_tasks()
            elif list_choice == '2':
                tasks = self.service.get_completed_tasks()
            elif list_choice == '3':
                tasks = self.service.get_incomplete_tasks()
            else:
                console.print("[yellow]Invalid choice. Showing all tasks.[/yellow]")
                tasks = self.service.get_all_tasks()

            if not tasks:
                console.print("[yellow]No tasks found.[/yellow]")
                return

            # Create a rich table for tasks
            table = Table(title="Tasks", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Status", style="green")
            table.add_column("Description", style="white")

            # Add tasks to the table
            for task in tasks:
                status_emoji = "✅" if task.completed else "📝"
                status_text = "[green]Completed[/green]" if task.completed else "[yellow]Active[/yellow]"
                table.add_row(str(task.id), f"{status_emoji} {status_text}", task.description)

            console.print(table)
        except Exception as e:
            console.print(f"[red]Error listing tasks: {e}[/red]")

    def _handle_menu_update(self):
        """Handle updating a task via the menu with rich formatting."""
        try:
            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                console.print("[red]Task ID cannot be empty.[/red]")
                return

            task_id = int(task_id)
            description = input("Enter new task description: ").strip()
            if not description:
                console.print("[red]Task description cannot be empty.[/red]")
                return

            task = self.service.update_task(task_id, description)
            console.print(f"[green]Updated task #[/green][bold]{task.id}[/bold][green]: {task.description}[/green]")
        except ValueError:
            console.print("[red]Invalid task ID. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[red]Error updating task: {e}[/red]")

    def _handle_menu_complete(self):
        """Handle marking a task as complete via the menu with rich formatting."""
        try:
            task_id = input("Enter task ID to mark complete: ").strip()
            if not task_id:
                console.print("[red]Task ID cannot be empty.[/red]")
                return

            task_id = int(task_id)
            task = self.service.mark_task_complete(task_id)
            console.print(f"[green]Marked task #[/green][bold]{task.id}[/bold][green] as complete: {task.description}[/green]")
        except ValueError:
            console.print("[red]Invalid task ID. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[red]Error marking task complete: {e}[/red]")

    def _handle_menu_incomplete(self):
        """Handle marking a task as incomplete via the menu with rich formatting."""
        try:
            task_id = input("Enter task ID to mark incomplete: ").strip()
            if not task_id:
                console.print("[red]Task ID cannot be empty.[/red]")
                return

            task_id = int(task_id)
            task = self.service.mark_task_incomplete(task_id)
            console.print(f"[green]Marked task #[/green][bold]{task.id}[/bold][green] as incomplete: {task.description}[/green]")
        except ValueError:
            console.print("[red]Invalid task ID. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[red]Error marking task incomplete: {e}[/red]")

    def _handle_menu_delete(self):
        """Handle deleting a task via the menu with rich formatting."""
        try:
            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                console.print("[red]Task ID cannot be empty.[/red]")
                return

            task_id = int(task_id)
            task = self.service.delete_task(task_id)
            console.print(f"[red]Deleted task #[/red][bold]{task.id}[/bold][red]: {task.description}[/red]")
        except ValueError:
            console.print("[red]Invalid task ID. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[red]Error deleting task: {e}[/red]")

    def _handle_menu_export(self):
        """Handle exporting tasks via the menu with rich formatting."""
        try:
            filename = input("Enter filename to export to: ").strip()
            if not filename:
                console.print("[red]Filename cannot be empty.[/red]")
                return

            count = self.service.export_tasks(filename)
            console.print(f"[green]Exported {count} tasks to {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error exporting tasks: {e}[/red]")

    def _handle_menu_import(self):
        """Handle importing tasks via the menu with rich formatting."""
        try:
            filename = input("Enter filename to import from: ").strip()
            if not filename:
                console.print("[red]Filename cannot be empty.[/red]")
                return

            count = self.service.import_tasks(filename)
            console.print(f"[green]Imported {count} tasks from {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error importing tasks: {e}[/red]")

    def _handle_menu_exit(self):
        """Handle exiting the application via the menu with rich formatting."""
        console.print("[red]Exiting application...[/red]")
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
                try:
                    # Parse arguments without exiting on error
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
                except SystemExit:
                    # argparse may still raise SystemExit in some cases, catch and return error code
                    return 2
                except argparse.ArgumentError as e:
                    print(f"Error parsing arguments: {e}", file=sys.stderr)
                    self.parser.print_help()
                    return 2
            else:
                # No arguments provided, run the interactive menu loop
                self.run_menu_loop()
                return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_add(self, args) -> int:
        """Handle the 'add' command with rich formatting."""
        description = ' '.join(args.description)
        task = self.service.add_task(description)
        console.print(f"[green]Added task #[/green][bold]{task.id}[/bold][green]: {task.description}[/green]")
        return 0
    
    def _handle_list(self, args) -> int:
        """Handle the 'list' command with rich formatting."""
        if args.completed:
            tasks = self.service.get_completed_tasks()
        elif args.incomplete:
            tasks = self.service.get_incomplete_tasks()
        else:
            tasks = self.service.get_all_tasks()

        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return 0

        # Create a rich table for tasks
        table = Table(title="Tasks", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Description", style="white")

        # Add tasks to the table
        for task in tasks:
            status_emoji = "✅" if task.completed else "📝"
            status_text = "[green]Completed[/green]" if task.completed else "[yellow]Active[/yellow]"
            table.add_row(str(task.id), f"{status_emoji} {status_text}", task.description)

        console.print(table)

        return 0
    
    def _handle_update(self, args) -> int:
        """Handle the 'update' command with rich formatting."""
        description = ' '.join(args.description)
        try:
            task = self.service.update_task(args.id, description)
            console.print(f"[green]Updated task #[/green][bold]{task.id}[/bold][green]: {task.description}[/green]")
            return 0
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1
    
    def _handle_complete(self, args) -> int:
        """Handle the 'complete' command with rich formatting."""
        try:
            task = self.service.mark_task_complete(args.id)
            console.print(f"[green]Marked task #[/green][bold]{task.id}[/bold][green] as complete: {task.description}[/green]")
            return 0
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1
    
    def _handle_incomplete(self, args) -> int:
        """Handle the 'incomplete' command with rich formatting."""
        try:
            task = self.service.mark_task_incomplete(args.id)
            console.print(f"[green]Marked task #[/green][bold]{task.id}[/bold][green] as incomplete: {task.description}[/green]")
            return 0
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1
    
    def _handle_delete(self, args) -> int:
        """Handle the 'delete' command with rich formatting."""
        try:
            task = self.service.delete_task(args.id)
            console.print(f"[red]Deleted task #[/red][bold]{task.id}[/bold][red]: {task.description}[/red]")
            return 0
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1
    
    def _handle_export(self, args) -> int:
        """Handle the 'export' command with rich formatting."""
        try:
            count = self.service.export_tasks(args.filename)
            console.print(f"[green]Exported {count} tasks to {args.filename}[/green]")
            return 0
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1
    
    def _handle_import(self, args) -> int:
        """Handle the 'import' command with rich formatting."""
        try:
            count = self.service.import_tasks(args.filename)
            console.print(f"[green]Imported {count} tasks from {args.filename}[/green]")
            return 0
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
            return 1


def main():
    """Main entry point for the CLI application."""
    app = CLIApp()
    # Pass command line arguments to the run method
    sys.exit(app.run())


if __name__ == "__main__":
    main()