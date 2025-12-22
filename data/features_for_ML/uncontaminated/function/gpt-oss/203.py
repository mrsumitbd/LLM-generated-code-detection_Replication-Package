from __future__ import annotations

from typing import Sequence, List

# The following imports are assumed to be available in the environment
# where this function will be used. They are imported lazily to avoid
# import errors when the module is not present.
try:
    from my_event_module import Event, ActionEvent, ObservationEvent, UserRejectObservations
except Exception:  # pragma: no cover
    # Define minimal stubs for type checking / documentation purposes.
    class Event:
        pass

    class ActionEvent(Event):
        action_id: str
        timestamp: float

    class ObservationEvent(Event):
        action_id: str

    class UserRejectObservations(Event):
        action_id: str


def get_unmatched_actions(events: Sequence[Event]) -> List[ActionEvent]:
    """
    Find actions in the event history that don't have matching observations.

    This method identifies ActionEvents that don't have corresponding
    ObservationEvents or UserRejectObservations, which typically indicates
    actions that are pending confirmation or execution.

    Args:
        events: List of events to search through

    Returns:
        List of ActionEvent objects that don't have corresponding observations,
        in chronological order
    """
    # Map action_id to the ActionEvent instance
    actions_by_id: dict[str, ActionEvent] = {}
    # Set of action_ids that have been matched by an observation or reject
    matched_ids: set[str] = set()

    for ev in events:
        if isinstance(ev, ActionEvent):
            # Store the action event; if multiple actions with same id exist,
            # keep the earliest one (by timestamp)
            if ev.action_id not in actions_by_id or ev.timestamp < actions_by_id[ev.action_id].timestamp:
                actions_by_id[ev.action_id] = ev
        elif isinstance(ev, (ObservationEvent, UserRejectObservations)):
            matched_ids.add(ev.action_id)

    # Collect unmatched actions
    unmatched = [
        action for aid, action in actions_by_id.items() if aid not in matched_ids
    ]

    # Return them sorted by timestamp
    unmatched.sort(key=lambda a: a.timestamp)
    return unmatched