def bitwise_xor(self):
    """
    Parse a bitwise XOR expression according to the grammar:
        bitwise_xor : bitwise_and ( '|' bitwise_and )*
    The method consumes a sequence of bitwise_and expressions separated by the
    '|' operator and builds a left‑associative abstract syntax tree.
    """
    # Parse the first bitwise_and expression
    node = self.bitwise_and()

    # Consume any number of '|' operators followed by another bitwise_and
    while self.current_token.type == TokenType.OR:
        op_token = self.current_token
        self.eat(TokenType.OR)
        right = self.bitwise_and()
        node = BinOp(left=node, op=op_token, right=right)

    return node