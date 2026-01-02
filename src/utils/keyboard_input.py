"""
Cross-platform keyboard input utility for capturing special keys like arrow keys.
"""
import sys

def get_char():
    """
    Read a character from standard input without waiting for Enter.
    Returns the character or key sequence.
    """
    if sys.platform == 'win32':
        import msvcrt
        # On Windows, we need to handle special keys differently
        ch = msvcrt.getch()
        if ch == b'\x00' or ch == b'\xe0':  # Special key prefix
            ch = msvcrt.getch()  # Get the actual key code
            # Map to ANSI escape sequences for compatibility
            if ch == b'H':
                return '\x1b[A'  # Up arrow
            elif ch == b'P':
                return '\x1b[B'  # Down arrow
            elif ch == b'K':
                return '\x1b[D'  # Left arrow
            elif ch == b'M':
                return '\x1b[C'  # Right arrow
            else:
                return ch.decode('utf-8', errors='ignore')
        else:
            return ch.decode('utf-8', errors='ignore')
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Check if it's an escape sequence
            if ch == '\x1b':  # ESC character
                ch += sys.stdin.read(2)  # Read the next two characters
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def is_arrow_key(key):
    """
    Check if the key is an arrow key.
    
    Args:
        key: The key character/sequence to check
    
    Returns:
        True if it's an arrow key, False otherwise
    """
    return key in ['\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D']  # Up, Down, Left, Right


def is_movement_key(key):
    """
    Check if the key is a movement key (arrow keys or WASD).
    
    Args:
        key: The key character/sequence to check
    
    Returns:
        True if it's a movement key, False otherwise
    """
    return is_arrow_key(key) or key.lower() in ['w', 'a', 's', 'd']