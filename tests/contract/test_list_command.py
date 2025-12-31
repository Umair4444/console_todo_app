"""
Contract test for list command.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestListCommand:
    """Contract tests for the list command."""
    
    def test_list_command_with_no_tasks(self, capsys, temp_file):
        """Test that the list command shows appropriate message when no tasks exist."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # List tasks when there are none
        result = app.run(['list'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify the appropriate message is displayed
        captured = capsys.readouterr()
        assert "No tasks found." in captured.out
    
    def test_list_command_with_multiple_tasks(self, capsys, temp_file):
        """Test that the list command displays all tasks correctly."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add some tasks
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        app.run(['complete', '1'])  # Complete the first task
        
        # Clear the output from the add/complete commands
        capsys.readouterr()
        
        # List tasks
        result = app.run(['list'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify all tasks are displayed correctly
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out  # Completed task
        assert "2. [○] Finish report" in captured.out  # Incomplete task
    
    def test_list_command_with_completed_filter(self, capsys, temp_file):
        """Test that the list command with --completed filter works correctly."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add some tasks
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        app.run(['complete', '1'])  # Complete the first task
        
        # Clear the output from the add/complete commands
        capsys.readouterr()
        
        # List only completed tasks
        result = app.run(['list', '--completed'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify only completed tasks are displayed
        captured = capsys.readouterr()
        assert "1. [✓] Buy groceries" in captured.out  # Completed task
        assert "Finish report" not in captured.out  # Incomplete task should not appear
    
    def test_list_command_with_incomplete_filter(self, capsys, temp_file):
        """Test that the list command with --incomplete filter works correctly."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add some tasks
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        app.run(['complete', '1'])  # Complete the first task
        
        # Clear the output from the add/complete commands
        capsys.readouterr()
        
        # List only incomplete tasks
        result = app.run(['list', '--incomplete'])
        
        # Verify the command executed successfully
        assert result == 0
        
        # Verify only incomplete tasks are displayed
        captured = capsys.readouterr()
        assert "2. [○] Finish report" in captured.out  # Incomplete task
        assert "Buy groceries" not in captured.out  # Completed task should not appear