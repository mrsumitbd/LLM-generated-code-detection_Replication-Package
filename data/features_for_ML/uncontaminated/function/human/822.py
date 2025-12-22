def create_slide_transition(
    direction: TransitionDirection, 
    duration: int = 300
) -> RouteTransition:
    """Create a slide transition in the specified direction."""

    transition_map = {
        TransitionDirection.LEFT: TransitionType.SLIDE_LEFT,
        TransitionDirection.RIGHT: TransitionType.SLIDE_RIGHT,
        TransitionDirection.UP: TransitionType.SLIDE_UP,
        TransitionDirection.DOWN: TransitionType.SLIDE_DOWN,
    }
    return RouteTransition(transition_map[direction], duration)