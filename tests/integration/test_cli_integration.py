"""
Integration tests for the CLI application.
"""
import pytest
import tempfile
import os
import json
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestAddTaskIntegration:
    """Integration tests for the add task user journey."""
    
    def test_add_task_then_list_task(self, capsys, temp_file):
        """Test the complete user journey: add a task, then list tasks."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task
        result = app.run(['add', 'Buy', 'groceries'])
        assert result == 0
        
        # Verify the output of the add command
        captured = capsys.readouterr()
        assert "Added task #1: Buy groceries" in captured.out
        
        # List tasks
        result = app.run(['list'])
        assert result == 0
        
        # Capture and verify the list output
        captured = capsys.readouterr()
        assert "1. [○] Buy groceries" in captured.out  # ○ indicates incomplete task
    
    def test_add_multiple_tasks_then_list_all(self, capsys, temp_file):
        """Test adding multiple tasks and then listing them all."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add multiple tasks
        result1 = app.run(['add', 'Buy', 'groceries'])
        result2 = app.run(['add', 'Finish', 'report'])
        result3 = app.run(['add', 'Call', 'mom'])
        
        assert result1 == 0
        assert result2 == 0
        assert result3 == 0
        
        # Clear the output from the add commands
        capsys.readouterr()
        
        # List all tasks
        result = app.run(['list'])
        assert result == 0
        
        # Capture and verify the list output
        captured = capsys.readouterr()
        
        # Verify all tasks are present
        assert "1. [○] Buy groceries" in captured.out
        assert "2. [○] Finish report" in captured.out
        assert "3. [○] Call mom" in captured.out
    
    def test_add_task_then_mark_complete_then_list(self, capsys, temp_file):
        """Test adding a task, marking it complete, then listing."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task
        result = app.run(['add', 'Buy', 'groceries'])
        assert result == 0
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Mark the task as complete
        result = app.run(['complete', '1'])
        assert result == 0
        
        # Verify the output of the complete command
        captured = capsys.readouterr()
        assert "Marked task #1 as complete: Buy groceries" in captured.out
        
        # List tasks
        result = app.run(['list'])
        assert result == 0
        
        # Capture and verify the list output
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out  # ✓ indicates completed task


class TestMarkCompleteIntegration:
    """Integration tests for the mark complete user journey."""

    def test_add_task_complete_task_list_tasks(self, capsys, temp_file):
        """Test the complete user journey: add task, complete task, list tasks."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)

        # Add a task
        result = app.run(['add', 'Buy', 'groceries'])
        assert result == 0

        # Clear the output from the add command
        capsys.readouterr()

        # Mark the task as complete
        result = app.run(['complete', '1'])
        assert result == 0

        # Verify the output of the complete command
        captured = capsys.readouterr()
        assert "Marked task #1 as complete: Buy groceries" in captured.out

        # List tasks to verify the status change
        result = app.run(['list'])
        assert result == 0

        # Verify the task appears as completed in the list
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out  # ✓ indicates completed task

    def test_add_multiple_tasks_complete_some_list_with_filters(self, capsys, temp_file):
        """Test adding multiple tasks, completing some, and listing with filters."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)

        # Add multiple tasks
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        app.run(['add', 'Call', 'mom'])

        # Clear the output from the add commands
        capsys.readouterr()

        # Complete some tasks
        result1 = app.run(['complete', '1'])
        result2 = app.run(['complete', '3'])
        assert result1 == 0
        assert result2 == 0

        # Clear the output from the complete commands
        capsys.readouterr()

        # List all tasks
        result = app.run(['list'])
        assert result == 0

        # Verify all tasks are listed with correct status
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out  # Completed
        assert "2. [○] Finish report" in captured.out  # Incomplete
        assert "3. [✓] Call mom" in captured.out      # Completed

        # List only completed tasks
        result = app.run(['list', '--completed'])
        assert result == 0

        # Verify only completed tasks are listed
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out
        assert "3. [✓] Call mom" in captured.out
        assert "Finish report" not in captured.out

        # List only incomplete tasks
        result = app.run(['list', '--incomplete'])
        assert result == 0

        # Verify only incomplete tasks are listed
        captured = capsys.readouterr()
        assert "2. [○] Finish report" in captured.out
        assert "Buy groceries" not in captured.out
        assert "Call mom" not in captured.out


class TestImportExportIntegration:
    """Integration tests for the import/export user journey."""
    
    def test_export_tasks_then_import_to_new_storage(self, capsys, temp_file):
        """Test the complete user journey: add tasks, export them, then import to a new storage."""
        # Create original storage with some tasks
        original_storage = FileStorage(str(temp_file))
        original_service = TodoService(storage=original_storage)
        original_app = CLIApp(service=original_service)
        
        # Add some tasks to the original storage
        original_app.run(['add', 'Buy', 'groceries'])
        original_app.run(['add', 'Finish', 'report'])
        original_app.run(['complete', '1'])  # Complete the first task
        
        # Clear the output from the add/complete commands
        capsys.readouterr()
        
        # Export the tasks to a file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_export_file:
            export_path = temp_export_file.name
        
        result = original_app.run(['export', export_path])
        assert result == 0
        
        # Verify the export output
        captured = capsys.readouterr()
        assert "Exported 2 tasks to" in captured.out
        
        # Create a new storage and import the tasks
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_import_file:
            import_path = temp_import_file.name
        
        try:
            # Initialize new storage and service
            new_storage = FileStorage(import_path)
            new_service = TodoService(storage=new_storage)
            new_app = CLIApp(service=new_service)
            
            # Import the tasks
            result = new_app.run(['import', export_path])
            assert result == 0
            
            # Verify the import output
            captured = capsys.readouterr()
            assert "Imported 2 tasks from" in captured.out
            
            # List tasks in the new storage to verify they were imported correctly
            result = new_app.run(['list'])
            assert result == 0
            
            # Verify the tasks are present with correct status
            captured = capsys.readouterr()
            assert "1. [✓] Buy groceries" in captured.out  # Completed task
            assert "2. [○] Finish report" in captured.out  # Incomplete task
        finally:
            # Clean up temporary files
            if os.path.exists(import_path):
                os.remove(import_path)
            if os.path.exists(export_path):
                os.remove(export_path)
    
    def test_export_import_cycle_preserves_task_data(self, capsys, temp_file):
        """Test that exporting and importing preserves all task data."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add tasks with different statuses
        app.run(['add', 'Task', '1'])
        app.run(['add', 'Task', '2'])
        app.run(['add', 'Task', '3'])
        app.run(['complete', '2'])  # Complete the middle task
        
        # Clear the output from the add/complete commands
        capsys.readouterr()
        
        # Export tasks
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_export_file:
            export_path = temp_export_file.name
        
        result = app.run(['export', export_path])
        assert result == 0
        
        # Clear the export output
        capsys.readouterr()
        
        # Delete all tasks from current storage
        app.run(['delete', '1'])
        app.run(['delete', '2'])
        app.run(['delete', '3'])
        
        # Verify storage is empty
        result = app.run(['list'])
        assert result == 0
        captured = capsys.readouterr()
        assert "No tasks found." in captured.out
        
        # Import tasks back
        result = app.run(['import', export_path])
        assert result == 0
        
        # Verify import output
        captured = capsys.readouterr()
        assert "Imported 3 tasks from" in captured.out
        
        # List tasks to verify they were restored with correct status
        result = app.run(['list'])
        assert result == 0
        
        # Verify all tasks are present with correct status
        captured = capsys.readouterr()
        assert "1. [○] Task 1" in captured.out  # Incomplete task
        assert "2. [✓] Task 2" in captured.out  # Completed task
        assert "3. [○] Task 3" in captured.out  # Incomplete task

        # Clean up temporary file
        if os.path.exists(export_path):
            os.remove(export_path)