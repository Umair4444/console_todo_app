"""
Contract test for delete command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestDeleteCommand:
    """Contract tests for the delete command."""
    
    def test_delete_command_removes_task(self, capsys, temp_file):
        """Test that the delete command successfully removes a task."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Delete the task
        result = app.run(['delete', '1'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the output message
        captured = capsys.readouterr()
        assert "Deleted task #1: Buy groceries" in captured.out
        
        # Verify the task is actually removed from storage
        tasks = storage.load_tasks()
        assert len(tasks) == 0
    
    def test_delete_command_with_invalid_id_fails(self, capsys, temp_file):
        """Test that the delete command fails with an invalid task ID."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to delete a non-existent task
        result = app.run(['delete', '999'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower()
    
    def test_delete_command_output_format(self, capsys, temp_file):
        """Test that the delete command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Delete the task
        app.run(['delete', '1'])
        
        # Verify the output format
        captured = capsys.readouterr()
        assert "Deleted task #1: Buy groceries" in captured.out
    
    def test_delete_task_then_verify_it_is_gone(self, capsys, temp_file):
        """Test that after deleting a task, it no longer appears in the list."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add multiple tasks
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        app.run(['add', 'Call', 'mom'])
        
        # Clear the output from the add commands
        capsys.readouterr()
        
        # Delete the second task
        result = app.run(['delete', '2'])
        assert result == 0
        
        # Verify the output message
        captured = capsys.readouterr()
        assert "Deleted task #2: Finish report" in captured.out
        
        # List tasks to verify the deleted task is gone
        result = app.run(['list'])
        assert result == 0
        
        # Verify the deleted task is not in the list
        captured = capsys.readouterr()
        assert "2. [○] Finish report" not in captured.out  # Task #2 should be gone
        assert "1. [○] Buy groceries" in captured.out     # Task #1 should still be there
        assert "3. [○] Call mom" in captured.out          # Task #3 should still be there