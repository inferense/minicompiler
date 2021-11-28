from lexer import *
from parser import *
import sys


def main():
    print("compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: compiler needs source file as argument")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    parser = Parser(lexer)

    parser.program() # start the parser
    print('parsing complete')

main()
