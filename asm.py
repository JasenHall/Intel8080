# INtel 8080 Assembler 
#
# An assembler in  the fashion of ASM from CP/M
# No complicated parsing just simple line based stuff
#
#  LABEL:  OP [, ARG] ; COMMENT

# needs to be handle directives - ORG, EQU, DB, DW, DS, END
#
#
from instructions import INSTRUCTION_SET as INSTRUCTIONS
import sys
import re
import shlex
import os


# second version of Assembler with code cleanup
# still fairly hacky with hand rolled parsing but hey it works
#
# could probaly use regex to clean up the parsing
# I'm sure the patterns could handle the seperators within strings

class Hexfile:

    CHUNK_SIZE = 16
    RECORD_TYPE = 0  # Data record

    def __init__(self, byte_list, start_address=0):
        self.byte_list = byte_list
        self.start_address = start_address

    def __str__(self):
        return self.generate_intel_hex(self.start_address)

    def generate_intel_hex(self, start_address=0):
        hex_records = []
        address = start_address
        for i in range(0, len(self.byte_list), self.CHUNK_SIZE):
            chunk = self.byte_list[i:i+self.CHUNK_SIZE]
            record_length = len(chunk)
            record_address = address & 0xFFFF
            record = [record_length, (record_address >> 8) & 0xFF, record_address & 0xFF, self.RECORD_TYPE] + chunk
            checksum = (-sum(record)) &0xFF
            record.append(checksum)
            hex_record = ":" + "".join(f"{byte:02X}" for byte in record)
            hex_records.append(hex_record)
            address += record_length
        # End of file record
        eof_record = ":0000000000"
        hex_records.append(eof_record)

        return "\n".join(hex_records)


