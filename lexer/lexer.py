TokenType = {
    'NUMBER': 'NUMBER',
    'PLUS' : '+', 
    'MINUS' : '-', 
    'MULTIPLY' : '*', 
    'DIVIDE' : '/',
    'EOF': 'EOF',
}

class Token:
    def __init__(self, token_type, text):
        self.token_type = token_type
        self.text = text

class Lexer:
    def __init__(self, text):
        self.text = text
        self.text_lenght = len(self.text)
        self.position = 0
        self.tokens = []
    
    def tokenize(self):
        pass

    def next(self):
        self.position += 1
        return self.peek(0)

    def peek(self, relative_position):
        position = self.position + relative_position
        if position >= self.text_lenght:
            return '\0'
        else:
            return self.text[position]

    def add_token(self, token_type, text=None):
        self.tokens.append(Token(token_type, text))


