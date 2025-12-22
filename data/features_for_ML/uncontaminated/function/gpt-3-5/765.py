def bitwise_xor(self):
    result = self.bitwise_and()
    while self.current_token.type == TokenType.BITWISE_OR:
        self.eat(TokenType.BITWISE_OR)
        result ^= self.bitwise_and()
    return result