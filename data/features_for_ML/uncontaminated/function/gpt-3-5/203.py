from typing import Sequence

def get_unmatched_actions(events: Sequence[Event]) -> list[ActionEvent]:
    unmatched_actions = []
    action_events = [event for event in events if isinstance(event, ActionEvent)]
    observation_events = [event for event in events if isinstance(event, ObservationEvent) or isinstance(event, UserRejectObservation)]
    
    for action_event in action_events:
        matched = False
        for observation_event in observation_events:
            if action_event.action_id == observation_event.action_id:
                matched = True
                break
        if not matched:
            unmatched_actions.append(action_event)
    
    return unmatched_actions