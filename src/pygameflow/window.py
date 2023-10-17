"""
The main Window class that a game made with pygameflow should build upon.

Example:
    ```python
    import pygameflow as pgf
    pygameflow = pgf.Window(width=1024, height=768, title="My Game")
    ```
"""
# pylint: disable=too-many-arguments
from typing import Optional

import pygame

from .event import EventManager, EventType
from .window_commands import exit  # pylint: disable=redefined-builtin
from .window_commands import set_title, set_window

__AA_ENABLED = False  # Antialiasing
__VSYNC_ENABLED = False  # Vertical Sync (VSync)


def is_aa_enabled() -> bool:
    """
    Check if antialiasing is enabled.

    Returns:
        bool: True if antialiasing is enabled, False otherwise.
    """
    return __AA_ENABLED


def is_vsync_enabled() -> bool:
    """
    Check if vertical sync (VSync) is enabled.

    Returns:
        bool: True if VSync is enabled, False otherwise.
    """
    return __VSYNC_ENABLED


class _WindowContext:
    """
    Context manager for managing the window's active running state.
    """

    def __init__(self, window: "Window"):
        self.window = window
        self.active = False

    def __enter__(self):
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            return False

        self.active = False
        self.window.close()
        return True


class Window:  # pylint: disable=too-many-instance-attributes
    """
    The Window class forms the basis of most games that use PyGameFlow.
    It represents a window on the screen, and manages events.

    Args:
        width (int): The width of the window in pixels.
        height (int): The height of the window in pixels.
        title (str, optional): The title of the window. Default is "PyGameFlow Window".
        hide_title_bar (bool): Set to True to hide the window's title bar.
        fullscreen (bool): Set to True for fullscreen mode, False for windowed mode.
        resizable (bool): Set to True to allow window resizing, False to disable resizing.
        update_rate (float, optional): The rate at which the window should update in seconds.
            Default is approximately 60 frames per second (0.016666666666666666).
        antialiasing (bool): Enable or disable antialiasing for rendering.
            Note:
                Uses pygame.gfxdraw for drawing shapes.
                This feature is experimental and subject to change in future versions.
        hidden (bool): Set to True to make the window initially hidden.
        vsync (bool): Enable or disable vertical sync (VSync) for rendering.
            Note:
                This feature is experimental and subject to change in future versions.
        center_window (bool): Set to True to center the window on the screen.

    Note:
        The `width` and `height` parameters determine the size of the window's client area.
        The actual window size may include window decorations (e.g., title bar) and vary
        depending on the operating system.

    Example:
        ```python
        import pygameflow as pgf
        pygameflow = pgf.Window(width=1024, height=768, title="My Game")
        ```
    """

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: Optional[str] = "PyGameFlow Window",
        hide_title_bar: bool = False,
        fullscreen: bool = False,
        resizable: bool = False,
        update_rate: Optional[float] = 0.016666666666666666,
        antialiasing: bool = False,
        hidden: bool = False,
        vsync: bool = False,
        center_window: bool = False,
    ):
        self.height = height
        self.width = width
        self._screen: Optional["pygame.Surface"] = None
        self._background_color = pygame.Color((255, 255, 255))
        self._clock = pygame.time.Clock()

        self.__flags = (
            (fullscreen * pygame.FULLSCREEN)
            | (resizable * pygame.RESIZABLE)
            | (hide_title_bar * pygame.NOFRAME)
            | (hidden * pygame.HIDDEN)
        )

        global __AA_ENABLED, __VSYNC_ENABLED  # pylint: disable=global-statement
        __AA_ENABLED = antialiasing
        __VSYNC_ENABLED = vsync

        if center_window:
            import os  # pylint: disable=import-outside-toplevel

            os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.event_manager = EventManager()

        self.active = False

        self._ctx = _WindowContext(self)
        set_window(self)
        set_title(title)
        self.update_rate = update_rate
        # register events
        self.__register_events()

    def __register_events(self):
        self.event_manager.add_event_handler(pygame.QUIT, self.close)
        self.event_manager.add_event_handler(pygame.WINDOWFOCUSGAINED, self.on_focus)
        self.event_manager.add_event_handler(pygame.WINDOWFOCUSLOST, self.on_blur)
        self.event_manager.add_event_handler(pygame.KEYDOWN, self.on_key_press)
        self.event_manager.add_event_handler(pygame.KEYUP, self.on_key_release)
        self.event_manager.add_event_handler(pygame.WINDOWLEAVE, self.on_mouse_leave)
        self.event_manager.add_event_handler(pygame.WINDOWENTER, self.on_mouse_enter)
        self.event_manager.add_event_handler(pygame.MOUSEMOTION, self.__on_mouse_motion)
        self.event_manager.add_event_handler(pygame.MOUSEBUTTONDOWN, self.on_mouse_press)
        self.event_manager.add_event_handler(pygame.MOUSEBUTTONUP, self.on_mouse_release)
        self.event_manager.add_event_handler(pygame.MOUSEWHEEL, self.on_mouse_scroll)
        self.event_manager.add_event_handler(pygame.WINDOWRESIZED, self.on_resize)

    def clear(self, color: Optional[pygame.Color] = None):
        """
        Clear the window with a specified color or the configured background color.

        Args:
            color (pygameflow.Color, optional): The color to use for clearing the window.
                If not provided, the window will be cleared with the background color.

        Note:
            The background color can be set using the `background_color` property.

        Example:
            ```python
            window.clear()  # Clear the window with the configured background color
            window.clear(pygameflow.Color(255, 0, 0))  # Clear the window with a red color
            ```

        """
        color = color if color is not None else self.background_color
        self._screen.fill(color)

    @property
    def background_color(self) -> pygame.Color:
        """
        Get the current background color of the window.

        Returns:
            pygameflow.Color: The background color of the window.
        """
        return self._background_color

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
        self._background_color = value

    def run(self):
        """
        Start the game loop and run the window.

        This method sets up the window and enters the game loop.
        """
        self._screen = pygame.display.set_mode(
            size=self.size, flags=self.__flags, vsync=is_vsync_enabled()
        )
        with self._ctx as runner:
            while runner.active:
                self.event_manager.handle_events()
                self.clear()
                self.on_update()
                self.on_draw()
                pygame.display.flip()
                self._clock.tick(1 / self.update_rate)

    def close(self, _event: "EventType" = None):
        """
        Close the window and quit the game.

        This method should be called to close the window and end the game.
        """
        self._ctx.active = False
        exit()

    @staticmethod
    def get_title() -> str:
        """
        Get the current title of the window.

        Returns:
            str: The title of the window.
        """
        return pygame.display.get_caption()[0]

    @property
    def size(self) -> tuple[int, int]:
        """
        Get the size of the window.

        Returns:
            Tuple[int, int]: The width and height of the window.
        """
        return self.width, self.height

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

    def __on_mouse_motion(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
        buttons: tuple[int, int, int],
        modifiers: int,
    ):
        """
        Handle the mouse motion event.

        This method is an internal method used to differentiate between mouse motion
        and mouse drag events. It calls either the `on_mouse_motion` or `on_mouse_drag`
        method based on whether any mouse buttons are pressed during the mouse motion.
        """
        if buttons == (0, 0, 0):
            self.on_mouse_motion(x, y, dx, dy, modifiers)
        else:
            self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

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

    def on_resize(self, width: int, height: int):
        """
        Handle the window resize event.

        This method is called when the window is resized. It should be overridden in your game
        code to handle window resize events.

        Args:
            width (int): The new width of the window's client area.
            height (int): The new height of the window's client area.
        """

    def on_focus(self, _event: EventType):
        """
        Handle the window focus event.

        This method is called when the window gains the focus. It should be overridden in your
        game code to handle window resize events.

        Args:
            _event (EventType): The event.
        """

    def on_blur(self, _event: EventType):
        """
        Handle the window blur event.

        This method is called when the window loses the focus. It should be overridden in your
        game code to handle window resize events.

        Args:
            _event (EventType): The event.
        """


def open_window(
    width: int,
    height: int,
    window_title: Optional[str] = None,
    resizable: bool = False,
    antialiasing: bool = True,
) -> Window:
    """
    Create and open a PyGameFlow window with the specified parameters.

    Args:
        width (int): The width of the window in pixels.
        height (int): The height of the window in pixels.
        window_title (str, optional): The title of the window. Default is None.
        resizable (bool): Set to True to allow window resizing, False to disable resizing.
        antialiasing (bool): Enable or disable antialiasing for rendering.

    Returns:
        Window: The newly created PyGameFlow window.

    Example:
        ```python
        import pygameflow as pgf

        # Create a resizable window with antialiasing
        window = pgf.open_window(800, 600, "My Game", resizable=True, antialiasing=True)

        # Create a non-resizable window with the default title
        window = pgf.open_window(1024, 768)
        ```
    """
    return Window(
        width=width,
        height=height,
        title=window_title,
        resizable=resizable,
        antialiasing=antialiasing,
    )
