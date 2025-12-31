"""
Contract test for complete command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestCompleteCommand:
    """Contract tests for the complete command."""
    
    def test_complete_command_marks_task_as_complete(self, capsys, temp_file):
        """Test that the complete command successfully marks a task as complete."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Mark the task as complete
        result = app.run(['complete', '1'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the output message
        captured = capsys.readouterr()
        assert "Marked task #1 as complete: Buy groceries" in captured.out
        
        # Verify the task is actually marked as complete in storage
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['completed'] is True
        assert tasks[0]['id'] == 1
    
    def test_complete_command_with_invalid_id_fails(self, capsys, temp_file):
        """Test that the complete command fails with an invalid task ID."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to mark a non-existent task as complete
        result = app.run(['complete', '999'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower()
    
    def test_complete_command_output_format(self, capsys, temp_file):
        """Test that the complete command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Mark the task as complete
        app.run(['complete', '1'])
        
        # Verify the output format
        captured = capsys.readouterr()
        assert "Marked task #1 as complete: Buy groceries" in captured.out