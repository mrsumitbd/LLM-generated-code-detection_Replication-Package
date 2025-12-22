class BatchAction:
    """Represents a batch action for a NEAR promise."""

    def __init__(self, action_type, receiver_id, amount, gas, args):
        self.action_type = action_type
        self.receiver_id = receiver_id
        self.amount = amount
        self.gas = gas
        self.args = args

    def to_json(self):
        return {
            "type": self.action_type,
            "receiver_id": self.receiver_id,
            "amount": str(self.amount),
            "gas": self.gas,
            "args": self.args
        }

    def __str__(self):
        return f"BatchAction(type={self.action_type}, receiver_id={self.receiver_id}, amount={self.amount}, gas={self.gas}, args={self.args})"

    def __repr__(self):
        return str(self)