"""
Emoji Mapping Service for mapping to-do states to appropriate emojis.
"""
from typing import Dict
from src.services.terminal_compatibility_service import TerminalCompatibilityService
from src.services.visual_element_service import VisualElementService


class EmojiMappingService:
    """
    Service class that maps to-do states to appropriate emojis based on terminal capabilities.
    """

    def __init__(self, 
                 compatibility_service: TerminalCompatibilityService = None,
                 visual_element_service: VisualElementService = None):
        """
        Initialize the Emoji Mapping Service.

        Args:
            compatibility_service: TerminalCompatibilityService instance for checking capabilities.
                                   If None, creates a default instance.
            visual_element_service: VisualElementService instance for visual elements.
                                    If None, creates a default instance.
        """
        self.compatibility_service = compatibility_service or TerminalCompatibilityService()
        self.visual_element_service = visual_element_service or VisualElementService(self.compatibility_service)
        
        # Define the mapping of to-do states to emojis
        self.state_to_emoji = {
            'completed': '✅',
            'in_progress': '🔄',
            'active': '📝',
            'deleted': '❌',
            'pending': '⏳',
            'high_priority': '❗',
            'low_priority': '🔽',
        }
        
        # Define fallback symbols for terminals that don't support emojis
        self.state_to_fallback = {
            'completed': '[X]',
            'in_progress': '[~]',
            'active': '[O]',
            'deleted': '[DEL]',
            'pending': '[P]',
            'high_priority': '[H]',
            'low_priority': '[L]',
        }

    def get_emoji_for_state(self, state: str) -> str:
        """
        Get the appropriate emoji for a given to-do state.

        Args:
            state: The state of the to-do item (e.g., 'completed', 'active', 'in_progress')

        Returns:
            Emoji string for the given state, or fallback symbol if emoji not supported
        """
        # Check if the terminal supports emojis
        if self.compatibility_service.supports_emoji():
            return self.state_to_emoji.get(state, self.state_to_emoji.get('active', '📝'))
        else:
            # Return fallback symbol if emoji is not supported
            return self.state_to_fallback.get(state, self.state_to_fallback.get('active', '[O]'))

    def get_visual_for_todo_status(self, completed: bool, in_progress: bool = False, 
                                   priority: str = None) -> str:
        """
        Get the appropriate visual element for a to-do item based on its status.

        Args:
            completed: Whether the task is completed
            in_progress: Whether the task is in progress
            priority: Priority level ('high', 'low', None)

        Returns:
            String with appropriate visual representation
        """
        if completed:
            state = 'completed'
        elif in_progress:
            state = 'in_progress'
        elif priority == 'high':
            state = 'high_priority'
        elif priority == 'low':
            state = 'low_priority'
        else:
            state = 'active'
        
        return self.get_emoji_for_state(state)

    def get_emoji_for_task_operation(self, operation: str) -> str:
        """
        Get the appropriate emoji for a task operation.

        Args:
            operation: The operation being performed ('add', 'list', 'update', 'delete', etc.)

        Returns:
            Emoji string for the given operation
        """
        operation_to_emoji = {
            'add': '➕',
            'list': '📋',
            'update': '✏️',
            'delete': '🗑️',
            'complete': '✅',
            'incomplete': '↩️',
            'export': '📤',
            'import': '📥',
            'help': '❓',
            'exit': '🚪',
        }
        
        operation_to_fallback = {
            'add': '[+]',
            'list': '[L]',
            'update': '[U]',
            'delete': '[DEL]',
            'complete': '[C]',
            'incomplete': '[I]',
            'export': '[E]',
            'import': '[IMP]',
            'help': '[?]',
            'exit': '[X]',
        }
        
        if self.compatibility_service.supports_emoji():
            return operation_to_emoji.get(operation, '❓')
        else:
            return operation_to_fallback.get(operation, '[?]')

    def get_available_states(self) -> Dict[str, str]:
        """
        Get a dictionary of all available states and their corresponding emojis.

        Returns:
            Dictionary mapping states to emojis or fallback symbols
        """
        if self.compatibility_service.supports_emoji():
            return self.state_to_emoji.copy()
        else:
            return self.state_to_fallback.copy()

    def get_available_operations(self) -> Dict[str, str]:
        """
        Get a dictionary of all available operations and their corresponding emojis.

        Returns:
            Dictionary mapping operations to emojis or fallback symbols
        """
        if self.compatibility_service.supports_emoji():
            operation_map = {
                'add': '➕',
                'list': '📋',
                'update': '✏️',
                'delete': '🗑️',
                'complete': '✅',
                'incomplete': '↩️',
                'export': '📤',
                'import': '📥',
                'help': '❓',
                'exit': '🚪',
            }
        else:
            operation_map = {
                'add': '[+]',
                'list': '[L]',
                'update': '[U]',
                'delete': '[DEL]',
                'complete': '[C]',
                'incomplete': '[I]',
                'export': '[E]',
                'import': '[IMP]',
                'help': '[?]',
                'exit': '[X]',
            }
        
        return operation_map

    def is_state_valid(self, state: str) -> bool:
        """
        Check if a given state is valid for emoji mapping.

        Args:
            state: The state to check

        Returns:
            True if the state is valid, False otherwise
        """
        return state in self.state_to_emoji or state in self.state_to_fallback