"""
*********************************************************************************
*                          Intel 8080 Assembler                                 *
*                                                                               *
*********************************************************************************
"""
# Definitely needs a parser
# from <file> import <something>
from cpu import CPU
import re


class Token:
    def __init__(self, type, val):
        self.value = val
        self.type = type


class Tokentype(enum.Enum):
    # TOKEN types
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    EOF = "EOF"
    SEMI = "SEMI"
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"
    NE = "NE"
    COLON = "COLON"
    COMMAND = "COMMAND"
    COMMENT = "COMMENT"
    REGISTER = "REGISTER"
    HEX = "HEX"



class Lexer:

    def __init__(self, cpu):
        self.text = None
        self.pos = 0
        self.current_char = None
        self.current_token = None
        self.cpu = cpu

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        """Return a multichar identifier consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def comment(self):
        """Comment - ignore text and just consume everything left"""
        while self.current_char is not None:
            self.advance()

    def hex(self):
        "Return hex value consumed from input"
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return int(result, 16)

    def string(self):
        """Return a string consumed from the input."""
        result = ""
        self.advance()  # move past the quote identifier
        while self.current_char is not None and self.current_char is not '"':
            result += self.current_char
            self.advance()
        self.advance()  # move past the closing quote identifier
        return result

    def peek(self):
        """Peek at the next character without advancing"""
        return self.text[self.pos + 1]

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "$":
                self.advance()
                return Token(Tokentype.INTEGER, self.hex())

            if self.current_char.isdigit():
                return Token(Tokentype.INTEGER, self.integer())

            if self.current_char == "A":
                if self.peek() == "," or self.peek() == " ":  # register A
                    self.advance()
                    return Token(Tokentype.REGISTER, "A")

            if self.current_char == "B":
                if self.peek() == "," or self.peek() == " ":  # register B
                    self.advance()
                    return Token(Tokentype.REGISTER, "B")

            if self.current_char == "C":
                if self.peek() == "," or self.peek() == " ":  # register C
                    self.advance()
                    return Token(Tokentype.REGISTER, "C")

            if self.current_char == "D":
                if self.peek() == "," or self.peek() == " ":  # register D
                    self.advance()
                    return Token(Tokentype.REGISTER, "D")

            if self.current_char == "E":
                if self.peek() == "," or self.peek() == " ":  # register E
                    self.advance()
                    return Token(Tokentype.REGISTER, "E")

            if self.current_char == "H":
                if self.peek() == "," or self.peek() == " ":  # register H
                    self.advance()
                    return Token(Tokentype.REGISTER, "H")

            if self.current_char == "L":
                if self.peek() == "," or self.peek() == " ":  # register L
                    self.advance()
                    return Token(Tokentype.REGISTER, "L")

            if self.current_char == "M":
                if self.peek() == "," or self.peek() == " ":  # memory location
                    self.advance()
                    return Token(Tokentype.REGISTER, "M")

            if self.current_char.isalpha():  # must start with alpha char
                value = self.identifier()
                if value.upper in self.cpu.commands:
                    return Token(Tokentype.COMMAND, value)
                else:
                    return Token(Tokentype.IDENTIFIER, value)

            if self.current_char == '"':  # double quote for string identity
                return Token(Tokentype.STRING, self.string())

            if self.current_char == '+':
                self.advance()
                return Token(Tokentype.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(Tokentype.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(Tokentype.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(Tokentype.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(Tokentype.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(Tokentype.RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(Tokentype.EQUALS, '=')

            if self.current_char == ';':
                self.advance()
                self.comment()
                continue

            if self.current_char == ':':
                self.advance()
                return Token(Tokentype.COLON, ':')

            if self.current_char == ">":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(Tokentype.GTE, ">=")
                else:
                    self.advance()
                    return Token(Tokentype.GT, ">")

            if self.current_char == "<":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(Tokentype.LTE, "<=")
                elif self.peek() == ">":
                    self.advance()
                    self.advance()
                    return Token(Tokentype.NE, "<>")
                else:
                    self.advance()
                    return Token(Tokentype.LT, "<")

            self.error()

        return Token(Tokentype.EOF, None)


class Assembler:
    def __init__(self, cpu):
        self.cpu = cpu
        self.lexer = Lexer(self.cpu)
        self.asmram = bytearray(0xFFFF)  # assemblers own ram space
        self.st = {}  # symbol table
        self.counter = 0  # current address to assemble code at
        self.commands = {  # internal assembler directives
            "ORG": self.org,
            "EQU": self.equ,
            "SET": self.set,
        }
        self.label = ""
        self.command = ""
        self.operand = ""
        self.errorlist = []
        self.line = None
        self.lineno = 0
        self.current_token = None

    def consume(self, content):
        # consume a token and advance if the current token matches else error
        if self.current_token.type == content:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def assemble_line(self, text):
        """Assembles a line of text.
           (identifier)? command (";" comment)?
        """
        self.label = self.command = self.operand = ""
        self.lexer.text = text
        self.lexer.current_token = self.lexer.get_next_token()
        # process identifier if present
        while self.lexer.current_token.type == Tokentype.IDENTIFIER:
            token = self.current_token
            self.consume(Tokentype.IDENTIFIER)
            self.st.update({token.value: self.counter})
            self.label = token.value
        # process command
        self.execute_command()
        # process comment if present
        while self.lexer.current_token.type == Tokentype.COMMENT:
            self.consume(Tokentype.COMMENT)

        # if command is a psuedo command then perform the action
        if self.command in self.commands:
            self.commands.get(self.command)()  # execute psuedo command
        else:
            # do the real command assembly here
            if self.operand == "":
                instruction = self.command
            else:
                instruction = self.command + " " + self.operand
            if instruction in self.cpu.mnemonic:
                # single byte direct hit
                self.asmram[self.counter] = self.cpu.mnemonic.get(instruction)
                self.counter += 1
            else:
                self.insert_address()

    def execute_command(self):
        """ command ( expression ("," expression)? )? """



    def insert_address(self):
        if "," in self.operand:
            val = self.operand.split(",")[1]
            op = self.operand.split(",")[0]
        else:
            val = self.operand
            op = ""
        addr = -1
        if val in self.st:
            addr = self.st.get(val)
        else:
            try:
                addr = int(val, 16)
            except ValueError:
                self.error("Invalid address")
        if 0 <= addr <= 0xFF:
            instruction = self.command + " " + op + ",{:02X}"
            if instruction in self.cpu.mnemonic:
                # two  byte instruction
                self.asmram[self.counter] = self.cpu.mnemonic.get(instruction)
                self.counter += 1
                self.asmram[self.counter] = addr
                self.counter += 1
            else:
                self.error()
        elif 0x100 <= addr <= 0xFFFF:
            instruction = self.command + " " + op + ",{:04X}"
            if instruction in self.cpu.mnemonic:
                # three  byte instruction - lsb then msb
                opcode = self.cpu.mnemonic.get(instruction)
                self.asmram[self.counter] = opcode
                self.counter += 1
                self.asmram[self.counter] = addr & 0xFF
                self.counter += 1
                self.asmram[self.counter] = addr >> 8
                self.counter += 1
            else:
                self.error()
        else:
            self.error("Invalid Address")

    def error(self, msg = "Invalid Command"):
        msg = "Error - line {}: {} >> {} <<".format(self.lineno,self.line, msg)
        self.errorlist.append(msg)


    def org(self):
        pass

    def equ(self):
        pass

    def set(self):
        pass

    def assemble_file(self):
        with open("sample.src", "r") as file:
            for line in file:
                self.lineno += 1
                self.line = line
                self.assemble_line(line)

    def save_binary(self):
        with open("sample.bin", "wb") as file:
            file.write(self.asmram)

def main():
    cpu = CPU()
    asm = Assembler(cpu)
    asm.assemble_file()
    if len(asm.errorlist) == 0:
        # it worked so save file
        asm.save_binary()
    else:
        print("Assembly Failed")
        for e in asm.errorlist:
            print(e)

if __name__ == "__main__":
    main()
