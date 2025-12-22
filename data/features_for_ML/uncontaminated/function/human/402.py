import grpc
from . import a2a_pb2 as a2a__pb2

def SendStreamingMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/a2a.v1.A2AService/SendStreamingMessage',
            a2a__pb2.SendMessageRequest.SerializeToString,
            a2a__pb2.StreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)