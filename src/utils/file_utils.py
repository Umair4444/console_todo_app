import os
import tempfile
from pathlib import Path
from typing import Union


def atomic_write(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
    """
    Write content to a file atomically using a temporary file and rename approach.
    
    Args:
        file_path: Path to the target file
        content: Content to write to the file
        encoding: Text encoding to use (default: utf-8)
    """
    file_path = Path(file_path)
    
    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a temporary file in the same directory as the target file
    with tempfile.NamedTemporaryFile(mode='w', dir=file_path.parent, delete=False, encoding=encoding) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name
    
    # Atomically replace the original file with the temporary file
    os.replace(temp_path, file_path)


def atomic_write_bytes(file_path: Union[str, Path], content: bytes) -> None:
    """
    Write binary content to a file atomically using a temporary file and rename approach.
    
    Args:
        file_path: Path to the target file
        content: Binary content to write to the file
    """
    file_path = Path(file_path)
    
    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a temporary file in the same directory as the target file
    with tempfile.NamedTemporaryFile(mode='wb', dir=file_path.parent, delete=False) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name
    
    # Atomically replace the original file with the temporary file
    os.replace(temp_path, file_path)