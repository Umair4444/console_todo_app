"""
Application configuration settings.
"""
import os
from pathlib import Path


class Settings:
    """
    Application configuration management.
    """
    
    # Default file path for task storage
    DEFAULT_TASKS_FILE = Path.home() / ".todo_app" / "tasks.json"
    
    # Maximum number of tasks supported
    MAX_TASKS = 1000
    
    # Performance thresholds (in milliseconds)
    LIST_TASKS_THRESHOLD_MS = 100  # Time to list tasks should be under 100ms for 1000 tasks
    
    # Default storage directory
    @staticmethod
    def get_storage_dir() -> Path:
        """
        Get the directory where task data is stored.
        
        Returns:
            Path object for the storage directory
        """
        storage_dir = os.getenv('TODO_STORAGE_DIR', str(Path.home() / ".todo_app"))
        return Path(storage_dir)
    
    # Get the file path for task storage
    @staticmethod
    def get_tasks_file_path() -> Path:
        """
        Get the file path for task storage.
        
        Returns:
            Path object for the tasks file
        """
        file_path = os.getenv('TODO_TASKS_FILE', str(Settings.DEFAULT_TASKS_FILE))
        return Path(file_path)
    
    @staticmethod
    def ensure_storage_directory():
        """
        Ensure that the storage directory exists.
        """
        storage_dir = Settings.get_storage_dir()
        storage_dir.mkdir(parents=True, exist_ok=True)