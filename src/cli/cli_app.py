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
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI application with the given arguments.
        
        Args:
            args: List of command-line arguments. If None, uses sys.argv.
            
        Returns:
            Exit code (0 for success, non-zero for errors)
        """
        try:
            if args is None:
                args = sys.argv[1:]
            
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
            status = "X" if task.completed else "O"
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
    sys.exit(app.run())


if __name__ == "__main__":
    main()