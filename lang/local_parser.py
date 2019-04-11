from expressions import (BinaryExpression, CircleObject, ConditionalExpression,
                         ConstantExpression, DrawObject, PointObject,
                         PolygonObject, UnaryExpression, ValueExpression)
from lexer import DRAW_FUCNTIONS, TOKENS, VAR_SUBTYPES, Token
from statement import (AssignStatement, BlockStatement, DrawStatement,
                       ForStatement, IfStatement, PrintStatement,
                       WhileStatement)


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
        result = BlockStatement()

        while not self.match(TOKENS['EOF']):
            result.add(self.statement())
        
        return result
    
    def statement_or_block(self):
        if self.match(TOKENS['{']):
            return self.block()
        else:
            return self.statement()

    def block(self):
        block = BlockStatement()

        while not self.match(TOKENS['}']):
            block.add(self.statement())

        return block

    def statement(self):
        if self.match('PRINT'):
            return PrintStatement(self.expression())
        elif self.current_token.value == 'draw':
            return DrawStatement(*self.draw_statement())
        elif self.match('IF'):
            return self.ifelse_statement()
        elif self.match('WHILE'):
            return self.while_statement()
        elif self.match('FOR'):
            return self.for_statement()
        return self.assignment_statement()

    def clear_statement(self):
        self.consume('WORD')
        self.consume('LPAREN')
        self.consume('RPAREN')
    
    def draw_statement(self):
        self.consume('WORD')
        self.consume('LPAREN')
        _object = self.primary()
        self.consume('COMMA')
        color = self.current_token.value
        self.consume('TEXT')
        self.consume('RPAREN')
        return (_object, color)

    def assignment_statement(self):
        variable = self.current_token.value
        if (self.match('VARIABLE') or self.match('WORD')) and self.get(0).type == "EQUAL":
            self.consume('EQUAL')
            if self.current_token.type is TOKENS['WORD'] and self.current_token.value in VAR_SUBTYPES:
                result = AssignStatement(variable, self.object_statement())
            else:
                result = AssignStatement(variable, self.expression())
            return result
        
        raise RuntimeError("Error when assignment")

    def object_statement(self):
        function = self.current_token
        self.consume('WORD')
        if function.value == 'circle':
            if self.consume('LPAREN').value == '[':
                point = self.point_statement()
            self.consume('COMMA')
            r = self.expression()
            self.consume('RPAREN')
            return CircleObject(point, r)
        elif function.value == 'polygon':
            points = []
            self.consume('LPAREN')
            while not self.match('RPAREN'):
                points.append(self.point_statement())
                if self.current_token.type == 'COMMA':
                    self.consume('COMMA')
            return PolygonObject(points)
        elif function.value in DRAW_FUCNTIONS: 
            object1 = self.consume('LPAREN').value
            self.consume('WORD')
            object2 = self.consume('COMMA').value
            self.consume('WORD')
            self.consume('RPAREN')
            return DrawObject(function.value, object1, object2) 

    def point_statement(self):
        self.consume('LBRACKET')
        while not self.match('COMMA'):
            x = self.expression()

        while not self.match('RBRACKET'):
            y = self.expression()
        
        return PointObject(x, y)

    def ifelse_statement(self):
        condition = self.expression()
        if_statement = self.statement_or_block()
        if self.match(TOKENS['ELSE']):
            else_statement = self.statement_or_block()
        else:
            else_statement = None

        return IfStatement(condition, if_statement, else_statement)

    def while_statement(self):
        condition = self.expression()
        statement = self.statement_or_block()
        return WhileStatement(condition, statement)

    def for_statement(self):
        initialization = self.assignment_statement()
        self.consume(TOKENS[','])
        termination = self.expression()
        self.consume(TOKENS[','])
        increment = self.assignment_statement()
        statement = self.statement_or_block()
        return ForStatement(initialization, termination, increment, statement)

    def expression(self):
        return self.conditional()

    def conditional(self):
        result = self.additive()
        while True:
            if self.match(TOKENS['=']):
                result = ConditionalExpression('=', result, self.additive())
                continue
            elif self.match(TOKENS['>']):
                result = ConditionalExpression('>', result, self.additive())
                continue
            elif self.match(TOKENS['<']):
                result = ConditionalExpression('<', result, self.additive())
                continue
            break

        return result

    def additive(self):
        result = self.multiplicative()
        while True:
            if self.match(TOKENS['+']):
                result = BinaryExpression('+', result, self.multiplicative())
                continue
            elif self.match(TOKENS['-']):
                result = BinaryExpression('-', result, self.multiplicative())
                continue
            break
            
        return result

    def multiplicative(self):
        result = self.unary()
        while True:
            if self.match(TOKENS['*']):
                result = BinaryExpression('*', result, self.unary())
                continue
            elif self.match(TOKENS['/']):
                result = BinaryExpression('/', result, self.unary())
                continue
            break
            
        return result

    def unary(self):
        if self.match(TOKENS['-']):
            return UnaryExpression('-', self.primary())
        elif self.match(TOKENS['+']):
            return self.primary()

        return self.primary()
    
    def primary(self):
        token = self.current_token
        if self.match('NUMBER'):
            return ValueExpression(token.value)
        elif self.match('WORD'):
            return ConstantExpression(token.value)
        elif self.match('TEXT'):
            return ValueExpression(token.value)
        elif self.match('LPAREN'):
            result = self.expression()
            self.match('RPAREN')
            return result
        else:
            raise RuntimeError("Unknown Expression")

    def consume(self, token_type):
        if self.current_token.type != token_type:
            raise TypeError("Inappropriate type: Got {}, but {} expected.".format(self.current_token.type, token_type))
        else:
            self.position += 1
            return self.current_token 

    def match(self, token_type):
        if self.current_token.type != token_type:
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
