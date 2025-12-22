class ActionBeginTransactionRequest:
    def Unpack(self, any_message):
        from google.protobuf.any_pb2 import Any
        if not isinstance(any_message, Any):
            raise TypeError("any_message must be a google.protobuf.any_pb2.Any")
        any_message.Unpack(self)