class Assembler:
    # todo -  consider adding functionality to evaluate complex expressions for argument field

    DIRECTIVES = {"ORG", "EQU", "DB", "DW", "DS", "END"}
    REGISTERS = {"A", "B", "C", "D", "E", "H", "L", "M","PSW"}


    def __init__(self, sourcefile,DEBUG):
        self.binary = bytearray(16384)  # 16K of memory space for assembly code
        self.labels = {}  # dict of label names from source file
        self.hexlist = []  # list of hex codes after assembly
        self.assembled = False  # flag to indicate successful assembly, can be checked before saving
        self.start_address = 0x0100  # start address for assembled code ( default 0x0100 0100H CPM TPA start)
        self.current_line = None  # current line for error reporting
        self.pass_mode = 0  # assembler pass through
        self.current_address = None  # current address during  assembly pass
        self.filename = sourcefile
        self.DEBUG = DEBUG

    def assemble(self):
        with open("".join([self.filename, ".asm"]), 'r') as file:
            source = file.readlines()
            print(source)
            try:
                self.pass_one(source)  # resolve labels and org
                print("Symbol Table")
                print(self.labels)
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
                label, command, arg = self.parse()
                if label is not None:  # resolve labels
                    if arg is None: # marker for address
                        self.labels[label] = self.current_address # 
                    else:
                        if command == "EQU": # set label to value of argument
                            self.labels[label] = self.get_val(arg)
                        else: # other commands on line so set label to current address
                            self.labels[label] = self.current_address # 
                else:  # parse commands and increment address
                    result_list = self._tokenize(command, arg)
                    if len(result_list) > 0:
                        self.current_address += len(result_list)  # update address

        

    def pass_two(self, file):
        print("Running Pass Two")
        self.pass_mode = 2
        self.current_address = self.start_address
        for line in file:
            self.current_line = self.clean(line)
            if self.current_line is not None:
                label, command, arg = self.parse()
                if command in INSTRUCTIONS or command in self.DIRECTIVES:  # only create tokens for recognised instructions
                    result_list = self._tokenize(command, arg)
                    if len(result_list) > 0:
                        self.current_address += len(result_list)  # update address
                        print("Current address {}".format(self.current_address))
                        for hexcode in result_list:
                            self.hexlist.append(hexcode)              
        self._convert_binary()

    def save(self):
        file = "".join([self.filename, ".bin"])
        with open(file, 'wb') as f:
            f.write(self.binary)
        print("{} binary "
              "file created!".format(file))
        file = "".join([self.filename, ".hex"])
        with open(file, 'w') as f:
            # TODO other INtel hex record detail
            f.write(":");
            f.write("1000");
            for h in self.hexlist:
                f.write("{:02X}".format(h))
            # TODO checksum
        print("{} Intel HEX "
              "file created!".format(file))

    def _convert_binary(self):
        location = 0
        print(self.hexlist)
        for h in self.hexlist:
            self.binary[location] = h
            location += 1

    def _tokenize(self, command, arg):
        """
        Lookup and return bytecode for the command, the command has already been validated
        and the address resolved, so simple routine to return the bytes
        :param command - the KEYWORD
        :param arg - the address value ( or None if not applicable)
        :returns: a list of byte values
        :raises ValueError: call function from within try..except block to catch syntax errors
        """
        bytelist = []
        if self.DEBUG:
            print("--------------  LINE   DEBUG    --------------------")
            print(self.current_line)
            print("Command: {} Arg: {}".format(command, arg))
        if command == "DB": # store data bytes
            result = self.store_data(arg)
            for c in result:
                bytelist.append(c)
        elif command in self.DIRECTIVES:
            # other directives
            # ignored for now   
            pass
        else:
            ins=INSTRUCTIONS.get(command)
            opcode=ins.get("Opcode")
            bytes=ins.get("Bytes")
            # need to know opcode so can just insert bytes for Pass 1
            # not all labels will be resolved until Pass 1 completed.
            # need to change instruction set so key is mnemonic and contains bytes and opcode
            if self.pass_mode == 1: # dummy insert for pass 1 padding- simply number of bytes
                for _ in range(bytes):
                    bytelist.append(0x00)
            else:
                bytelist.append(opcode) # append opcode
                if bytes == 2:     # append data byte
                    bytelist.append(self.get_val(arg, type="BYTE"))
                elif bytes == 3: # append data word
                    lsb, msb = self.get_val(arg, type="WORD")
                    bytelist.append(lsb)
                    bytelist.append(msb)
        return bytelist
    
    def get_val(self, arg, type=None):
        """
        Return either a byte value for type 'BYTE' or a word value with msb and lsb for type 'WORD'
        :param type: string 'BYTE' or 'WORD'
        :param arg: string  to evaluate
        :returns: a byte for type of 'BYTE' or a word for type 'WORD' along with lsb and msb
        """
        if arg in self.labels:
            arg=self.labels[arg]
        if isinstance(arg, str):
            if arg.startswith("'") and arg.endswith("'"): # expect only single character at this point
                arg=arg[1:-1]
                result = ord(arg)
            else:
                if arg.endswith("H") or arg.endswith("h"):
                    arg = arg[:-1]
                elif arg.startswith("$"):
                    arg = arg[1:]
                try:
                    result = int(arg, 16)  # convert hex to integer
                except ValueError as er:
                    print(f"Invalid numeric address {arg}")
        else:
            result = arg
        if type == "BYTE":
            if -1 < result < 0xFF:
                return result
            else:
                raise ValueError("Byte Value out of range")
        elif type == "WORD":
            if -1 < result < 0xFFFF:
                msb = int(result / 256)
                lsb = (result - (msb * 256))
                return lsb, msb
            else:
                raise ValueError("Word Value out of range")
        elif type == None: # just return the value
            return result
        else:
            raise ValueError("Invalid type")



    def store_data(self, arg):
        """
        Store data in memory
        :param arg: data to store
        :returns: list of byte values to store
        """
        data_list = self.get_words(arg, ",")
        result=[]
        for data in data_list:
            if data.startswith("'") and data.endswith("'"):
                data = data[1:-1]
                for s in data:
                    result.append(ord(s))
            else:
                result.append(self.get_val(data, type="BYTE"))
        return result
    
    def get_words(self,line,sep):
        """
        Return a list of words split by seperator character
        Ignore separators found within single quotes
        :param line: input string to split
        :sep: separator character
        :returns: list of words
        """
        words = []
        index=0
        string_on = False
        count = len(line)
        while index < count:
            if line[index] == "'":
                string_on = not string_on
            if line[index] == sep and string_on is False: # word break
                new_word = line[:index]
                if len(new_word) > 0:
                    words.append(line[:index])
                line = line[index+1:].strip() # trim the modified line again
                count = len(line) # update count after modifying line
                index=-1 # reset index to start again
            index+=1
        words.append(line) # add the last word
        return words

    def parse(self):
        """
        This will parse line input into a label, command and an argument
        returns:    
                    label - string
                    command - string
                    arg - string
        """
        'TOFIX - need to define my own parsing routine. Has to handle strings, hex and multiple data args comma seperated for DB, DW and DS'

        # words = self.current_line.split()
        #
        # pattern = r"(?:'[^']*'|\S)+"
        # words = re.findall(pattern, self.current_line)
        #
        #
        # assumptions
        # label must end with a colon
        # if words = 1 then could be a label or a single command
        # if words = 2 then could be a label with a command or a command with an argument
        # if words = 3 then must have a label, command and argument
        # words = shlex.split(self.current_line)
        words = self.get_words(self.current_line, " ")
        if self.DEBUG:
            print(f"List of tokens > {words}")
        arg = None
        if len(words) == 1:
            if words[0].endswith(':'):
                label = words[0][:-1]
                command = None
            else:
                label = None
                command = words[0]
        elif len(words) == 2:
            if words[0].endswith(':'):
                label = words[0][:-1]
                command = words[1]
            else:
                label = None
                command = words[0]
                arg = words[1]
        elif len(words) == 3:
            label = words[0][:-1]
            command = words[1]
            arg = words[2]
        else:
            raise ValueError("Syntax Error")
        # now use logic steps to work out the special cases for register commands
        # first one byte commands where registers are used as operations
        if arg is not None and command not in self.DIRECTIVES:
            operator = arg.split(",")
            if len(operator) == 2:
                if operator[0] and (operator[1] in self.REGISTERS): # argument is 2 registers
                    command = "".join([command," ", operator[0], ",", operator[1]] )
                    arg = None
                elif operator[0] in self.REGISTERS:  # argument is register and label/value
                    command = "".join([command," ", operator[0], ","])
                    arg = operator[1]
            else:
                # single register command
                if operator[0] in self.REGISTERS:
                    command = "".join([command," ", operator[0]])
                    arg =None
        return label, command, arg


    def clean(self, text):
        """
        Routine to clean up code line.
        First remove comments
        Replace tabs with spaces
        Strip newline
        Finally trim whitespace
        param: line - input text
        returns: clean text or None if line is empty or a comment
        """
        line = None
        if text is not None:
            if text[0] == ";":  # line is a comment so do nothing
                line = None
            else:
                line = text.split(";")[0]  # remove any inline comments - assume anything after ; is ignored
                line = line.replace("\t", " ")  # replace remaining tabs with spaces
                line = line.strip("\n").strip()  # finally strip newline and whitespace
        if self.DEBUG:
            print(f"Original source line > {repr(text)}")
            print(f"Cleaned line > {repr(line)}")
        return line


def main(sourcefile, DEBUG):
    asm = Assembler(sourcefile,DEBUG)
    asm.assemble()
    if asm.assembled:
        print(asm.labels)
        for h in asm.hexlist:
            print("{:02X}".format(h))
        # asm.save("code")
        hex_file = Hexfile(asm.hexlist, asm.start_address)
        print(hex_file)
        file = "".join([sourcefile, ".hex"])
        with open(file, 'w') as f:
            f.write(str(hex_file))
            

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sourcefile = sys.argv[1]
        DEBUG = True if len(sys.argv) > 2 and sys.argv[2].upper() == "-D" else False
        main(sourcefile, DEBUG)
    else:
        print("Usage: python asm.py <sourcefile>")
        fname = input("Source filename ? >")
        if os.path.exists("".join([fname, ".asm"])):
            DEBUG = True
            main(fname, DEBUG)
        else:
            print("File not found")
            sys.exit(0)
        