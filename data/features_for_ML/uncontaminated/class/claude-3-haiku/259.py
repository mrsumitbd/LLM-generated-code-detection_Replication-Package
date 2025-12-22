class ActionBeginTransactionRequest:
    def __init__(self, transaction_id: str, user_id: str, timestamp: int):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.timestamp = timestamp

    def Unpack(self, any_message: bytes):
        import struct

        # Unpack the message into the class attributes
        transaction_id_length, = struct.unpack('B', any_message[:1])
        self.transaction_id = any_message[1:1+transaction_id_length].decode('utf-8')
        user_id_length, = struct.unpack('B', any_message[1+transaction_id_length:2+transaction_id_length])
        self.user_id = any_message[2+transaction_id_length:2+transaction_id_length+user_id_length].decode('utf-8')
        self.timestamp, = struct.unpack('Q', any_message[2+transaction_id_length+user_id_length:2+transaction_id_length+user_id_length+8])