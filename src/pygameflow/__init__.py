"""
PyGameFlow: An Object-Oriented and Modern Pygame Wrapper with Developer-Friendly Features
"""
# pylint: disable=wrong-import-position
# isort: skip_file
import os

# hide pygame support
if not os.environ.get("PYGAME_HIDE_SUPPORT_PROMPT"):
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"


import pygame

# noinspection PyUnresolvedReferences
from pygame.color import *

# noinspection PyUnresolvedReferences
from pygame.constants import *

from .event import UserEvent
from .event import EventManager

from ._time import pause
from ._time import schedule
from ._time import unschedule

from .view import View
from .window import Window
from .window import open_window

from .window_commands import get_display_size
from .window_commands import get_window
from .window_commands import set_window
from .window_commands import close_window

from .window_commands import run
from .window_commands import set_background_color
from .window_commands import exit  # pylint: disable=redefined-builtin

# initiate
pygame.init()

# welcome!
if not os.environ.get("PGF_HIDE_WELCOME"):
    import platform

    from pygame import get_sdl_version

    ver = "0.0.0"  # pylint: disable=invalid-name
    print(
        f"PyGameFlow {ver} (SDL {'.'.join(map(str, get_sdl_version()))}, "
        f"Python {platform.python_version()})"
    )
