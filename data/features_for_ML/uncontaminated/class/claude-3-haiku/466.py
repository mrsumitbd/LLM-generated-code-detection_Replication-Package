class AIRAState:
    """State object for AIRA LangGraph workflow."""

    def __init__(self, state_id, state_type, state_data):
        self.state_id = state_id
        self.state_type = state_type
        self.state_data = state_data

    def __str__(self):
        return f"AIRAState(id={self.state_id}, type={self.state_type}, data={self.state_data})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, AIRAState):
            return False
        return (
            self.state_id == other.state_id
            and self.state_type == other.state_type
            and self.state_data == other.state_data
        )

    def __hash__(self):
        return hash((self.state_id, self.state_type, self.state_data))