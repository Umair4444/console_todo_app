"""
Unit tests for the Visual Elements model.
"""
import pytest
from src.models.visual_elements import VisualElement, NavigationState, TerminalCompatibility, MenuOption, ApplicationState


class TestVisualElement:
    """
    Test class for VisualElement model.
    """

    def test_visual_element_creation_with_valid_data(self):
        """
        Test creating a VisualElement with valid data.
        """
        element = VisualElement(
            emoji='✅',
            color='green',
            symbol='[X]',
            description='Task completed'
        )

        assert element.emoji == '✅'
        assert element.color == 'green'
        assert element.symbol == '[X]'
        assert element.description == 'Task completed'

    def test_visual_element_creation_fails_with_empty_emoji(self):
        """
        Test that creating a VisualElement with empty emoji raises ValueError.
        """
        with pytest.raises(ValueError, match="Emoji cannot be empty"):
            VisualElement(
                emoji='',
                color='green',
                symbol='[X]',
                description='Task completed'
            )

    def test_visual_element_creation_fails_with_empty_color(self):
        """
        Test that creating a VisualElement with empty color raises ValueError.
        """
        with pytest.raises(ValueError, match="Color cannot be empty"):
            VisualElement(
                emoji='✅',
                color='',
                symbol='[X]',
                description='Task completed'
            )

    def test_visual_element_creation_fails_with_empty_symbol(self):
        """
        Test that creating a VisualElement with empty symbol raises ValueError.
        """
        with pytest.raises(ValueError, match="Symbol cannot be empty"):
            VisualElement(
                emoji='✅',
                color='green',
                symbol='',
                description='Task completed'
            )

    def test_visual_element_creation_fails_with_empty_description(self):
        """
        Test that creating a VisualElement with empty description raises ValueError.
        """
        with pytest.raises(ValueError, match="Description cannot be empty"):
            VisualElement(
                emoji='✅',
                color='green',
                symbol='[X]',
                description=''
            )


class TestNavigationState:
    """
    Test class for NavigationState model.
    """

    def test_navigation_state_creation_with_valid_data(self):
        """
        Test creating a NavigationState with valid data.
        """
        state = NavigationState(
            current_index=0,
            total_items=5,
            menu_id='main_menu',
            last_action='select'
        )

        assert state.current_index == 0
        assert state.total_items == 5
        assert state.menu_id == 'main_menu'
        assert state.last_action == 'select'

    def test_navigation_state_creation_fails_with_negative_current_index(self):
        """
        Test that creating a NavigationState with negative current index raises ValueError.
        """
        with pytest.raises(ValueError, match="Current index cannot be negative"):
            NavigationState(
                current_index=-1,
                total_items=5,
                menu_id='main_menu',
                last_action='select'
            )

    def test_navigation_state_creation_fails_with_negative_total_items(self):
        """
        Test that creating a NavigationState with negative total items raises ValueError.
        """
        with pytest.raises(ValueError, match="Total items cannot be negative"):
            NavigationState(
                current_index=0,
                total_items=-1,
                menu_id='main_menu',
                last_action='select'
            )

    def test_navigation_state_creation_fails_with_invalid_index_total_combination(self):
        """
        Test that creating a NavigationState with current index >= total items raises ValueError.
        """
        with pytest.raises(ValueError, match="Current index cannot be greater than or equal to total items"):
            NavigationState(
                current_index=5,
                total_items=5,
                menu_id='main_menu',
                last_action='select'
            )

    def test_navigation_state_creation_fails_with_empty_menu_id(self):
        """
        Test that creating a NavigationState with empty menu ID raises ValueError.
        """
        with pytest.raises(ValueError, match="Menu ID cannot be empty"):
            NavigationState(
                current_index=0,
                total_items=5,
                menu_id='',
                last_action='select'
            )


class TestTerminalCompatibility:
    """
    Test class for TerminalCompatibility model.
    """

    def test_terminal_compatibility_creation_with_valid_data(self):
        """
        Test creating a TerminalCompatibility with valid data.
        """
        compat = TerminalCompatibility(
            supports_color=True,
            supports_emoji=True,
            supports_keyboard=True,
            color_depth=256,
            encoding='utf-8'
        )

        assert compat.supports_color is True
        assert compat.supports_emoji is True
        assert compat.supports_keyboard is True
        assert compat.color_depth == 256
        assert compat.encoding == 'utf-8'

    def test_terminal_compatibility_creation_fails_with_invalid_color_depth(self):
        """
        Test that creating a TerminalCompatibility with invalid color depth raises ValueError.
        """
        with pytest.raises(ValueError, match="Color depth must be 32, 256, or 16777216"):
            TerminalCompatibility(
                supports_color=True,
                supports_emoji=True,
                supports_keyboard=True,
                color_depth=128,  # Invalid color depth
                encoding='utf-8'
            )

    def test_terminal_compatibility_creation_fails_with_empty_encoding(self):
        """
        Test that creating a TerminalCompatibility with empty encoding raises ValueError.
        """
        with pytest.raises(ValueError, match="Encoding cannot be empty"):
            TerminalCompatibility(
                supports_color=True,
                supports_emoji=True,
                supports_keyboard=True,
                color_depth=256,
                encoding=''
            )


class TestMenuOption:
    """
    Test class for MenuOption model.
    """

    def test_menu_option_creation_with_valid_data(self):
        """
        Test creating a MenuOption with valid data.
        """
        option = MenuOption(
            id='add_task',
            display_text='Add Task',
            action='add'
        )

        assert option.id == 'add_task'
        assert option.display_text == 'Add Task'
        assert option.action == 'add'

    def test_menu_option_creation_fails_with_empty_id(self):
        """
        Test that creating a MenuOption with empty ID raises ValueError.
        """
        with pytest.raises(ValueError, match="Menu option ID cannot be empty"):
            MenuOption(
                id='',
                display_text='Add Task',
                action='add'
            )

    def test_menu_option_creation_fails_with_empty_display_text(self):
        """
        Test that creating a MenuOption with empty display text raises ValueError.
        """
        with pytest.raises(ValueError, match="Display text cannot be empty"):
            MenuOption(
                id='add_task',
                display_text='',
                action='add'
            )

    def test_menu_option_creation_fails_with_empty_action(self):
        """
        Test that creating a MenuOption with empty action raises ValueError.
        """
        with pytest.raises(ValueError, match="Action cannot be empty"):
            MenuOption(
                id='add_task',
                display_text='Add Task',
                action=''
            )


class TestApplicationState:
    """
    Test class for ApplicationState model.
    """

    def test_application_state_creation_with_valid_data(self):
        """
        Test creating an ApplicationState with valid data.
        """
        state = ApplicationState(
            current_menu='main_menu',
            waiting_for_confirmation=False,
            last_key_press='x'
        )

        assert state.current_menu == 'main_menu'
        assert state.waiting_for_confirmation is False
        assert state.last_key_press == 'x'

    def test_application_state_creation_with_none_last_key_press(self):
        """
        Test creating an ApplicationState with None as last_key_press (default).
        """
        state = ApplicationState(
            current_menu='main_menu',
            waiting_for_confirmation=True
        )

        assert state.current_menu == 'main_menu'
        assert state.waiting_for_confirmation is True
        assert state.last_key_press is None

    def test_application_state_creation_fails_with_empty_current_menu(self):
        """
        Test that creating an ApplicationState with empty current menu raises ValueError.
        """
        with pytest.raises(ValueError, match="Current menu cannot be empty"):
            ApplicationState(
                current_menu='',
                waiting_for_confirmation=False
            )