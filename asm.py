# INtel 8080 Assembler 
#
# An assembler in  the fashion of ASM from CP/M
# No complicated parsing just simple line based stuff
#
#  LABEL:  OP [, ARG2] ; COMMENT

# needs to be handle directives - ORG, EQU, DB, DW, DS, END
#
#
from instructions import INSTRUCTION_SET
import sys


# second version of Assembler with code cleanup

class Assembler:
    # todo add parsing of variables to assembler

    DIRECTIVES = {"ORG", "EQU", "DB", "DW", "DS", "END"}

    def __init__(self, org):
        self.binary = bytearray(16384)  # 16K of memory space for assembly code
        self.variables = {}  # dict of variable names from source file
        self.hexlist = []  # list of hex codes after assembly
        self.assembled = False  # flag to indicate successful assembly, can be checked before saving
        self.start_address = org  # start address for assembled code ( default 0x0100 0100H CPM TPA start)
        self.current_line = None  # current line for error reporting
        self.pass_mode = 0  # assembler pass through
        self.current_address = None  # current address during  assembly pass

    def assemble(self, filename="code"):
        with open("".join([filename, ".src"]), 'r') as file:
            source = file.readlines()
            print(source)
            try:
                self.pass_one(source)  # resolve variable addresses and org
                self.pass_two(source)  # attempt to assemble code
                print("Assembly Complete")
                self.assembled = True
            except ValueError as err:
                print(err)
                print("Failed - line {}".format(self.current_line))

    def pass_one(self, file):
        print("Running Pass One")
        print("Org at {:04X}".format(self.start_address))
        self.current_address = self.start_address
        self.pass_mode = 1
        for line in file:
            self.current_line = self.clean(line)
            if self.current_line is not None:
                command, arg, mode = self.parse()
                if command not in KEYWORDS:  # must be a variable
                    if arg is None:
                        self.variables[command] = self.current_address
                    else:
                        self.variables[command] = arg
                else:  # parse commands and increment address
                    result_list = self._tokenize(command, arg, mode)
                    if len(result_list) > 0:
                        self.current_address += len(result_list)  # update address

    def pass_two(self, file):
        print("Running Pass Two")
        self.pass_mode = 2
        self.current_address = self.start_address
        for line in file:
            self.current_line = self.clean(line)
            if self.current_line is not None:
                command, arg, mode = self.parse()
                if command in KEYWORDS:  # only create tokens for recognised instructions
                    result_list = self._tokenize(command, arg, mode)
                    if len(result_list) > 0:
                        self.current_address += len(result_list)  # update address
                        print("Current address {}".format(self.current_address))
                        for hexcode in result_list:
                            self.hexlist.append(hexcode)
        self._convert_binary()

    def save(self, filename):
        file = "".join([filename, ".bin"])
        with open(file, 'wb') as f:
            f.write(self.binary)
        print("{} binary "
              "file created!".format(file))

    def _convert_binary(self):
        location = 0
        print(self.hexlist)
        for h in self.hexlist:
            self.binary[location] = h
            location += 1

    def _tokenize(self, command, arg, mode):
        """
        Lookup and return bytecode for the command, the command has already been validated
        and the address resolved, so simple routine to return the bytes
        :param command - the KEYWORD
        :param arg - the address value ( or None if not applicable)
        :param mode - the address mode ( or None if not applicable)
        :returns: a list of byte values
        :raises ValueError: call function from within try..except block to catch syntax errors
        """
        bytelist = []
        # first see if command is a single instruction
        if SINGLE_OPCODES.get(command) is not None:
            bytelist.append(SINGLE_OPCODES[command])
        else:
            lookup = "".join([command, "_", mode])
            if OPCODES.get(lookup) is not None:
                bytelist.append(OPCODES[lookup])
            address = arg
            if address is not None:
                if address < 256:
                    bytelist.append(address)
                else:
                    msb = int(address / 256)
                    lsb = (address - (msb * 256))
                    bytelist.append(lsb)
                    bytelist.append(msb)
        return bytelist

    def parse(self):
        """
        This will parse line input into a command and an argument
        returns:    command - string
                    val - integer value of argument
                    mode - address mode for an address

        """
        words = self.current_line.split()
        command = words[0]
        if len(words) > 1:
            val, mode = self.resolve_arg(words[1])
        else:
            val = None
            mode = ""
        return command, val, mode

    def resolve_arg(self, arg):
        """
        Do some clever stuff to return an argument value and an address mode
        """
        val = None
        mode = ""
        copy = arg  # create a copy of the argument for slicing
        if copy == "A":  # accumulator
            mode = "accumulator"
        elif copy[:2] == "#$":  # immediate address
            copy = copy[2:]
            mode = "immediate"
        elif copy[:2] == "($" and copy[-3:] == ",X)":  # indirect x
            copy = copy[2:len(copy) - 3]
            mode = "indirect_x"
        elif copy[:2] == "($" and copy[-3:] == "),Y":  # indirect y
            copy = copy[2:len(copy) - 3]
            mode = "indirect_y"
        elif copy[:2] == "($" and copy[-1] == ")":  # indirect
            copy = copy[2:-1]
            mode = "indirect"
        elif copy[0] == "$" and copy[-2:] == ",X":  # indexed x
            copy = copy[1:len(copy) - 2]
            mode = "_x"
        elif copy[0] == "$" and copy[-2:] == ",Y":  # indexed y
            copy = copy[1:len(copy) - 2]
            mode = "_y"
        elif copy[0] == "$":  # direct address
            copy = copy[1:]
        else:
            raise ValueError("Invalid address mode")
        # need to set address to None
        if mode != "accumulator":  # don't need to calculate address for accumulator
            val, mode = self._calculate_address(copy, mode)
        return val, mode

    def _calculate_address(self, val, mode):
        """
        Calculate the hex value of the operand
        param: operand - contains either variable name or address
        """
        address = -9999  # start with an invalid address
        # first see if the value  is actually a  variable name
        if self.variables.get(val) is not None:
            address = self.variables.get(val)
        else:
            try:
                address = int(val, 16)  # convert hex to integer
            except ValueError as er:
                print("Invalid address")
        if -1 < address < 0xFFFF:
            if -1 < address < 0xFF and mode != "immediate":  # 0 - 255  it's a zeropage address
                mode = "".join(["zeropage", mode])
            elif 256 < address < 0xFFFF:  # 256 - 64  it's an absolute address
                mode = "".join(["absolute", mode])
        else:
            raise ValueError("Address out of range")
        return address, mode

    def clean(self, text):
        """
        Routine to trim input and strip newline
        Will also remove comments
        param: line - input text
        returns: clean text or None if line is a comment
        """
        line = text.strip("\n").strip()  # remove newline and whitespace
        if line[0] == ";":  # line is a comment so ignore it
            line = None
        else:
            line = line.split(";")[0]  # remove any inline comments - assume anything after ; is ignored
        return line


