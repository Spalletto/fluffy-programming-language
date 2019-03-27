from lexer import Lexer
from local_parser import Parser

if __name__ == "__main__":
    input_text = '22*10 - 5+10'
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print(tokens)
    parser = Parser(tokens)
    print(parser.parse())