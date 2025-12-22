def create_slide_transition(direction: TransitionDirection, duration: int = 300) -> RouteTransition:
    return RouteTransition(transition_type='slide', direction=direction, duration=duration)