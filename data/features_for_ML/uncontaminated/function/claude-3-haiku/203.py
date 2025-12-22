def get_unmatched_actions(events: Sequence[Event]) -> list[ActionEvent]:
    unmatched_actions = []
    observed_actions = set()

    for event in events:
        if isinstance(event, ActionEvent):
            if event not in observed_actions:
                unmatched_actions.append(event)
        elif isinstance(event, (ObservationEvent, UserRejectObservation)):
            if event.action in observed_actions:
                observed_actions.remove(event.action)

    return unmatched_actions