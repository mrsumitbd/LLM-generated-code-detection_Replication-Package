class ActionsResourceWithStreamingResponse:
    def __init__(self, actions: ActionsResource) -> None:
        self.actions = actions

    def get(self, request: Request) -> StreamingHttpResponse:
        action_ids = request.query_params.get('action_ids', [])
        if not action_ids:
            return StreamingHttpResponse(status=status.HTTP_400_BAD_REQUEST)

        action_ids = [int(id) for id in action_ids.split(',')]
        actions = self.actions.get_actions(action_ids)

        def generate_response():
            for action in actions:
                yield json.dumps(action.to_dict()) + '\n'

        return StreamingHttpResponse(generate_response(), content_type='application/json')

    def post(self, request: Request) -> Response:
        data = json.loads(request.body)
        action = self.actions.create_action(data)
        return Response(action.to_dict(), status=status.HTTP_201_CREATED)

    def patch(self, request: Request, action_id: int) -> Response:
        data = json.loads(request.body)
        action = self.actions.update_action(action_id, data)
        return Response(action.to_dict(), status=status.HTTP_200_OK)

    def delete(self, request: Request, action_id: int) -> Response:
        self.actions.delete_action(action_id)
        return Response(status=status.HTTP_204_NO_CONTENT)