class AnalysisStep:
    """Represents an analysis step with sub-events."""

    def __post_init__(self):
        self.sub_events = []

    def add_sub_event(self, sub_event):
        self.sub_events.append(sub_event)

    def get_sub_events(self):
        return self.sub_events

    def clear_sub_events(self):
        self.sub_events = []