def get_opcodes():
    """
    Function to map list of valid commands and produce a dictionary of opcodes.
    """
    #
    # could try this using a filter command but how to get the position value for the dict key?
    # The example below will filter the list of all instructions ignoring those which are "???"
    # and produce a new list
    #
    # map_result = list(filter(lambda x: x[0] != "???", INSTRUCTIONS))
    #
    #
    singlelist = {}
    codelist = {}
    for i in range(len(INSTRUCTIONS)):
        cmd = INSTRUCTIONS[i][0].format(0)
        if cmd[0:3] != "???":
            # if a single byte instruction put it in a separate list
            # Accumulator is the exception and is handled as 2 byte
            if INSTRUCTIONS[i][1] == 1 and len(cmd) < 4:  # Accumulator command length will be longer than 4
                singlelist[cmd] = i
            else:
                codelist[cmd] = i
    return singlelist, codelist


def get_keywords():
    keywords = []
    for i in range(len(INSTRUCTIONS)):
        cmd = INSTRUCTIONS[i][0].format(0)[0:3]
        mode = INSTRUCTIONS[i][2]
        if cmd != "???":
            if cmd not in keywords:
                keywords.append("".join([cmd, "_", mode]))
    return keywords


SINGLE_OPCODES, OPCODES = get_opcodes()
KEYWORDS = get_keywords()


def main(org):
    asm = Assembler(org)
    asm.assemble()
    if asm.assembled:
        print(asm.variables)
        for h in asm.hexlist:
            print("{:02X}".format(h))
        asm.save("code")


if __name__ == '__main__':
    print(KEYWORDS)
    print(SINGLE_OPCODES)
    print(OPCODES)
    org = 0x0100
    if len(sys.argv) > 1:
        try:
            org = int(sys.argv[1], 16)
        except ValueError as err:
            print(err)
    main(org)
