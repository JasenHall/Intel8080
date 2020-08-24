""""
Monitor for 8080 processor
"""
from cpu import CPU
import re


class Monitor:

    def __init__(self, cpu):
        self.cpu = cpu
        # set stack pointer
        self.cpu.SP = self.cpu.set_stackpointer(0xEE00)
        self.current_address = 0
        self.command = ""
        self.operand = ""
        self.buffer = []
        self.command_map = {
            "R": self.show_registers,
            "D": self.disasm,
            "A": self.set_address,
            "M": self.memory_dump,
            "I": self.insert_memory,
            "G": self.go,
            "S": self.step,
            "X": self.reset,
            "SAVE": self.save,
            "LOAD": self.load,
        }
    def help(self):
        print("Commands")
        print("--------")
        print("a hhhh  - set current address to hhhh where hhhh is hex value 0 to FFFF")
        print("d (hhhh lines) - disassemble lines from address hhhh")
        print("i (hhhh)  - edit hex values starting from address hhhh")
        print("g (addr) - start executing code from address hhhh")

    def disasm(self, addr = None):
        addr = self.current_address if addr is None else addr
        try:
            number = int(self.operand)
        except ValueError:
            number = 10
        for i in range(number):
            output = ""
            value = None
            opcode = self.cpu.memory[addr]
            baseaddr = addr
            addr += 1
            instruction = self.cpu.opcodes.get(opcode)
            bytes = instruction.get("Bytes")
            if bytes == 2:
                value = self.cpu.memory[addr]
                addr += 1
            elif bytes == 3:
                lb = self.cpu.memory[addr]
                addr += 1
                hb = self.cpu.memory[addr]
                value = self.cpu.get_word(hb, lb)
                addr += 1
            if value is not None:
                output += "${:04X}: {}".format(baseaddr, instruction.get("Instruction").format(value))
            else:
                output += "$" \
                          "{:04X}: {}".format(baseaddr, instruction.get("Instruction"))
            print(output)

    def memory_dump(self):
        """Returns a memory page for screen output
        param: address - will be a 1K page value from memory"""
        addr = self.validate_address()
        if addr >= 0:
            page = int(addr / 256)
            address = page * 256
            line = "       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F\n"
            line += "       -----------------------------------------------\n"
            for z in range(address, address + 256):
                data = self.cpu.memory[z]
                #  initial line for memory page
                if z == 0:  # first page
                    line += "${:04X}  ".format(z)
                    line += "{:02X} ".format(data)
                elif z % 256 == 0:  # any other page apart from first
                    line += "\n"
                    line += "${:04X}  ".format(z)
                    line += "{:02X} ".format(data)
                elif z % 16 == 0:  # if 16th data location then break a new line
                    line += "\n"
                    line += "${:04X}  ".format(z)
                    line += "{:02X} ".format(data)
                else:  # anything else just add the data to the current line
                    line += "{:02X} ".format(data)
            line += "\n"  # add the last line created dummy!!!
            print(line)

    def insert_memory(self):
        exit = False
        addr = self.validate_address()
        if addr >= 0:
            while not exit:
                value = input("{:04X}: {:02X} -".format(addr, self.cpu.memory[addr])).upper()
                if value == " ":
                    addr += 1
                elif value == "":
                    exit = True
                else:
                    try:
                        val = int(value, 16)
                        if val > 255:
                            raise ValueError("Value out of range")
                        self.cpu.memory[addr] = val
                        addr = addr + 1
                    except ValueError as e:
                        print(e)

    def show_registers(self):
        """ Show CPU registers"""
        output = "PC: ${:04X}\n".format(self.cpu.PC)
        output += "A: ${:02X}\n".format(self.cpu.A.value)
        output += "BC: ${:04X}\n".format(self.cpu.get_word(self.cpu.B.value, self.cpu.C.value))
        output += "DE: ${:04X}\n".format(self.cpu.get_word(self.cpu.D.value, self.cpu.E.value))
        output += "HL: ${:04X}\n".format(self.cpu.get_word(self.cpu.H.value, self.cpu.L.value))
        output += "SP: ${:04X}\n".format(self.cpu.get_word(self.cpu.S.value, self.cpu.P.value))
        print(output)

    def go(self):
        """Execute code"""
        if self.operand != "":
            self.set_pc()
        self.cpu.halt = False
        while self.cpu.halt is False:
            self.cpu.fetch_instruction()
            self.cpu.execute_instruction()
            self.check_out_buffer()

    def check_out_buffer(self):
        if len(self.cpu.output_buffer) > 0 and self.cpu.output_buffer[-1] == 0:
            self.cpu.output_buffer.pop()
            output = ""
            for c in self.cpu.output_buffer:
                output += chr(c)
            print(output)
            # clear buffer
            self.cpu.output_buffer = []


    def step(self):
        addr = self.cpu.PC
        self.cpu.fetch_instruction()
        self.operand =1
        self.disasm(addr)
        self.cpu.execute_instruction()
        print("OK")
        self.show_registers()
        self.check_out_buffer()

    def set_address(self):
        addr = self.validate_address()
        if addr >= 0:
            self.current_address = addr

    def set_pc(self):
        addr = self.validate_address()
        if addr >= 0:
            self.cpu.PC = addr

    def reset(self):
        self.cpu.PC = 0
        self.cpu.SP = 0

    def validate_address(self):
        if self.operand == "":
            return self.current_address
        try:
            addr = int(self.operand, 16)
            if addr > 0xFFFF:
                raise ValueError
            if addr >= 0:
                return addr
        except ValueError:
            print("Invalid address")
            return -1

    def parse(self, text):
        """Simple break down of commands for now"""
        self.command = self.operand = ""
        text = text.strip()  # strip leading and trailing spaces
        text = re.sub(" +", " ", text)  # substitute multiple whitespace for single space
        if text != "":
            text = text.split(" ")
            self.command = text[0].upper()
            if len(text) > 1:
                self.operand = text[1].upper()

    def load(self, filename="code"):
        # always use .bin extension
        filename = "".join([filename, ".bin"])
        with open(filename, 'rb') as f:
            self.cpu.memory[0x0000:] = f.read()  # load bin file starting at 0x0000

    def save(self, filename="code"):
        # always use .bin extension
        filename = "".join([filename, ".bin"])
        with open(filename, 'wb') as f:
            f.write(self.cpu.memory)

def main():
    cpu = CPU()
    mon = Monitor(cpu)
    ##########################
    # Main loop
    ##########################
    cmd = None
    while cmd != "EXIT":
        text = input("${:04X}: >".format(mon.current_address))
        mon.parse(text)
        if mon.command in mon.command_map:
            mon.command_map.get(mon.command)()


if __name__ == '__main__':
    main()
