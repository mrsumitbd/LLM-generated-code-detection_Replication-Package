class ActionBeginTransactionRequest:

    def __init__(self):
        self.nonce = None

    def Unpack(self, any_message):
        """
        Unpacks an Any message into ActionBeginTransactionRequest.
        
        Args:
            any_message: A protobuf Any message containing a serialized ActionBeginTransactionRequest
            
        Returns:
            bool: True if unpacking was successful, False otherwise
        """
        if any_message is None:
            return False
        
        try:
            # Attempt to unpack the Any message
            if hasattr(any_message, 'Unpack'):
                return any_message.Unpack(self)
            else:
                # If it's already the message type, copy its contents
                if hasattr(any_message, 'nonce'):
                    self.nonce = any_message.nonce
                return True
        except Exception:
            return False

    def __repr__(self):
        return f"ActionBeginTransactionRequest(nonce={self.nonce})"

    def __eq__(self, other):
        if not isinstance(other, ActionBeginTransactionRequest):
            return False
        return self.nonce == other.nonce

    def __hash__(self):
        return hash(self.nonce)