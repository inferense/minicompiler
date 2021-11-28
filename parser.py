import sys
from lexer import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.symbols = set()
        self.currentToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    def checkToken(self, kind):
        return kind == self.currentToken.kind

    def nextToken(self):
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def match(self, kind):
        if not self.checkToken(kind):
            return sys.exit("expected " + kind.name + ", got " + self.currentToken.kind.name)
        self.nextToken()

    def abort(self, message):
        return sys.exit("parser error:" + message)

    # start the parser
    def program(self):
        print('PROGRAM')

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        # ignore goto for now
        # for label in self.labelsGoTo:
        #     if label not in self.labelsDeclared:
        #         self.abort

    # parse for statement
    def statement(self):
        if self.checkToken(TokenType.PRINT):
            print('PRINT-STATEMENT')
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        elif self.checkToken(TokenType.IF):
            print("IF-STATEMENT")

            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)

        elif self.checkToken(TokenType.WHILE):
            print("WHILE-LOOP")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)

            self.nl()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)

        elif self.checkToken(TokenType.LET):
            print("LET-STATEMENT")
            self.nextToken()

            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.checkToken(TokenType.INPUT):
            print("INPUT-STATEMENT")
            self.nextToken()

            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)

            self.match(TokenType.IDENT)

        else:
            self.abort("invalid statement: " + self.currentToken.text + "(" + self.currentToken.kind.name + ")")

        self.nl()

    def primary(self):
        print("PRIMARY (" + self.currentToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.currentToken.text not in self.symbols:
                self.abort("referencing variable before assignment: " + self.currentToken.text)
            self.nextToken()
        else:
            self.abort("unexpected token: " + self.currentToken.text)

    def unary(self):
        print("UNARY")
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def term(self):
        print("TERM")
        self.unary()
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    def expression(self):
        print("EXPRESSION")
        self.term()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LTEQ) \
               or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def comparison(self):
        print("COMPARISON")
        self.expression()
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("expected comparison operator: " + self.currentToken.text)

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()


