from re import sub


TOKENS = {
    'NUMBER': 'NUMBER',
    'WORD': 'WORD',
    'TEXT': 'TEXT',
    'POINT': 'POINT',
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
    'WHILE': 'WHILE',
    'FOR': 'FOR',
    'EOF': 'EOF',
    'PRINT': 'PRINT',
    'VARIABLE': 'VARIABLE',
    '{': 'LBRACE',
    '}': 'RBRACE',
    '[': 'LBRACKET',
    ']': 'RBRACKET',
    ',': 'COMMA',
}

VAR_TYPES = {'int', 'str', 'figure'}
DRAW_FUCNTIONS = {'intersection', 'difference', 'symmetric_difference', 'union'}
VAR_SUBTYPES = {'circle', 'polygon'} | DRAW_FUCNTIONS
FUNCTIONS = {'draw'}


class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value
    
    def __str__(self):
        return "TOKEN({}, {})".format(self.type, self.value)
    
    def __repr__(self):
        return self.__str__()


class Lexer:
    OPERATORS = {'+', '-', '*', '/', '(', ')', '=', '<', '>', '{', '}', '[', ']', ','}
    
    def __init__(self, text):
        self.text = sub(r'\/\*[\sU\S]*?\*\/', '', text)
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
        self.add_token(TOKENS["NUMBER"], self.parse_number())

    def parse_number(self):
        number_string = ""
        while self.current_char.isdigit():
            number_string += self.current_char
            self.next_char()

        return int(number_string)

    def tokenize_operator(self):
        self.add_token(TOKENS[self.current_char], self.current_char)
        self.next_char()

    def tokenize_word(self):
        word_string = ""
        while self.current_char.isalnum() or self.current_char == '_' or word_string in VAR_TYPES:
            word_string += self.current_char
            self.next_char()

        if word_string == 'print':
            self.add_token(TOKENS["PRINT"], word_string)
        elif word_string == 'if':
            self.add_token(TOKENS["IF"], word_string)
        elif word_string == 'else':
            self.add_token(TOKENS["ELSE"], word_string)
        elif word_string == 'while':
            self.add_token(TOKENS["WHILE"], word_string)
        elif word_string == 'for':
            self.add_token(TOKENS["FOR"], word_string)
        elif word_string.startswith('int ') or word_string.startswith('str') or \
        word_string.startswith('figure'):
            self.add_token(TOKENS['VARIABLE'], word_string)
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
