from bot_api import BotAPI
import reaction

class Reaction:

    def __init__(self, api: BotAPI, event_id, data: reaction.Reaction):
        self.api = api
        self.event_id = event_id
        self.data = data

    def __repr__(self):
        return f"Reaction(api={self.api}, event_id={self.event_id}, data={self.data})"