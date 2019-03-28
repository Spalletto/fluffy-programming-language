TOKENS = {
    'NUMBER' : 'NUMBER',
    'WORD' : 'WORD',
    '+' : 'PLUS', 
    '-' : 'MINUS', 
    '*' : 'MULTIPLY', 
    '/' : 'DIVIDE',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '=' : 'EQUAL',
    'EOF': 'EOF',
}

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
    def __str__(self):
        return f"TOKEN({self.token_type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()

class Lexer:
    OPERATORS = ('+', '-', '*', '/', '(', ')', '=')
    
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

    def tokenize_word(self):
        word_string = ""
        while self.current_char.isalnum():
            word_string += self.current_char
            self.next_char()

        self.add_token(TOKENS["WORD"], word_string)

    def tokenize_operator(self):
        self.add_token(TOKENS[self.current_char], self.current_char)
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


if __name__ == "__main__":
    input_text = '2+223'
    lexer = Lexer(input_text)
    print(lexer.tokenize())