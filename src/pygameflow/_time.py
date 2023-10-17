"""
Pause the game or schedule/unschedule events
"""
import pygame.time


def pause(ms: int):
    """
    Pause the program for a specified number of milliseconds.

    Args:
        ms (int): The number of milliseconds to pause the program.
    """
    pygame.time.wait(ms)


def schedule(event: "pygame.event.Event", ms: int):
    """
    Schedule a timer event to occur after a specified delay.

    Args:
        event (pygame.event.Event): The timer event to schedule.
        ms (int): The delay in milliseconds before the event is triggered.
    Must be a non-zero positive integer.

    Raises:
        RuntimeError: If `ms` is not a non-zero positive integer.
    """
    if ms <= 0:
        raise RuntimeError("`ms` should be a non-zero integer")
    pygame.time.set_timer(event, ms)


def unschedule(event: "pygame.event.Event"):
    """
    Unschedule a previously scheduled timer event.

    Args:
        event (pygame.event.Event): The timer event to unschedule.
    """
    pygame.time.set_timer(event, 0)
