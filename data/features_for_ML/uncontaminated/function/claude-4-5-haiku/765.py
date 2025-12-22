def bitwise_xor(self):
    # bitwise_xor: bitwise_and (| bitwise_and)*
    left = self.bitwise_and()
    while self.current_token and self.current_token.type == 'PIPE':
        self.eat('PIPE')
        right = self.bitwise_and()
        left = BinOp(left, Token('PIPE', '|'), right)
    return left