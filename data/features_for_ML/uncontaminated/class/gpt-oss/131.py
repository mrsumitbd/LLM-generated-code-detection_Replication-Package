import grpc
from typing import Any, Callable, Dict, Optional, Tuple


class A2AGrpcClient:  # type: ignore
    """A minimal gRPC client for A2A services."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 50051,
        options: Optional[Tuple[Tuple[str, Any], ...]] = None,
        credentials: Optional[grpc.ChannelCredentials] = None,
        channel: Optional[grpc.Channel] = None,
    ) -> None:
        """
        Initialize the client.

        Args:
            host: The server host.
            port: The server port.
            options: Optional gRPC channel options.
            credentials: Optional channel credentials for secure channel.
            channel: Optional pre-created channel to use.
        """
        self.host = host
        self.port = port
        self.options = options or ()
        self.credentials = credentials
        self._channel = channel
        self._stub: Optional[grpc.DynamicStub] = None
        if channel is None:
            self.connect()

    @property
    def channel(self) -> grpc.Channel:
        """Return the underlying gRPC channel."""
        if self._channel is None:
            raise RuntimeError("Channel is not initialized.")
        return self._channel

    def connect(self) -> None:
        """Create a new gRPC channel and dynamic stub."""
        target = f"{self.host}:{self.port}"
        if self.credentials:
            self._channel = grpc.secure_channel(target, self.credentials, options=self.options)
        else:
            self._channel = grpc.insecure_channel(target, options=self.options)
        self._stub = grpc.DynamicStub(self._channel)

    def close(self) -> None:
        """Close the gRPC channel."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None

    def call(
        self,
        method: str,
        request: Any,
        timeout: Optional[float] = None,
        metadata: Optional[Tuple[Tuple[str, str], ...]] = None,
        request_serializer: Optional[Callable[[Any], bytes]] = None,
        response_deserializer: Optional[Callable[[bytes], Any]] = None,
    ) -> Any:
        """
        Make a unary-unary RPC call.

        Args:
            method: The full method name, e.g. '/package.Service/Method'.
            request: The request message.
            timeout: Optional timeout in seconds.
            metadata: Optional metadata to send with the request.
            request_serializer: Serializer for the request.
            response_deserializer: Deserializer for the response.

        Returns:
            The response message.
        """
        if self._channel is None:
            raise RuntimeError("Channel is not initialized.")
        # Default serializers/deserializers if not provided
        if request_serializer is None:
            request_serializer = lambda x: x
        if response_deserializer is None:
            response_deserializer = lambda x: x
        unary_unary = self._channel.unary_unary(
            method,
            request_serializer=request_serializer,
            response_deserializer=response_deserializer,
        )
        return unary_unary(request, timeout=timeout, metadata=metadata)

    def __enter__(self) -> "A2AGrpcClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()