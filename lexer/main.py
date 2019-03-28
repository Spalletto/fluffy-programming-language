from lexer import Lexer
from local_parser import Parser

if __name__ == "__main__":
    input_text = 'name = 2+2*10'
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print(tokens)
    parser = Parser(tokens)
    statements = parser.parse()
    for s in statements:
        s.execute()
        print(s)