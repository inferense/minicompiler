# compiler: 
# 1. lexer - tokenizer
# 2. parser - ordered instructions? - program tree
# 3. emitter - compiled code in C

from enum import Enum
import sys


class Lexer:
    def __init__(self, data):
        self.source = data + '\n'  # append a newline to simplify lexing the last token
        self.currrent_char = ''
        self.current_pos = -1
        self.nextChar()

    # to next char 
    def nextChar(self):
        self.current_pos += 1
        if self.current_pos >= len(self.source):
            self.currrent_char = '\0'  # EOF
        else:
            self.currrent_char = self.source[self.current_pos]

    # lookahead
    def peek(self):
        if self.current_pos + 1 >= len(self.source):  # if EOF return EOF, else peek 1 increment
            return '\0'
        return self.source[self.current_pos + 1]

    # error msg for invalid token
    def abort(self, message):
        sys.exit("lexing error. " + message)

    # skip whitespcae except newlines (which are indicating end of statement)
    def skipWhitespace(self):
        while self.currrent_char == ' ' or self.currrent_char == '\t' or self.currrent_char == '\r':
            self.nextChar()

    def skipComment(self):
        if self.currrent_char == '#':
            while self.currrent_char != '\n':
                self.nextChar()

    # return the next token
    # there are different hierarchies of tokens (some can not be just separated with whitespace. e.g. operators, special chars, quote marks etc.)
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.currrent_char == '+':
            token = Token(self.currrent_char, TokenType.PLUS)

        elif self.currrent_char == '-':
            token = Token(self.currrent_char, TokenType.MINUS)

        elif self.currrent_char == '*':
            token = Token(self.currrent_char, TokenType.ASTERISK)

        elif self.currrent_char == '/':
            token = Token(self.currrent_char, TokenType.SLASH)

        elif self.currrent_char == '\n':
            token = Token(self.currrent_char, TokenType.NEWLINE)

        elif self.currrent_char == '\0':
            token = Token(self.currrent_char, TokenType.EOF)

        elif self.currrent_char == '=':
            if self.peek() == '=':
                token = Token(self.currrent_char + self.peek(), TokenType.EQEQ)
                self.nextChar()
            else:
                token = Token(self.currrent_char, TokenType.EQ)

        elif self.currrent_char == '!' and self.peek() == '=':
            token = Token(self.currrent_char + self.peek(), TokenType.NOTEQ)
            self.nextChar()

        elif self.currrent_char == '>':
            if self.peek() == '=':
                token = Token(self.currrent_char + self.peek(), TokenType.GTEQ)
                self.nextChar()
            else:
                token = Token(self.currrent_char, TokenType.GT)

        elif self.currrent_char == '<':
            if self.peek() == '=':
                token = Token(self.currrent_char + self.peek(), TokenType.LTEQ)
                self.nextChar()
            else:
                token = Token(self.currrent_char, TokenType.LT)

        elif self.currrent_char == '\"':
            self.nextChar()
            startPos = self.current_pos

            while self.currrent_char != '\"':
                if self.currrent_char == '\r' or self.currrent_char == '\n' or self.currrent_char == '\t' or self.currrent_char == '\\' or self.currrent_char == '%':
                    self.abort("illegal character in string")
                self.nextChar()
            tokText = self.source[startPos:self.current_pos]
            token = Token(tokText, TokenType.STRING)

        elif self.currrent_char.isdigit():
            startPos = self.current_pos

            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort('illegal digit')
                while self.peek().isdigit():
                    self.nextChar()

            tokDigit = self.source[startPos:self.current_pos + 1]
            token = Token(tokDigit, TokenType.NUMBER)

        elif self.currrent_char.isalpha():
            startPos = self.current_pos
            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos:self.current_pos + 1]
            keyword = Token.keywordCheck(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)

        else:
            self.abort("unknown token: " + self.currrent_char)

        self.nextChar()
        return token


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod  # method that belongs to the class rather than instance of the Token class
    def keywordCheck(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:  # access enum classes by value, or name
                return kind
        return None


class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
