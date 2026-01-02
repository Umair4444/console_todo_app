"""
Keyboard input listener for detecting arrow key presses and other keyboard input.
"""
import sys
import select
import tty
import termios
from typing import Optional, Callable, Dict, Any
import threading
import time


class KeyboardInputListener:
    """
    A class to listen for keyboard input, particularly arrow keys and other special keys.
    """
    
    def __init__(self):
        """
        Initialize the keyboard input listener.
        """
        self.is_windows = sys.platform.startswith('win')
        self.listener_thread = None
        self.is_listening = False
        self.callbacks: Dict[str, Callable] = {}
        
        # Key mappings
        self.key_mappings = {
            'up': ['\x1b[A', 'w', 'W'],
            'down': ['\x1b[B', 's', 'S'],
            'left': ['\x1b[D', 'a', 'A'],
            'right': ['\x1b[C', 'd', 'D'],
            'enter': ['\n', '\r'],
            'exit': ['\x1b', 'q', 'Q', 'x', 'X'],
            'backspace': ['\x7f', '\x08'],
            'tab': ['\t'],
        }
        
    def start_listening(self):
        """
        Start listening for keyboard input in a separate thread.
        """
        if self.is_listening:
            return
            
        self.is_listening = True
        self.listener_thread = threading.Thread(target=self._listen_for_input, daemon=True)
        self.listener_thread.start()
    
    def stop_listening(self):
        """
        Stop listening for keyboard input.
        """
        self.is_listening = False
        if self.listener_thread:
            self.listener_thread.join(timeout=1)  # Wait up to 1 second for thread to finish
    
    def register_callback(self, action: str, callback: Callable[[str], None]):
        """
        Register a callback function for a specific action.
        
        Args:
            action: The action to register callback for (e.g., 'up', 'down', 'select')
            callback: The function to call when the action is detected
        """
        self.callbacks[action] = callback
    
    def _listen_for_input(self):
        """
        Internal method to listen for keyboard input.
        """
        if self.is_windows:
            self._listen_windows()
        else:
            self._listen_unix()
    
    def _listen_windows(self):
        """
        Listen for keyboard input on Windows.
        """
        import msvcrt
        
        while self.is_listening:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore')
                
                # Handle special keys that are multi-byte sequences
                if ord(key) == 0 or ord(key) == 224:  # Special key prefix
                    key = key + msvcrt.getch().decode('utf-8', errors='ignore')
                    # Map Windows special keys to our standard format
                    if key == '\x00H' or key == '\xe0H':  # Up arrow
                        key = '\x1b[A'
                    elif key == '\x00P' or key == '\xe0P':  # Down arrow
                        key = '\x1b[B'
                    elif key == '\x00K' or key == '\xe0K':  # Left arrow
                        key = '\x1b[D'
                    elif key == '\x00M' or key == '\xe0M':  # Right arrow
                        key = '\x1b[C'
                
                self._process_key(key)
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    
    def _listen_unix(self):
        """
        Listen for keyboard input on Unix-like systems.
        """
        # Save the current terminal settings
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            # Set the terminal to cbreak mode to read single characters
            tty.setcbreak(fd)
            
            while self.is_listening:
                # Check if there's input available
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    
                    # Handle special sequences
                    if key == '\x1b':  # ESC sequence
                        key += sys.stdin.read(2)  # Read the next two characters
                    
                    self._process_key(key)
        finally:
            # Restore the original terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _process_key(self, key: str):
        """
        Process a key press and call the appropriate callback.
        
        Args:
            key: The key that was pressed
        """
        # Determine the action based on the key
        action = self._get_action_for_key(key)
        
        if action and action in self.callbacks:
            # Call the registered callback for this action
            self.callbacks[action](key)
    
    def _get_action_for_key(self, key: str) -> Optional[str]:
        """
        Get the action associated with a key press.
        
        Args:
            key: The key that was pressed
            
        Returns:
            The action associated with the key, or None if no action is associated
        """
        for action, keys in self.key_mappings.items():
            if key in keys:
                return action
        return None
    
    def get_key_for_action(self, action: str) -> Optional[list]:
        """
        Get the list of keys associated with an action.
        
        Args:
            action: The action to get keys for
            
        Returns:
            List of keys associated with the action, or None if action is not found
        """
        return self.key_mappings.get(action)
    
    def add_key_mapping(self, action: str, key: str):
        """
        Add a key mapping for an action.
        
        Args:
            action: The action to map the key to
            key: The key to map
        """
        if action not in self.key_mappings:
            self.key_mappings[action] = []
        if key not in self.key_mappings[action]:
            self.key_mappings[action].append(key)
    
    def remove_key_mapping(self, action: str, key: str):
        """
        Remove a key mapping for an action.
        
        Args:
            action: The action to remove the key from
            key: The key to remove
        """
        if action in self.key_mappings and key in self.key_mappings[action]:
            self.key_mappings[action].remove(key)
            # Remove the action if no keys are left
            if not self.key_mappings[action]:
                del self.key_mappings[action]


def get_keyboard_listener() -> KeyboardInputListener:
    """
    Get a singleton instance of the keyboard input listener.
    
    Returns:
        KeyboardInputListener instance
    """
    if not hasattr(get_keyboard_listener, '_instance'):
        get_keyboard_listener._instance = KeyboardInputListener()
    return get_keyboard_listener._instance