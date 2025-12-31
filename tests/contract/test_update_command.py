"""
Contract test for update command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestUpdateCommand:
    """Contract tests for the update command."""
    
    def test_update_command_updates_task_description(self, capsys, temp_file):
        """Test that the update command successfully updates a task's description."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Update the task
        result = app.run(['update', '1', 'Buy', 'groceries', 'and', 'cook', 'dinner'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the output message
        captured = capsys.readouterr()
        assert "Updated task #1: Buy groceries and cook dinner" in captured.out
        
        # Verify the task is actually updated in storage
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['description'] == 'Buy groceries and cook dinner'
        assert tasks[0]['id'] == 1
    
    def test_update_command_with_invalid_id_fails(self, capsys, temp_file):
        """Test that the update command fails with an invalid task ID."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to update a non-existent task
        result = app.run(['update', '999', 'New', 'description'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower()
    
    def test_update_command_with_empty_description_fails(self, capsys, temp_file):
        """Test that the update command fails with an empty description."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Try to update with an empty description
        result = app.run(['update', '1'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "empty" in captured.err.lower() or "whitespace" in captured.err.lower()
    
    def test_update_command_output_format(self, capsys, temp_file):
        """Test that the update command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Update the task
        app.run(['update', '1', 'Buy', 'groceries', 'and', 'cook', 'dinner'])
        
        # Verify the output format
        captured = capsys.readouterr()
        assert "Updated task #1: Buy groceries and cook dinner" in captured.out