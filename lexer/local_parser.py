from lexer import *
from expressions import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    @property
    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else: 
            return Token('EOF', 'EOF')

    def parse(self):
        result = []

        while not self.match(TOKENS['EOF']):
            result.append(self.expression())
        
        return result

    def expression(self):
        return self.additive()

    def additive(self):
        result = self.multiplicative()
        while True:
            if self.match(TOKENS['+']):
                expression = BinaryExpression('+', result, self.multiplicative())
                result = expression.evaluate()
                continue
            elif self.match(TOKENS['-']):
                expression = BinaryExpression('-', result, self.multiplicative())
                result = expression.evaluate()
                continue
            break
            
        return result

    def multiplicative(self):
        result = self.unary()
        while True:
            if self.match(TOKENS['*']):
                expression = BinaryExpression('*', result, self.unary())
                result = expression.evaluate()
                continue
            elif self.match(TOKENS['/']):
                expression = BinaryExpression('/', result, self.unary())
                result = expression.evaluate()
                continue
            break
            
        return result

    def unary(self):
        if self.match(TOKENS['-']):
            expression = UnaryExpression('-', self.primary())
            return expression.evaluate()
        elif self.match(TOKENS['+']):
            expression = UnaryExpression('+', self.primary())
            return expression.evaluate()

        return self.primary()
    
    def primary(self):
        token = self.current_token
        if self.match('NUMBER'):
            return NumberExpression(token.value)
        if self.match('WORD'):
            result = ConstantExpression(token.value)
            return result.evaluate()
        elif self.match('LPAREN'):
            result = self.expression()
            self.match('RPAREN')
            return result
        else:
            raise RuntimeError("Unknown Expression")

    def match(self, token_type):
        if self.current_token.token_type != token_type:
            return False
        else:
            self.position += 1
            return True 

    def get(self, relative_position):
        position = self.position + relative_position
        if position > len(self.tokens):
            return TOKENS['EOF']
        else:
            return self.tokens[position]

        