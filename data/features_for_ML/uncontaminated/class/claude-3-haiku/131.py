class A2AGrpcClient:
    """A client for interacting with the A2A GRPC service."""

    def __init__(self, host: str, port: int, credentials=None):
        """
        Initialize the A2AGrpcClient.

        Args:
            host (str): The hostname or IP address of the A2A GRPC service.
            port (int): The port number of the A2A GRPC service.
            credentials (Optional[grpc.ChannelCredentials]): The credentials to use for the GRPC connection.
        """
        self._channel = grpc.secure_channel(f"{host}:{port}", credentials) if credentials else grpc.insecure_channel(f"{host}:{port}")
        self._stub = a2a_pb2_grpc.A2AServiceStub(self._channel)

    def get_data(self, request: a2a_pb2.GetDataRequest) -> a2a_pb2.GetDataResponse:
        """
        Retrieve data from the A2A GRPC service.

        Args:
            request (a2a_pb2.GetDataRequest): The request object containing the necessary parameters.

        Returns:
            a2a_pb2.GetDataResponse: The response object containing the retrieved data.
        """
        return self._stub.GetData(request)

    def set_data(self, request: a2a_pb2.SetDataRequest) -> a2a_pb2.SetDataResponse:
        """
        Set data in the A2A GRPC service.

        Args:
            request (a2a_pb2.SetDataRequest): The request object containing the data to be set.

        Returns:
            a2a_pb2.SetDataResponse: The response object indicating the result of the set operation.
        """
        return self._stub.SetData(request)

    def close(self):
        """
        Close the GRPC channel.
        """
        self._channel.close()