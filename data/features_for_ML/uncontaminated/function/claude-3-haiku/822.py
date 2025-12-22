def create_slide_transition(
    direction: TransitionDirection, 
    duration: int = 300
) -> RouteTransition:
    """Create a slide transition in the specified direction."""
    if direction == TransitionDirection.LEFT:
        return RouteTransition(
            enter_animation=SlideAnimation(
                direction=SlideDirection.LEFT,
                duration=duration
            ),
            exit_animation=SlideAnimation(
                direction=SlideDirection.RIGHT,
                duration=duration
            )
        )
    elif direction == TransitionDirection.RIGHT:
        return RouteTransition(
            enter_animation=SlideAnimation(
                direction=SlideDirection.RIGHT,
                duration=duration
            ),
            exit_animation=SlideAnimation(
                direction=SlideDirection.LEFT,
                duration=duration
            )
        )
    elif direction == TransitionDirection.UP:
        return RouteTransition(
            enter_animation=SlideAnimation(
                direction=SlideDirection.UP,
                duration=duration
            ),
            exit_animation=SlideAnimation(
                direction=SlideDirection.DOWN,
                duration=duration
            )
        )
    elif direction == TransitionDirection.DOWN:
        return RouteTransition(
            enter_animation=SlideAnimation(
                direction=SlideDirection.DOWN,
                duration=duration
            ),
            exit_animation=SlideAnimation(
                direction=SlideDirection.UP,
                duration=duration
            )
        )
    else:
        raise ValueError("Invalid transition direction")