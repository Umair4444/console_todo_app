"""
Contract test for import command.
"""
import pytest
import tempfile
import os
import json
from pathlib import Path
from src.cli.cli_app import CLIApp
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage


class TestImportCommand:
    """Contract tests for the import command."""
    
    def test_import_command_imports_tasks_from_file(self, capsys, temp_file):
        """Test that the import command successfully imports tasks from a JSON file."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Create a temporary JSON file with tasks to import
        import_tasks = [
            {
                "id": 1,
                "description": "Imported task 1",
                "completed": False,
                "created_at": "2025-12-30T10:00:00",
                "updated_at": "2025-12-30T10:00:00"
            },
            {
                "id": 2,
                "description": "Imported task 2",
                "completed": True,
                "created_at": "2025-12-30T09:30:00",
                "updated_at": "2025-12-30T11:15:00"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_import_file:
            json.dump(import_tasks, temp_import_file, indent=2)
            temp_import_path = temp_import_file.name
        
        try:
            # Import the tasks
            result = app.run(['import', temp_import_path])
            
            # Verify the command executed successfully
            assert result == 0
            
            # Verify the output message
            captured = capsys.readouterr()
            assert "Imported 2 tasks from" in captured.out
            
            # Verify the tasks are actually imported to storage
            tasks = storage.load_tasks()
            assert len(tasks) == 2
            assert tasks[0]['description'] == 'Imported task 1'
            assert tasks[1]['description'] == 'Imported task 2'
        finally:
            # Clean up the temporary import file
            os.remove(temp_import_path)
    
    def test_import_command_with_invalid_file_fails(self, capsys, temp_file):
        """Test that the import command fails with an invalid file."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Try to import from a non-existent file
        result = app.run(['import', 'non_existent_file.json'])
        
        # Verify the command failed
        assert result != 0
        
        # Verify the error message
        captured = capsys.readouterr()
        assert "Error:" in captured.err
    
    def test_import_command_output_format(self, capsys, temp_file):
        """Test that the import command produces the expected output format."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        app = CLIApp(service=service)
        
        # Create a temporary JSON file with tasks to import
        import_tasks = [
            {
                "id": 1,
                "description": "Imported task 1",
                "completed": False,
                "created_at": "2025-12-30T10:00:00",
                "updated_at": "2025-12-30T10:00:00"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_import_file:
            json.dump(import_tasks, temp_import_file, indent=2)
            temp_import_path = temp_import_file.name
        
        try:
            # Import the tasks
            app.run(['import', temp_import_path])
            
            # Verify the output format
            captured = capsys.readouterr()
            assert "Imported 1 tasks from" in captured.out
        finally:
            # Clean up the temporary import file
            os.remove(temp_import_path)