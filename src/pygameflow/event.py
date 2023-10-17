"""
This module provides functionality to generate custom user events, manage event handlers, and handle
various types of events in a PGF-based application.
"""
# pylint: disable=global-statement
from typing import Union, final

import pygame.event


@final
class UserEvent:
    """
    Initialize a UserEvent instance. This event is custom and can be posted to the event queue.
    """

    _counter = 0

    @classmethod
    def get_userevent_count(cls) -> int:
        """
        Get the current count of user events generated.

        Returns:
            int: The current count of user events.
        """
        return cls._counter

    @classmethod
    def create_new_userevent(cls, _dict=None):
        """
        Get a new user-generated event.

        Args:
            _dict (dict, optional): A dictionary of attributes to include in the event.

        Returns:
            pygame.event.Event: A new user-generated event.
        """
        cls._counter += 1
        event_type = pygame.USEREVENT + cls._counter
        return pygame.event.Event(event_type, **(_dict or {}))

    def __init__(self, name: str = None, _dict: dict = None):
        self.event: pygame.event.Event = self.create_new_userevent(_dict)
        self.type: int = self.event.type
        self.dict: dict = self.event.dict
        setattr(self.event, "pgf_name", name)

    def post(self, _dict: dict = None):
        """
        Post the custom event to the pygame event queue.
        """
        if _dict:
            for name, value in _dict.items():
                setattr(self.event, name, value)
        pygame.event.post(self.event)

    def schedule(self, ms: int):
        """
        Schedule this event to occur after a specified delay.

        Args:
            ms (int): The delay in milliseconds before the event is triggered.
        Must be a non-zero positive integer.

        Raises:
            RuntimeError: If `ms` is not a non-zero positive integer.
        """
        if ms <= 0:
            raise RuntimeError("`ms` should be a non-zero integer")
        pygame.time.set_timer(self.event, ms)

    def unschedule(self):
        """
        Unschedule this event.
        """
        pygame.time.set_timer(self.event, 0)


@final
class EventManager:
    """
    Initialize an EventManager to manage event handlers.
    """

    def __init__(self):
        self.event_handlers = {}

    def add_event_handler(self, event_type: int, callback):
        """
        Add an event handler for a specific event type.

        Args:
            event_type (int): The type of event to handle.
            callback (callable): The function to call when the specified event type is detected.
        """
        handlers = self.event_handlers.setdefault(event_type, {})
        handlers[callback.__name__] = callback

    def remove_event_handler(self, event_type: int, callback):
        """
        Remove an event handler for a specific event type.

        Args:
            event_type (int): The type of event to handle.
            callback (callable): The function to remove from handling the specified event type.
        """
        if handlers := self.event_handlers.get(event_type):
            handlers.pop(callback.__name__, None)

    def handle_events(self):
        """
        Handle events by calling the appropriate event handlers for the events in the
        pygame event queue.
        """
        event_mapping = {
            pygame.KEYUP: lambda e: (e.key, e.mod),
            pygame.KEYDOWN: lambda e: (e.key, e.mod),
            pygame.WINDOWENTER: lambda e: pygame.mouse.get_pos(),
            pygame.WINDOWLEAVE: lambda e: pygame.mouse.get_pos(),
            pygame.MOUSEMOTION: lambda e: (*e.pos, *e.rel, e.buttons, pygame.key.get_mods()),
            pygame.MOUSEBUTTONUP: lambda e: (*e.pos, e.button, pygame.key.get_mods()),
            pygame.MOUSEBUTTONDOWN: lambda e: (*e.pos, e.button, pygame.key.get_mods()),
            pygame.MOUSEWHEEL: lambda e: (*pygame.mouse.get_pos(), e.x, e.y),
            pygame.WINDOWRESIZED: lambda e: (e.x, e.y),
        }

        for event in pygame.event.get():
            if handlers := self.event_handlers.get(event.type):
                for callback in handlers.values():
                    callback(*event_mapping.get(event.type, lambda e: ())(event))
            # else:
            #     print("unhandled event:", event)


EventType = Union[pygame.event.Event, UserEvent]
