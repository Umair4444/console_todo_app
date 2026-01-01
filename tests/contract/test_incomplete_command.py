"""
Contract test for incomplete command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestIncompleteCommand:
    """Contract tests for the incomplete command."""
    
    def test_incomplete_command_marks_task_as_incomplete(self, capsys, temp_file):
        """Test that the incomplete command successfully marks a task as incomplete."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Mark it as complete
        app.run(['complete', '1'])
        
        # Clear the output from previous commands
        capsys.readouterr()
        
        # Mark the task as incomplete
        result = app.run(['incomplete', '1'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the output message
        captured = capsys.readouterr()
        assert "Marked task #1 as incomplete: Buy groceries" in captured.out
        
        # Verify the task is actually marked as incomplete in storage
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['completed'] is False
        assert tasks[0]['id'] == 1
    
    def test_incomplete_command_with_invalid_id_fails(self, capsys, temp_file):
        """Test that the incomplete command fails with an invalid task ID."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to mark a non-existent task as incomplete
        result = app.run(['incomplete', '999'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower()
    
    def test_incomplete_command_output_format(self, capsys, temp_file):
        """Test that the incomplete command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Mark it as complete
        app.run(['complete', '1'])
        
        # Clear the output from previous commands
        capsys.readouterr()
        
        # Mark the task as incomplete
        app.run(['incomplete', '1'])
        
        # Verify the output format
        captured = capsys.readouterr()
        assert "Marked task #1 as incomplete: Buy groceries" in captured.out