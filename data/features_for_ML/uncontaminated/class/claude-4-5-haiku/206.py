import json
from typing import Any, Optional


class BatchAction:
    """Represents a batch action for a NEAR promise."""

    def __init__(self, action_type: str, args: Optional[dict[str, Any]] = None):
        """Initialize a BatchAction.
        
        Args:
            action_type: The type of action (e.g., 'FunctionCall', 'Transfer', 'CreateAccount', etc.)
            args: Optional dictionary of arguments for the action
        """
        self.action_type = action_type
        self.args = args or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert the batch action to a dictionary representation.
        
        Returns:
            Dictionary representation of the batch action
        """
        return {
            "action_type": self.action_type,
            "args": self.args
        }

    def to_json(self) -> str:
        """Convert the batch action to a JSON string.
        
        Returns:
            JSON string representation of the batch action
        """
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        """Return string representation of the batch action."""
        return f"BatchAction(action_type='{self.action_type}', args={self.args})"

    def __eq__(self, other: Any) -> bool:
        """Check equality with another BatchAction."""
        if not isinstance(other, BatchAction):
            return False
        return self.action_type == other.action_type and self.args == other.args

    @classmethod
    def function_call(
        cls,
        method_name: str,
        args: Optional[dict[str, Any]] = None,
        gas: Optional[str] = None,
        deposit: Optional[str] = None
    ) -> "BatchAction":
        """Create a FunctionCall batch action.
        
        Args:
            method_name: Name of the method to call
            args: Optional arguments for the method
            gas: Optional gas amount
            deposit: Optional deposit amount
            
        Returns:
            BatchAction instance for function call
        """
        action_args = {
            "method_name": method_name,
            "args": args or {}
        }
        if gas is not None:
            action_args["gas"] = gas
        if deposit is not None:
            action_args["deposit"] = deposit
        return cls("FunctionCall", action_args)

    @classmethod
    def transfer(cls, amount: str) -> "BatchAction":
        """Create a Transfer batch action.
        
        Args:
            amount: Amount to transfer
            
        Returns:
            BatchAction instance for transfer
        """
        return cls("Transfer", {"amount": amount})

    @classmethod
    def create_account(cls) -> "BatchAction":
        """Create a CreateAccount batch action.
        
        Returns:
            BatchAction instance for account creation
        """
        return cls("CreateAccount", {})

    @classmethod
    def delete_account(cls, beneficiary_id: str) -> "BatchAction":
        """Create a DeleteAccount batch action.
        
        Args:
            beneficiary_id: Account ID to receive remaining balance
            
        Returns:
            BatchAction instance for account deletion
        """
        return cls("DeleteAccount", {"beneficiary_id": beneficiary_id})

    @classmethod
    def add_key(
        cls,
        public_key: str,
        access_key: Optional[dict[str, Any]] = None
    ) -> "BatchAction":
        """Create an AddKey batch action.
        
        Args:
            public_key: Public key to add
            access_key: Optional access key configuration
            
        Returns:
            BatchAction instance for adding a key
        """
        action_args = {"public_key": public_key}
        if access_key is not None:
            action_args["access_key"] = access_key
        return cls("AddKey", action_args)

    @classmethod
    def delete_key(cls, public_key: str) -> "BatchAction":
        """Create a DeleteKey batch action.
        
        Args:
            public_key: Public key to delete
            
        Returns:
            BatchAction instance for deleting a key
        """
        return cls("DeleteKey", {"public_key": public_key})

    @classmethod
    def stake(cls, amount: str, public_key: str) -> "BatchAction":
        """Create a Stake batch action.
        
        Args:
            amount: Amount to stake
            public_key: Public key for staking
            
        Returns:
            BatchAction instance for staking
        """
        return cls("Stake", {"amount": amount, "public_key": public_key})

    @classmethod
    def deploy_contract(cls, code: bytes) -> "BatchAction":
        """Create a DeployContract batch action.
        
        Args:
            code: Contract code as bytes
            
        Returns:
            BatchAction instance for deploying a contract
        """
        return cls("DeployContract", {"code": code.hex() if isinstance(code, bytes) else code})