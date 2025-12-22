
class A2AGrpcClient:  # type: ignore
        """Placeholder for A2AGrpcClient when dependencies are not installed."""

        def __init__(self, *args, **kwargs):
            raise ImportError(
                'To use A2AGrpcClient, its dependencies must be installed. '
                'You can install them with \'pip install "a2a-sdk[grpc]"\''
            ) from _original_error