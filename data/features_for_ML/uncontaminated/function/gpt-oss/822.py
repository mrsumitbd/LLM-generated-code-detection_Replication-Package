from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TransitionDirection(Enum):
    """Enumeration of possible slide directions."""
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


@dataclass(frozen=True)
class RouteTransition:
    """Represents a transition used when navigating between routes."""
    transition_type: str
    direction: TransitionDirection
    duration: int

    def __repr__(self) -> str:
        return (
            f"RouteTransition(transition_type={self.transition_type!r}, "
            f"direction={self.direction!r}, duration={self.duration})"
        )


def create_slide_transition(
    direction: TransitionDirection,
    duration: int = 300,
) -> RouteTransition:
    """
    Create a slide transition in the specified direction.

    Parameters
    ----------
    direction : TransitionDirection
        The direction in which the slide transition should occur.
    duration : int, optional
        The duration of the transition in milliseconds. Defaults to 300.

    Returns
    -------
    RouteTransition
        A transition object configured for a slide animation.

    Raises
    ------
    TypeError
        If ``direction`` is not an instance of :class:`TransitionDirection`.
    ValueError
        If ``duration`` is negative.
    """
    if not isinstance(direction, TransitionDirection):
        raise TypeError(
            f"direction must be an instance of TransitionDirection, got {type(direction)!r}"
        )
    if not isinstance(duration, int):
        raise TypeError(
            f"duration must be an int, got {type(duration)!r}"
        )
    if duration < 0:
        raise ValueError("duration must be non‑negative")

    return RouteTransition(transition_type="slide", direction=direction, duration=duration)