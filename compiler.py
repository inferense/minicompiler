from lexer import *
from parser import *
from emitter import *

import sys


def main():
    print("compiling...")

    if len(sys.argv) != 2:
        sys.exit("Error: compiler needs source file as argument")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)


    parser.program() # start the parser
    emitter.writeFile()
    print('parsing complete')


main()
