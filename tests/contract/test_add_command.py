"""
Contract test for add command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestAddCommand:
    """Contract tests for the add command."""
    
    def test_add_command_with_valid_description(self, temp_file):
        """Test that the add command successfully adds a task with a valid description."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task
        result = app.run(['add', 'Buy', 'groceries'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the task was added to storage
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['description'] == 'Buy groceries'
        assert tasks[0]['completed'] is False
        assert tasks[0]['id'] == 1
    
    def test_add_command_with_empty_description_fails(self, temp_file):
        """Test that the add command fails with an empty description."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to add a task with empty description
        result = app.run(['add'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify no tasks were added to storage
        tasks = storage.load_tasks()
        assert len(tasks) == 0
    
    def test_add_command_with_whitespace_description_fails(self, temp_file):
        """Test that the add command fails with a whitespace-only description."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to add a task with whitespace-only description
        result = app.run(['add', '   '])
        
        # Verify the command failed
        assert result != 0
        
        # Verify no tasks were added to storage
        tasks = storage.load_tasks()
        assert len(tasks) == 0
    
    def test_add_command_output_format(self, capsys, temp_file):
        """Test that the add command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task
        app.run(['add', 'Buy', 'groceries'])
        
        # Capture the output
        captured = capsys.readouterr()
        
        # Verify the output format
        assert "Added task #1: Buy groceries" in captured.out