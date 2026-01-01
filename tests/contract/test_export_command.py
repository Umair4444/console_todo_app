"""
Contract test for export command.
"""
import pytest
import tempfile
import os
import json
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestExportCommand:
    """Contract tests for the export command."""
    
    def test_export_command_exports_tasks_to_file(self, capsys, temp_file):
        """Test that the export command successfully exports tasks to a JSON file."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add some tasks first
        app.run(['add', 'Buy', 'groceries'])
        app.run(['add', 'Finish', 'report'])
        
        # Clear the output from the add commands
        capsys.readouterr()
        
        # Create a temporary file for export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_export_file:
            temp_export_path = temp_export_file.name
        
        try:
            # Export the tasks
            result = app.run(['export', temp_export_path])
            
            # Verify the command executed successfully
            assert result == 0
            
            # Verify the output message
            captured = capsys.readouterr()
            assert "Exported 2 tasks to" in captured.out
            
            # Verify the tasks are actually exported to the file
            with open(temp_export_path, 'r', encoding='utf-8') as f:
                exported_tasks = json.load(f)
            
            assert len(exported_tasks) == 2
            assert exported_tasks[0]['description'] == 'Buy groceries'
            assert exported_tasks[1]['description'] == 'Finish report'
        finally:
            # Clean up the temporary export file
            if os.path.exists(temp_export_path):
                os.remove(temp_export_path)
    
    def test_export_command_with_empty_task_list(self, capsys, temp_file):
        """Test that the export command works with an empty task list."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Create a temporary file for export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_export_file:
            temp_export_path = temp_export_file.name
        
        try:
            # Export the tasks (none exist)
            result = app.run(['export', temp_export_path])
            
            # Verify the command executed successfully
            assert result == 0
            
            # Verify the output message
            captured = capsys.readouterr()
            assert "Exported 0 tasks to" in captured.out
            
            # Verify the file contains an empty list
            with open(temp_export_path, 'r', encoding='utf-8') as f:
                exported_tasks = json.load(f)
            
            assert exported_tasks == []
        finally:
            # Clean up the temporary export file
            if os.path.exists(temp_export_path):
                os.remove(temp_export_path)
    
    def test_export_command_output_format(self, capsys, temp_file):
        """Test that the export command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Add a task first
        app.run(['add', 'Buy', 'groceries'])
        
        # Clear the output from the add command
        capsys.readouterr()
        
        # Create a temporary file for export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_export_file:
            temp_export_path = temp_export_file.name
        
        try:
            # Export the tasks
            app.run(['export', temp_export_path])
            
            # Verify the output format
            captured = capsys.readouterr()
            assert "Exported 1 tasks to" in captured.out
        finally:
            # Clean up the temporary export file
            if os.path.exists(temp_export_path):
                os.remove(temp_export_path)