"""
Error handling and logging infrastructure.
"""
import logging
import sys
from typing import Optional


# Set up basic logging configuration
def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Set up the logging configuration for the application.
    
    Args:
        level: Logging level (default: logging.INFO)
        log_file: Optional file to log to (default: None, logs to console)
    """
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    handlers.append(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True  # This ensures the configuration is applied even if logging was already configured
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Custom exception classes
class TodoError(Exception):
    """
    Base exception class for todo-related errors.
    """
    pass


class TaskNotFoundError(TodoError):
    """
    Raised when a task with a specific ID is not found.
    """
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskDescriptionError(TodoError):
    """
    Raised when a task description is invalid (e.g., empty or whitespace only).
    """
    def __init__(self):
        super().__init__("Task description cannot be empty or whitespace only")


class StorageError(TodoError):
    """
    Raised when there's an error with file storage operations.
    """
    def __init__(self, message: str):
        super().__init__(f"Storage error: {message}")


class ValidationError(TodoError):
    """
    Raised when validation fails.
    """
    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}")