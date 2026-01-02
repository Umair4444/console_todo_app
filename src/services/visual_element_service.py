"""
Visual Element Service for managing visual elements and their fallbacks.
"""
from typing import Dict, List, Optional
from src.models.visual_elements import VisualElement, TerminalCompatibility
from src.services.terminal_compatibility_service import TerminalCompatibilityService


class VisualElementService:
    """
    Service class that manages visual elements and their fallbacks based on terminal capabilities.
    """

    def __init__(self, compatibility_service: Optional[TerminalCompatibilityService] = None):
        """
        Initialize the Visual Element Service.

        Args:
            compatibility_service: TerminalCompatibilityService instance for checking capabilities.
                                   If None, creates a default instance.
        """
        self.compatibility_service = compatibility_service or TerminalCompatibilityService()
        self.emoji_mapping = {
            'completed': '✅',
            'in_progress': '🔄',
            'active': '📝',
            'deleted': '❌',
            'add': '➕',
            'list': '📋',
            'update': '✏️',
            'delete': '🗑️',
            'exit': '🚪',
            'help': '❓',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️',
        }
        
        self.color_mapping = {
            'completed': 'green',
            'in_progress': 'yellow',
            'active': 'blue',
            'deleted': 'red',
            'add': 'cyan',
            'list': 'magenta',
            'update': 'yellow',
            'delete': 'red',
            'exit': 'bright_black',
            'help': 'bright_cyan',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'blue',
        }

    def get_visual_element(self, element_type: str) -> VisualElement:
        """
        Get a visual element for the specified type.

        Args:
            element_type: Type of visual element to retrieve

        Returns:
            VisualElement instance
        """
        emoji = self.emoji_mapping.get(element_type, '❓')
        color = self.color_mapping.get(element_type, 'white')
        symbol = self._get_fallback_symbol(element_type)
        description = self._get_element_description(element_type)
        
        return VisualElement(
            emoji=emoji,
            color=color,
            symbol=symbol,
            description=description
        )

    def _get_fallback_symbol(self, element_type: str) -> str:
        """
        Get a fallback symbol for when emojis aren't supported.

        Args:
            element_type: Type of visual element

        Returns:
            Fallback symbol string
        """
        fallbacks = {
            'completed': '[X]',
            'in_progress': '[~]',
            'active': '[O]',
            'deleted': '[D]',
            'add': '[+]',
            'list': '[L]',
            'update': '[U]',
            'delete': '[DEL]',
            'exit': '[EXIT]',
            'help': '[?]',
            'success': '[OK]',
            'error': '[ERR]',
            'warning': '[!]',
            'info': '[INFO]',
        }
        return fallbacks.get(element_type, '[?]')

    def _get_element_description(self, element_type: str) -> str:
        """
        Get a description for the visual element.

        Args:
            element_type: Type of visual element

        Returns:
            Description string
        """
        descriptions = {
            'completed': 'Task completed',
            'in_progress': 'Task in progress',
            'active': 'Active task',
            'deleted': 'Deleted task',
            'add': 'Add new task',
            'list': 'List tasks',
            'update': 'Update task',
            'delete': 'Delete task',
            'exit': 'Exit application',
            'help': 'Help information',
            'success': 'Success message',
            'error': 'Error message',
            'warning': 'Warning message',
            'info': 'Information message',
        }
        return descriptions.get(element_type, 'Unknown element')

    def get_visual_representation(self, element_type: str) -> str:
        """
        Get the appropriate visual representation based on terminal capabilities.

        Args:
            element_type: Type of visual element

        Returns:
            String with appropriate visual representation
        """
        compat = self.compatibility_service.get_terminal_compatibility()
        
        if compat.supports_emoji and compat.supports_color:
            # Use full visual enhancement
            element = self.get_visual_element(element_type)
            return f"[{element.color}]{element.emoji}[/] {element.description}"
        elif compat.supports_emoji:
            # Use emoji but without color
            element = self.get_visual_element(element_type)
            return f"{element.emoji} {element.description}"
        else:
            # Use fallback symbol
            element = self.get_visual_element(element_type)
            return f"{element.symbol} {element.description}"

    def get_todo_status_visual(self, completed: bool, in_progress: bool = False) -> str:
        """
        Get the appropriate visual representation for a todo item based on its status.

        Args:
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            String with appropriate visual representation
        """
        if completed:
            element_type = 'completed'
        elif in_progress:
            element_type = 'in_progress'
        else:
            element_type = 'active'
        
        return self.get_visual_representation(element_type)

    def get_todo_status_fallback(self, completed: bool, in_progress: bool = False) -> str:
        """
        Get the fallback representation for a todo item based on its status.

        Args:
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            Fallback string representation
        """
        if completed:
            element_type = 'completed'
        elif in_progress:
            element_type = 'in_progress'
        else:
            element_type = 'active'
        
        element = self.get_visual_element(element_type)
        return element.symbol

    def format_task_with_visuals(self, task_id: int, description: str, completed: bool, in_progress: bool = False) -> str:
        """
        Format a task with appropriate visual elements based on terminal capabilities.

        Args:
            task_id: ID of the task
            description: Description of the task
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            Formatted string with appropriate visual elements
        """
        visual_status = self.get_todo_status_visual(completed, in_progress)
        return f"{visual_status} {task_id}. {description}"

    def get_menu_option_visual(self, option_id: str, display_text: str) -> str:
        """
        Format a menu option with appropriate visual elements.

        Args:
            option_id: ID of the menu option
            display_text: Text to display for the option

        Returns:
            Formatted string with appropriate visual elements
        """
        # Map option IDs to visual element types
        option_type_map = {
            'add_task': 'add',
            'list_tasks': 'list',
            'update_task': 'update',
            'delete_task': 'delete',
            'exit': 'exit',
            'help': 'help'
        }
        
        element_type = option_type_map.get(option_id, 'info')
        visual_element = self.get_visual_representation(element_type)
        
        return f"{visual_element} {display_text}"

    def get_visual_elements_list(self) -> List[VisualElement]:
        """
        Get a list of all available visual elements.

        Returns:
            List of VisualElement instances
        """
        elements = []
        for element_type in self.emoji_mapping.keys():
            elements.append(self.get_visual_element(element_type))
        return elements

    def supports_visual_enhancements(self) -> bool:
        """
        Check if the terminal supports visual enhancements.

        Returns:
            True if visual enhancements are supported, False otherwise
        """
        return not self.compatibility_service.should_use_fallback_display()