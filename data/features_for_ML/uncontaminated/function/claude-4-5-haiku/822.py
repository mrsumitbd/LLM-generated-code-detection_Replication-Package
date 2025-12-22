def create_slide_transition(
    direction: TransitionDirection, 
    duration: int = 300
) -> RouteTransition:
    """Create a slide transition in the specified direction."""
    return RouteTransition(
        type=TransitionType.SLIDE,
        direction=direction,
        duration=duration
    )