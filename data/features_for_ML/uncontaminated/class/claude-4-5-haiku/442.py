class Reaction:

    def __init__(self, api: BotAPI, event_id, data: reaction.Reaction):
        self.api = api
        self.event_id = event_id
        self.data = data
        self.user_id = data.user_id
        self.emoji = data.emoji
        self.timestamp = data.timestamp

    def __repr__(self):
        return (
            f"Reaction(event_id={self.event_id}, user_id={self.user_id}, "
            f"emoji={self.emoji!r}, timestamp={self.timestamp})"
        )