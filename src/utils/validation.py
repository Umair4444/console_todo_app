"""
Validation utilities for input sanitization and validation.
"""
import re
from typing import Optional


def validate_task_description(description: str) -> bool:
    """
    Validate a task description.
    
    Args:
        description: The task description to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not description:
        return False
    
    # Check if description is just whitespace
    if not description.strip():
        return False
    
    # Check for minimum length (optional, can be adjusted)
    if len(description.strip()) < 1:
        return False
    
    return True


def sanitize_task_description(description: str) -> str:
    """
    Sanitize a task description by removing or escaping special characters if needed.
    
    Args:
        description: The task description to sanitize
        
    Returns:
        Sanitized task description
    """
    # For now, just strip leading/trailing whitespace
    # Additional sanitization can be added as needed
    return description.strip()


def validate_task_id(task_id: int) -> bool:
    """
    Validate a task ID.
    
    Args:
        task_id: The task ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Task ID should be a positive integer
    return isinstance(task_id, int) and task_id > 0


def validate_file_path(file_path: str) -> bool:
    """
    Validate a file path.
    
    Args:
        file_path: The file path to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not file_path or not file_path.strip():
        return False
    
    # Basic check for potentially dangerous patterns
    dangerous_patterns = [
        r'\.\./',  # Directory traversal
        r'\.\.\\',  # Directory traversal (Windows)
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, file_path):
            return False
    
    return True