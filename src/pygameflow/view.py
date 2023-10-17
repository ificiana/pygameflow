"""
Creating and managing views in PyGameFlow games

The `pygameflow.view` module provides a framework for creating views, which are the core components
that handle game logic, rendering, and user interaction in PygameFlow-based games.
A view is typically associated with a window and manages various game-related events and updates.
"""
# pylint: disable=too-many-arguments
import typing

import pygame

if typing.TYPE_CHECKING:
    from .window import Window


class View:  # pylint: disable=too-many-instance-attributes
    """
    The View class overcomes the limitation of having a single window. Use View.run() to
    start the mainloop from this view, or use View.show() to switch to this view.
    """

    def __init__(
        self,
        window: "Window",
    ):
        self.window = window
        self.__register_callers()

    def __register_callers(self):
        # register callers
        self.window.on_draw = self.on_draw
        self.window.on_update = self.on_update
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.window.on_mouse_leave = self.on_mouse_leave
        self.window.on_mouse_enter = self.on_mouse_enter
        self.window.on_mouse_press = self.on_mouse_press
        self.window.on_mouse_release = self.on_mouse_release
        self.window.on_mouse_scroll = self.on_mouse_scroll

        # re-register
        # noinspection PyProtectedMember, PyUnresolvedReferences
        self.window._Window__register_events()  # pylint: disable=protected-access

    def setup(self):
        """
        This method is called before running this View
        """

    @property
    def background_color(self) -> pygame.Color:
        """
        Get the current background color of the window.

        Returns:
            pygameflow.Color: The background color of the window.
        """
        return self.window.background_color

    @background_color.setter
    def background_color(self, value: pygame.Color):
        """
        Set the background color of the window.

        Args:
            value (pygameflow.Color): The new background color to set for the window.

        Example:
            ```python
            window.background_color = pygameflow.Color(0, 0, 255)
            # Set the background color to blue
            ```

        """
        self.window.background_color = value

    @property
    def size(self) -> tuple[int, int]:
        """
        Get the size of the window.

        Returns:
            Tuple[int, int]: The width and height of the window.
        """
        return self.window.width, self.window.height

    def on_draw(self):
        """
        Draw game elements on the window.

        This method should be overridden in your game code to draw game objects, characters,
        and other elements on the window.
        """

    def on_update(self):
        """
        Update the game state.

        This method should be overridden in your game code to update game logic, handle collisions,
        and perform other game-related tasks.
        """

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Handle the key press event.

        This method is called when a key is pressed. It should be overridden in your game code to
        handle key press events.

        Args:
            symbol (int): The key symbol or code that was pressed.
            modifiers (int): A bitmask representing any modifier keys that were pressed
                (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Handle the key release event.

        This method is called when a key is released. It should be overridden in your game code to
        handle key release events.

        Args:
            symbol (int): The key symbol or code that was released.
            modifiers (int): A bitmask representing any modifier keys that were pressed
                (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_mouse_enter(self, x: int, y: int):
        """
        Handle the mouse enter event.

        This method is called when the mouse cursor enters the window's client area.
        It should be overridden in your game code to handle mouse enter events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
        """

    def on_mouse_leave(self, x: int, y: int):
        """
        Handle the mouse leave event.

        This method is called when the mouse cursor leaves the window's client area.
        It should be overridden in your game code to handle mouse leave events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.s
        """

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int, modifiers: int):
        """
        Handle the mouse motion event.

        This method is called when the mouse cursor is moved without any mouse buttons being
        pressed. It should be overridden in your game code to handle mouse motion events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
            dx (int): The change in the x-coordinate of the mouse cursor.
            dy (int): The change in the y-coordinate of the mouse cursor.
            modifiers (int): A bitmask representing any modifier keys that were pressed
                (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_mouse_drag(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
        buttons: tuple[int, int, int],
        modifiers: int,
    ):
        """
        Handle the mouse drag event.

        This method is called when the mouse cursor is moved with one or more mouse buttons being
        pressed. It should be overridden in your game code to handle mouse drag events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
            dx (int): The change in the x-coordinate of the mouse cursor.
            dy (int): The change in the y-coordinate of the mouse cursor.
            buttons (tuple[int, int, int]): A tuple of integers representing the state of
            mouse buttons.
            modifiers (int): A bitmask representing any modifier keys that were pressed
            (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Handle the mouse button press event.

        This method is called when a mouse button is pressed. It should be overridden in your
        game code to handle mouse button press events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
            button (int): The mouse button that was pressed (e.g., pygameflow.BUTTON_LEFT,
            pygameflow.BUTTON_RIGHT, etc.).
            modifiers (int): A bitmask representing any modifier keys that were pressed
                (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """
        Handle the mouse button release event.

        This method is called when a mouse button is released. It should be overridden in your
        game code to handle mouse button release events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
            button (int): The mouse button that was released (e.g., pygameflow.BUTTON_LEFT,
            pygameflow.BUTTON_RIGHT, etc.).
            modifiers (int): A bitmask representing any modifier keys that were pressed
                (e.g., pygameflow.KMOD_SHIFT, pygameflow.KMOD_CTRL, etc.).
        """

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        Handle the mouse scroll event.

        This method is called when the mouse wheel is scrolled. It should be overridden in your
        game code to handle mouse scroll events.

        Args:
            x (int): The x-coordinate of the mouse cursor's position.
            y (int): The y-coordinate of the mouse cursor's position.
            scroll_x (int): The horizontal scroll amount.
            scroll_y (int): The vertical scroll amount.
        """

    def show(self):
        """
        Display the view and set up necessary event handlers.
        This method is used to prepare and display the view.
        """
        self.__register_callers()
        self.setup()

    def run(self):
        """
        Start the view and run the associated window.
        This method initiates the view and starts running the associated window.
        """
        self.show()
        self.window.run()
