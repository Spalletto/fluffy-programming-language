from lexer import Lexer
from local_parser import Parser

if __name__ == "__main__":
    with open("../programs/program.ffy") as f:
        input_text = f.read()
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print(tokens)
    parser = Parser(tokens)
    program = parser.parse()
    program.execute()
    

# name = 2+2*10
# name2 = 50/(8+2)
# str = "HUY!"
# print name
# print "Hello World"
# print name2