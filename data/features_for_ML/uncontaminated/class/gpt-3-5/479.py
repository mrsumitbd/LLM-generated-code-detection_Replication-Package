class ActionsResourceWithStreamingResponse:

    def __init__(self, actions: ActionsResource) -> None:
        self.actions = actions

    def get_actions(self):
        return self.actions.get_actions()

    def stream_actions(self):
        for action in self.actions.get_actions():
            yield action