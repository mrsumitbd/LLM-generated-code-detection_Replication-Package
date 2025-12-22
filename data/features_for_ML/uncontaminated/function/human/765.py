from .Node import (
    NodeArrayAssignment,
    NodeArrayGetElement,
    NodeArraySetElement,
    NodeFunctionCall,
    NodeTernary,
    NodeToken,
    NodeUnaryPostfix,
    NodeUnaryPrefix,
)
from .Token import Token

def bitwise_xor(self):
        # bitwise_xor: bitwise_and (| bitwise_and)*

        n = self.bitwise_and()

        token = self.parser.current_token()
        while token is not None and token.type == Token.BITWISE_XOR:
            self.parser.advance_token()
            next_bitwise_and = self.bitwise_and()

            new_node = NodeToken(self.ids_map_list, token=token, left=n, right=next_bitwise_and)
            n = new_node

            token = self.parser.current_token()

        return n