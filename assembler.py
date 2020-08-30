"""
*********************************************************************************
*                          Intel 8080 Assembler                                 *
*                                                                               *
*********************************************************************************
"""
# Definitely needs a parser
# from <file> import <something>
from cpu import CPU
import enum

registers = {
    "B": 0,
    "C": 1,
    "D": 2,
    "E": 3,
    "H": 4,
    "L": 5,
    "M": 6,
    "A": 7,
}

registerpair = {
    "B": 0,
    "D": 1,
    "H": 2,
    "SP": 3,
}

commands = {
    "MOV",
    "NOP",
    "INX",
    "LXI",
    "STAX",
    "INR",
    "DCR",
    "MVI"
}
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
    EOL = "EOL"
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
    COMMA = "COMMA"



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
        """Return hex value consumed from input"""
        result = ""
        while self.current_char is not None and self.current_char in "0123456789ABCDEF":
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
        if self.pos == len(self.text) - 1:
            return None
        else:
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
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register A
                    self.advance()
                    return Token(Tokentype.REGISTER, "A")

            if self.current_char == "B":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register B
                    self.advance()
                    return Token(Tokentype.REGISTER, "B")

            if self.current_char == "C":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register C
                    self.advance()
                    return Token(Tokentype.REGISTER, "C")

            if self.current_char == "D":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register D
                    self.advance()
                    return Token(Tokentype.REGISTER, "D")

            if self.current_char == "E":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register E
                    self.advance()
                    return Token(Tokentype.REGISTER, "E")

            if self.current_char == "H":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register H
                    self.advance()
                    return Token(Tokentype.REGISTER, "H")

            if self.current_char == "L":
                if self.peek() == "," or self.peek() == " " or self.peek() is None:  # register L
                    self.advance()
                    return Token(Tokentype.REGISTER, "L")

            if self.current_char == "M":
                if self.peek() == "," or self.peek() == " " or self.peek()  is None:  # memory location
                    self.advance()
                    return Token(Tokentype.REGISTER, "M")

            if self.current_char.isalpha():  # must start with alpha char
                value = self.identifier()
                if value.upper() in commands:
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

            if self.current_char == ',':
                self.advance()
                return Token(Tokentype.COMMA, ',')

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

        return Token(Tokentype.EOL, None)


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
        self.command_list = {
            "MOV": self.mov,
            "MVI": self.mvi,
            "LXI": self.lxi,
        }

    def consume(self, content):
        # consume a token and advance if the current token matches else error
        if self.lexer.current_token.type == content:
            self.lexer.current_token = self.lexer.get_next_token()
        else:
            self.error("Syntax Error")

    def assemble_line(self):
        """Assembles a line of text.
           (identifier)? command (";" comment)?
        """
        self.label = self.command = self.operand = ""
        self.lexer.text = self.line
        self.lexer.pos = 0
        self.lexer.current_char = self.lexer.text[self.lexer.pos]
        self.lexer.current_token = self.lexer.get_next_token()
        # process identifier if present
        while self.lexer.current_token.type == Tokentype.IDENTIFIER:
            token = self.lexer.current_token
            self.consume(Tokentype.IDENTIFIER)
            self.st.update({token.value: self.counter})
            self.label = token.value
        # process command
        while self.lexer.current_token.type == Tokentype.COMMAND:
            self.execute_command()
        # process comment if present
        while self.lexer.current_token.type == Tokentype.COMMENT:
            self.consume(Tokentype.COMMENT)

    def execute_command(self):
        """ command ( expression ("," expression)? )? """
        self.command = self.lexer.current_token.value.upper()
        self.consume(Tokentype.COMMAND)
        opcode = self.command_list.get(self.command)()
        # verbose code
        output = "Line {} {} :> Command {:02X} : ".format(self.lineno, self.line,opcode[0],opcode[0])
        if len(opcode) == 2:
            output += "Data {:02X}".format(opcode[1])
        elif len(opcode) == 3:
            addr = opcode[2] << 8 | opcode[1]
            output += "Address {:04X}".format(addr)
        print(output)
        # insert values into Assembler RAM
        for i in opcode:
            self.asmram[self.counter] = i
            self.counter += 1

    def single(self):
        if self.command == "NOP":
            return [0x76]
        elif self.command == "RLC":
            return [0xdd]
        elif self.command == "RRC":
            return [0xdD]
        elif self.command == "RAL":
            return [0xdd]
        elif self.command == "RAR":
            return [0xdD]
        elif self.command == "DAA":
            return [0xdd]
        elif self.command == "CMA":
            return [0xdD]
        elif self.command == "STC":
            return [0xdd]
        elif self.command == "CMC":
            return [0xdD]
        elif self.command == "HLT":
            return [0xdd]
        elif self.command == "RNZ":
            return [0xDd]
        elif self.command == "RZ":
            return [0xDd]
        elif self.command == "RET":
            return [0xDd]
        elif self.command == "RNC":
            return [0xDd]
        elif self.command == "RC":
            return  0xD8
        elif self.command == "RPO":
            return [0xDd]
        elif self.command == "XTHL":
            return [0xDd]
        elif self.command == "RPE":
            return [0xDd]
        elif self.command == "PCHL":
            return [0xDd]
        elif self.command == "XCHG":
            return [0xDD]
        elif self.command == "RP":
            return [0xDd]
        elif self.command == "DI":
            return [0xDd]
        elif self.command == "RM":
            return [0xDd]
        elif self.command == "SPHL":
            return [0xDd]
        elif self.command == "EI":
            return [0xDD]

    def mov(self):
        dst = self.lexer.current_token
        self.consume(Tokentype.REGISTER)
        self.consume(Tokentype.COMMA)
        src = self.lexer.current_token
        self.consume(Tokentype.REGISTER)
        if src.value == "M" and dst.value == "M":
            self.error("Invalid register - M,M")
        # mov command 01dddsrc
        return [(1 << 6 ) | (registers.get(dst.value) << 3) | registers.get(src.value)]

    def mvi(self):
        dst = self.lexer.current_token
        self.consume(Tokentype.REGISTER)
        self.consume(Tokentype.COMMA)
        val = self.lexer.current_token
        self.consume(Tokentype.INTEGER)
        return [(registers.get(dst.value) << 3) | 0x06, val.value & 0xFF]

    def lxi(self):
        rp = self.lexer.current_token
        self.consume(Tokentype.REGISTER)
        if rp.value in registerpair:
            bitval = registerpair.get(rp.value)
        else:
            self.error("Invalid register pair")
            return [0]
        self.consume(Tokentype.COMMA)
        val = self.lexer.current_token
        self.consume(Tokentype.INTEGER)
        return [(bitval << 4) | 0x01, val.value & 0xFF, val.value >> 8]

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
        msg = "Line {}: {} :> {} ".format(self.lineno, self.line, msg)
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
                self.line = line[:-1]
                if self.line[0] != ";":
                    self.assemble_line()

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
