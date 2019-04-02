TOKENS = {
    'NUMBER': 'NUMBER',
    'WORD': 'WORD',
    'TEXT': 'TEXT',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULTIPLY',
    '/': 'DIVIDE',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '=': 'EQUAL',
    '<': 'LT',
    '>': 'GT',
    'IF': 'IF',
    'ELSE': 'ELSE',
    'EOF': 'EOF',
    'PRINT': 'PRINT',
}


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
    def __str__(self):
        return "TOKEN({}, {})".format(self.token_type, self.value)
    
    def __repr__(self):
        return self.__str__()


class Lexer:
    OPERATORS = ('+', '-', '*', '/', '(', ')', '=', '<', '>')
    
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.tokens = []

    @property
    def current_char(self):
        if self.position < len(self.text):
            return self.text[self.position]
        else:
            return '\0'
    
    def tokenize(self):
        while self.position < len(self.text):
            if self.current_char.isdigit():
                self.tokenize_number()
            elif self.current_char == '"':
                self.tokenize_text()
            elif self.current_char.isalpha():
                self.tokenize_word()
            elif self.current_char in self.OPERATORS:
                self.tokenize_operator()
            else:
                self.next_char()

        return self.tokens
                 
    def tokenize_number(self):
        number_string = ""
        while self.current_char.isdigit():
            number_string += self.current_char
            self.next_char()

        self.add_token(TOKENS["NUMBER"], int(number_string))

    def tokenize_operator(self):
        self.add_token(TOKENS[self.current_char], self.current_char)
        self.next_char()

    def tokenize_word(self):
        word_string = ""
        while self.current_char.isalnum():
            word_string += self.current_char
            self.next_char()
        
        if word_string == 'print':
            self.add_token(TOKENS["PRINT"], word_string)
        elif word_string == 'if':
            self.add_token(TOKENS["IF"], word_string)
        elif word_string == 'else':
            self.add_token(TOKENS["ELSE"], word_string)
        else:
            self.add_token(TOKENS["WORD"], word_string)

    def tokenize_text(self):
        self.next_char()  # skip "
        word_string = ""
        while self.current_char != '"':
            if self.current_char == "\\":
                self.next_char()
                if self.current_char == '"':
                    word_string += '"'
                elif self.current_char == 'n':
                    word_string += '\n'
                else:
                    word_string += '\\'
                    continue
            word_string += self.current_char
            self.next_char()

        self.add_token(TOKENS['TEXT'], word_string)
        self.next_char()

    def next_char(self):
        self.position += 1

    def peek(self, relative_position):
        position = self.position + relative_position
        if position >= len(self.text):
            return '\0'
        else:
            return self.text[position]

    def add_token(self, token_type, text=None):
        self.tokens.append(Token(token_type, text))
