"""
Navigation Service for managing navigation state and keyboard input.
"""
import sys
import select
from typing import Optional, List, Dict, Any
from src.models.visual_elements import NavigationState
from src.services.terminal_compatibility_service import TerminalCompatibilityService


class NavigationService:
    """
    Service class that manages navigation state and keyboard input for interactive menus.
    """

    def __init__(self, compatibility_service: TerminalCompatibilityService = None):
        """
        Initialize the Navigation Service.

        Args:
            compatibility_service: TerminalCompatibilityService instance for checking capabilities.
                                   If None, creates a default instance.
        """
        self.compatibility_service = compatibility_service or TerminalCompatibilityService()
        self.navigation_state: Optional[NavigationState] = None
        self.items: List[Any] = []
        self.menu_id: str = ""
        self._key_map = {
            'up': ['\x1b[A', 'w', 'W'],      # Arrow up, W
            'down': ['\x1b[B', 's', 'S'],    # Arrow down, S
            'left': ['\x1b[D', 'a', 'A'],    # Arrow left, A
            'right': ['\x1b[C', 'd', 'D'],   # Arrow right, D
            'enter': ['\n', '\r'],           # Enter key
            'exit': ['\x1b', 'q', 'Q'],      # ESC, Q
        }

    def set_navigation_context(self, items: List[Any], menu_id: str = "default_menu") -> None:
        """
        Set the context for navigation (items to navigate through and menu ID).

        Args:
            items: List of items to navigate through
            menu_id: ID of the current menu
        """
        self.items = items
        self.menu_id = menu_id
        self.navigation_state = NavigationState(
            current_index=0 if items else -1,
            total_items=len(items),
            menu_id=menu_id,
            last_action="init"
        )

    def get_current_item(self) -> Optional[Any]:
        """
        Get the currently selected item based on navigation state.

        Returns:
            Currently selected item or None if no items or invalid index
        """
        if (not self.items or 
            self.navigation_state is None or 
            self.navigation_state.current_index < 0 or 
            self.navigation_state.current_index >= len(self.items)):
            return None
        
        return self.items[self.navigation_state.current_index]

    def get_current_index(self) -> int:
        """
        Get the current navigation index.

        Returns:
            Current index in the navigation
        """
        if self.navigation_state is None:
            return -1
        return self.navigation_state.current_index

    def move_up(self) -> bool:
        """
        Move the selection up in the list.

        Returns:
            True if the move was successful, False otherwise
        """
        if (self.navigation_state is None or 
            self.navigation_state.current_index <= 0):
            return False

        self.navigation_state.current_index -= 1
        self.navigation_state.last_action = "up"
        return True

    def move_down(self) -> bool:
        """
        Move the selection down in the list.

        Returns:
            True if the move was successful, False otherwise
        """
        if (self.navigation_state is None or 
            self.navigation_state.current_index >= self.navigation_state.total_items - 1):
            return False

        self.navigation_state.current_index += 1
        self.navigation_state.last_action = "down"
        return True

    def move_to_first(self) -> bool:
        """
        Move the selection to the first item in the list.

        Returns:
            True if the move was successful, False otherwise
        """
        if (self.navigation_state is None or 
            self.navigation_state.total_items == 0):
            return False

        self.navigation_state.current_index = 0
        self.navigation_state.last_action = "first"
        return True

    def move_to_last(self) -> bool:
        """
        Move the selection to the last item in the list.

        Returns:
            True if the move was successful, False otherwise
        """
        if (self.navigation_state is None or 
            self.navigation_state.total_items == 0):
            return False

        self.navigation_state.current_index = self.navigation_state.total_items - 1
        self.navigation_state.last_action = "last"
        return True

    def handle_key_input(self, key: str) -> str:
        """
        Handle a key input and update navigation state accordingly.

        Args:
            key: The key that was pressed

        Returns:
            Action to take based on the key ('up', 'down', 'select', 'exit', 'none')
        """
        if key in self._key_map['up']:
            self.move_up()
            return 'up'
        elif key in self._key_map['down']:
            self.move_down()
            return 'down'
        elif key in self._key_map['enter']:
            return 'select'
        elif key in self._key_map['exit']:
            return 'exit'
        else:
            return 'none'

    def get_navigation_state(self) -> Optional[NavigationState]:
        """
        Get the current navigation state.

        Returns:
            Current NavigationState or None if not initialized
        """
        return self.navigation_state

    def reset_navigation(self) -> None:
        """
        Reset the navigation state to the beginning.
        """
        if self.navigation_state is not None:
            self.navigation_state.current_index = 0
            self.navigation_state.last_action = "reset"

    def is_navigation_valid(self) -> bool:
        """
        Check if the current navigation state is valid.

        Returns:
            True if navigation state is valid, False otherwise
        """
        if self.navigation_state is None:
            return False

        return (0 <= self.navigation_state.current_index < self.navigation_state.total_items or
                (self.navigation_state.total_items == 0 and self.navigation_state.current_index == -1))

    def get_navigation_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the current navigation state.

        Returns:
            Dictionary with navigation information
        """
        if self.navigation_state is None:
            return {
                'current_index': -1,
                'total_items': 0,
                'menu_id': '',
                'last_action': 'none',
                'is_valid': False,
                'current_item': None,
                'has_items': False
            }

        return {
            'current_index': self.navigation_state.current_index,
            'total_items': self.navigation_state.total_items,
            'menu_id': self.navigation_state.menu_id,
            'last_action': self.navigation_state.last_action,
            'is_valid': self.is_navigation_valid(),
            'current_item': self.get_current_item(),
            'has_items': len(self.items) > 0
        }

    def get_key_mapping(self) -> Dict[str, List[str]]:
        """
        Get the current key mapping.

        Returns:
            Dictionary mapping actions to key sequences
        """
        return self._key_map.copy()

    def update_key_mapping(self, action: str, keys: List[str]) -> None:
        """
        Update the key mapping for a specific action.

        Args:
            action: The action to update ('up', 'down', 'left', 'right', 'enter', 'exit')
            keys: List of key sequences that should trigger this action
        """
        if action in self._key_map:
            self._key_map[action] = keys