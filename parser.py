import sys
from lexer import *


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

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
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        # ignore goto for now
        # for label in self.labelsGoTo:
        #     if label not in self.labelsDeclared:
        #         self.abort

    # parse for statement
    def statement(self):
        if self.checkToken(TokenType.PRINT):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("printf(\"" + self.currentToken.text + "\\n\");")
                self.nextToken()
            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

        elif self.checkToken(TokenType.IF):

            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")

        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.emitter.emitLine("){")

            self.nl()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")

        elif self.checkToken(TokenType.LET):
            self.nextToken()

            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.headerLine("float " + self.currentToken.text + ";")

            self.emitter.emit(self.currentToken.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emitLine(";")

        elif self.checkToken(TokenType.INPUT):
            self.nextToken()

            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)
                self.emitter.headerLine("float " + self.currentToken.text + ";")

            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.currentToken.text + ")) {")
            self.emitter.emitLine(self.currentToken.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")

            self.match(TokenType.IDENT)

        else:
            self.abort("invalid statement: " + self.currentToken.text + "(" + self.currentToken.kind.name + ")")

        self.nl()

    def primary(self):

        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.currentToken.text not in self.symbols:
                self.abort("referencing variable before assignment: " + self.currentToken.text)

            self.emitter.emit(self.currentToken.text)
            self.nextToken()
        else:
            self.abort("unexpected token: " + self.currentToken.text)

    def unary(self):
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
        self.primary()

    def term(self):
        self.unary()
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.unary()

    def expression(self):
        self.term()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.term()

    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LTEQ) \
               or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def comparison(self):
        self.expression()
        if self.isComparisonOperator():
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.expression()
        else:
            self.abort("expected comparison operator: " + self.currentToken.text)

        while self.isComparisonOperator():
            self.emitter.emit(self.currentToken.text)
            self.nextToken()
            self.expression()

    def nl(self):
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()


