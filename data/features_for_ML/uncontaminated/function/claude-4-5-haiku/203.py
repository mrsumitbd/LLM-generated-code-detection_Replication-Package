def get_unmatched_actions(events: Sequence[Event]) -> list[ActionEvent]:
    """Find actions in the event history that don't have matching observations.

    This method identifies ActionEvents that don't have corresponding
    ObservationEvents or UserRejectObservations, which typically indicates
    actions that are pending confirmation or execution.

    Args:
        events: List of events to search through

    Returns:
        List of ActionEvent objects that don't have corresponding observations,
        in chronological order
    """
    action_events = {}
    unmatched_actions = []
    
    for event in events:
        if isinstance(event, ActionEvent):
            action_events[event.id] = event
            unmatched_actions.append(event)
        elif isinstance(event, (ObservationEvent, UserRejectObservation)):
            action_id = event.action_id
            if action_id in action_events and event in unmatched_actions:
                unmatched_actions.remove(action_events[action_id])
    
    return unmatched_actions