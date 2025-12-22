from openhands.sdk.event import ActionEvent, ObservationEvent, UserRejectObservation
from openhands.sdk.event.base import Event
from collections.abc import Sequence

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
        observed_action_ids = set()
        unmatched_actions = []
        # Search in reverse - recent events are more likely to be unmatched
        for event in reversed(events):
            if isinstance(event, (ObservationEvent, UserRejectObservation)):
                observed_action_ids.add(event.action_id)
            elif isinstance(event, ActionEvent):
                # Only executable actions (validated) are considered pending
                if event.action is not None and event.id not in observed_action_ids:
                    # Insert at beginning to maintain chronological order in result
                    unmatched_actions.insert(0, event)

        return unmatched_actions