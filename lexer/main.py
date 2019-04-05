from lexer import Lexer
from local_parser import Parser
from matplotlib import pyplot


if __name__ == "__main__":
    with open("../programs/program2.ffy") as f:
        input_text = f.read()
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print(tokens)
    parser = Parser(tokens)
    program = parser.parse()
    program.execute()
    pyplot.show()