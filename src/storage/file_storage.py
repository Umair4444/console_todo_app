import json
import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path


class FileStorage:
    """
    Handles local file persistence with atomic write operations.
    Uses a temporary file approach to ensure data integrity.
    """
    
    def __init__(self, file_path: str = None):
        """
        Initialize the file storage.
        
        Args:
            file_path: Path to the JSON file for storage. 
                      If None, uses 'tasks.json' in user's home directory.
        """
        if file_path is None:
            self.file_path = Path.home() / "tasks.json"
        else:
            self.file_path = Path(file_path)
        
        # Create directory if it doesn't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize with empty list if file doesn't exist
        if not self.file_path.exists():
            self.save_tasks([])
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """
        Load tasks from the JSON file.
        
        Returns:
            List of task dictionaries
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():  # Check if file is not empty
                    return json.loads(content)
                else:
                    return []
        except FileNotFoundError:
            # If file doesn't exist, return empty list
            return []
        except json.JSONDecodeError:
            # If file contains invalid JSON, return empty list
            return []
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """
        Save tasks to the JSON file using atomic write operations.
        Uses a temporary file and rename to ensure data integrity.
        
        Args:
            tasks: List of task dictionaries to save
        """
        # Create a temporary file in the same directory as the target file
        temp_dir = self.file_path.parent
        with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False, encoding='utf-8') as temp_file:
            json.dump(tasks, temp_file, indent=2, ensure_ascii=False)
            temp_path = temp_file.name
        
        # Atomically replace the original file with the temporary file
        os.replace(temp_path, self.file_path)