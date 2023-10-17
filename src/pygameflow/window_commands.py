"""
Commands managing the window in PyGameFlow games
"""
# pylint: disable=global-statement
import os
import sys
from typing import TYPE_CHECKING, Optional

import pygame

if TYPE_CHECKING:
    from .window import Window

_window: Optional["Window"] = None


def get_display_size() -> tuple[int, int]:
    """
    Get the current display size.

    Returns:
        tuple[int, int]: The width and height of the current display.
    """
    return pygame.display.Info().current_w, pygame.display.Info().current_h


def set_window(window: "Window") -> None:
    """
    Set the active window.

    Args:
        window (Window): The window to set as the active window.
    """
    global _window
    _window = window


def get_window() -> "Window":
    """
    Get the active window.

    Returns:
        Window: The currently active window.

    Raises:
        RuntimeError: If no window is currently active.
    """
    if not _window:
        raise RuntimeError("No window is active.")
    return _window


def run() -> None:
    """
    Run the game loop.

    This function starts the game loop, processing events and updating the window.
    """
    if os.environ.get("PGF_TESTING"):
        # to be used for unit testing
        ...
    else:
        get_window().run()


def set_title(title: str) -> None:
    """
    Set the title of the active window.

    Args:
        title (str): The new title for the window.
    """
    pygame.display.set_caption(title)


def get_title() -> str:
    """
    Get the title of the active window.

    Returns:
        str: The title of the active window.
    """
    return get_window().get_title()


def set_background_color(color: pygame.Color) -> None:
    """
    Set the background color of the active window.

    Args:
        color (pygame.Color): The color to set as the background color.
    """
    get_window().background_color = color


def close_window() -> None:
    """
    Close the active window and end the game.
    """
    get_window().close()

    global _window
    _window = None


# noinspection PyShadowingBuiltins
def exit() -> None:  # pylint: disable=redefined-builtin
    """
    Quit the application.

    This function quits the application and should be called to exit the program.
    """
    pygame.quit()
    sys.exit()
