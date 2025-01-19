#
from instructions import INSTRUCTION_SET

class Register:

    def __init__(self, name):
        self.name = name
        self.value = 0


class CPU:

    def __init__(self):
        self.memory = bytearray(0xFFFF)
        self.cycles = 0
        self.address_bus = 0  # 16 bit
        self.data_bus = 0  # 8 bit
        self.IR = None
        self.IR_disasm = None
        self.halt = False
        self.input_buffer = []
        self.output_buffer = []
        #################################
        #    registers                  #
        #################################
        self.A = Register("A")
        self.B = Register("B")
        self.C = Register("C")
        self.D = Register("D")
        self.E = Register("E")
        self.H = Register("F")
        self.L = Register("L")
        self.S = Register("S")
        self.P = Register("P")
        self.PC = 0  # program counter - 16 bit
        #################################
        #    condition flags            #
        #################################
        self.Zero = 0
        self.Sign = 0
        self.Parity = 0
        self.Carry = 0
        self.AuxCarry = 0
        self.opcodes = INSTRUCTION_SET
   
   
    @property
    def F(self):
        # Flag Register - SZ0A0P1C
        f = self.Sign << 7
        f |= self.Zero << 6
        f |= 0 << 5
        f |= self.AuxCarry << 4
        f |= 0 << 3
        f |= self.Parity << 2
        f |= 1 << 1
        f |= self.Carry
        return f

    ############################################
    #          helper functions                #
    ############################################

    def show_registers(self):
        output = "PC > {:04X}".format(self.PC)
        output += "  BC {:04X}".format(self.get_word(self.B.value, self.C.value))
        output += "  DE {:04X}".format(self.get_word(self.D.value, self.E.value))
        output += "  HL {:04X}".format(self.get_word(self.H.value, self.L.value))
        output += "  SP {:04X}".format(self.get_word(self.S.value, self.P.value))
        print(output)

    def fetch_instruction(self):
        # get next instruction
        self.address_bus = self.PC
        self.memory_read()
        self.IR = self.data_bus
        # not operational but information
        self.IR_disasm = self.opcodes.get(self.IR)
        self.PC = (self.PC + 1) & 0xFFFF

    def execute_instruction(self):
        opcode = self.IR
        self.opcodes.get(opcode).get("Method")()

    def fetch_byte(self):
        """
        Gets next byte from memory, increments PC and Cycles
        """
        self.address_bus = self.PC
        self.cycles += 1
        self.PC += 1
        self.data_bus = self.memory[self.address_bus]

    def memory_read(self):
        """
        Read byte from memory location
        Uses one cycle
        """
        self.cycles += 1
        self.data_bus = self.memory[self.address_bus]

    def memory_write(self):
        """
        Write byte to memory location
        Uses one cycle
        """
        self.cycles += 1
        self.memory[self.address_bus] = self.data_bus & 0xFF

    def get_word(self, msb, lsb):
        # returns 16 bit word from 2 bytes (MSB)(LSB)
        return (msb << 8) | lsb

    def get_direct_address(self):
        """
        address = ((byte3)(byte2))
        """
        self.fetch_byte()
        lsb = self.data_bus
        self.fetch_byte()
        msb = self.data_bus
        return self.get_word(msb, lsb)

    def pop_flags(self, psw):
        # set flags based on processor status word low byte
        # SZ0A0P1C
        self.Sign = (psw >> 7) & 0x01
        self.Zero = (psw >> 6) & 0x01
        self.AuxCarry = (psw >> 4) & 0x01
        self.Parity = (psw >> 2) & 0x01
        self.Carry = psw & 0x01

    def decode_rp(self):
        """
        Decode register pair
        :return: rh, rl
        """
        rp = (self.IR & 0x30) >> 4
        if rp == 0x00:
            return self.B, self.C
        elif rp == 0x01:
            return self.D, self.E
        elif rp == 0x02:
            return self.H, self.L
        elif rp == 0x03:
            return self.S, self.P

    def register_decode_dest(self):
        r = (self.IR & 0x38) >> 3
        if r == 0x00:
            return self.B
        elif r == 0x01:
            return self.C
        elif r == 0x02:
            return self.D
        elif r == 0x03:
            return self.E
        elif r == 0x04:
            return self.H
        elif r == 0x05:
            return self.L
        elif r == 0x07:
            return self.A

    def register_decode_source(self):
        r = self.IR & 0x07
        if r == 0x00:
            return self.B
        elif r == 0x01:
            return self.C
        elif r == 0x02:
            return self.D
        elif r == 0x03:
            return self.E
        elif r == 0x04:
            return self.H
        elif r == 0x05:
            return self.L
        elif r == 0x07:
            return self.A

    def set_flags_zsp(self, result):
        self.Zero = 1 if result == 0 else 0
        self.Sign = 1 if result & 0x80 else 0
        self.Parity = 1 if result % 2 == 0 else 0

    def update_arithmetic_result(self, result):
        self.Carry = 1 if result > 255 else 0
        self.set_flags_zsp(result)
        self.A.value = result & 0xFF

    def update_logical_result(self, result):
        self.Carry = 0
        self.set_flags_zsp(result)
        self.A.value = result & 0xFF

    def push_stack(self):
        """Push value on data bus to next stack location"""
        self.address_bus = (self.get_word(self.S.value, self.P.value) - 1) & 0xFFFF
        self.memory_write()
        self.set_stackpointer(self.address_bus)

    def pop_stack(self):
        """Pop value at top of stack to data bus"""
        self.address_bus = self.get_word(self.S.value, self.P.value)
        self.memory_read()
        self.set_stackpointer((self.address_bus + 1) & 0xFFFF)

    def set_stackpointer(self, sp):
        self.S.value = (sp >> 8) & 0xFF
        self.P.value = sp & 0xFF

    ##################################################
    # Data Transfer Instructions                     #
    ##################################################

    def mov(self):
        """
        Move register
        (r1) <- (r2)
        """
        self.register_decode_dest().value = self.register_decode_source().value

    def movrm(self):
        """
        Move from memory
        (r) <- ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        self.register_decode_dest().value = self.data_bus

    def movmr(self):
        """
        Move to memory
        ((H)(L)) <- (r)
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.data_bus = self.register_decode_source().value
        self.memory_write()

    def mvi(self):
        """
        Move immediate
        (r) <- (byte 2)
        """
        self.fetch_byte()
        self.register_decode_dest().value = self.data_bus

    def mvimd(self):
        """
        Move to memory immediate
        ((H)(L)) <- (byte 2)
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.fetch_byte()
        self.memory_write()

    def lxi(self):
        """
        Load  register pair immediate
        (rl) <- (byte2)
        (rh) <- (byte3)
        """
        rh, rl = self.decode_rp()
        self.fetch_byte()
        rl.value = self.data_bus
        self.fetch_byte()
        rh.value = self.data_bus

    def lda(self):
        """
        Load accumulator direct
        (A) <- ((byte3)(byte2))
        """
        self.address_bus = self.get_direct_address()
        self.memory_read()
        self.A.value = self.data_bus

    def sta(self):
        """
        Store accumulator direct
        ((byte3)(byte2)) <- (A)
        """
        self.address_bus = self.get_direct_address()
        self.data_bus = self.A.value
        self.memory_write()

    def lhld(self):
        """
        Load H and L direct
        (L) <- ((byte3)(byte2))
        (H) <- ((byte3)(byte2) + 1)
        """
        self.address_bus = self.get_direct_address()
        self.memory_read()
        self.H.value = self.data_bus
        self.address_bus += 1
        self.memory_read()
        self.L.value = self.data_bus

    def shld(self):
        """
        Store H and L direct
        ((byte3)(byte2)) <- (L)
        ((byte3)(byte2) + 1) <- (H)
        """
        self.address_bus = self.get_direct_address()
        self.data_bus = self.L.value
        self.memory_write()
        self.address_bus += 1
        self.data_bus = self.H.value
        self.memory_write()

    def ldax(self):
        """
        Load accumulator indirect
        (A) <- ((rp))
        """
        rh, rl = self.decode_rp()
        self.address_bus = self.get_word(rh.value, rl.value)
        self.memory_read()
        self.A.value = self.data_bus

    def stax(self):
        """
        Store accumulator indirect
        ((rp)) <- (A)
        """
        rh, rl = self.decode_rp()
        self.address_bus = self.get_word(rh.value, rl.value)
        self.data_bus = self.A.value
        self.memory_write()

    ###############################################################################
    # Arithmetic instructions                                                     #
    ###############################################################################

    def xchg(self):
        """
        Exchange H and L with D and E
        (H) <-> (D)
        (L) <-> (E)
        """
        tmp_h = self.H.value
        self.H.value = self.D.value
        self.D.value = tmp_h
        tmp_l = self.L.value
        self.L.value = self.E.value
        self.E.value = tmp_l

    def add(self):
        """
        Add register
        (A) <- (A) + r
        """
        result = self.A.value + self.register_decode_source().value
        self.update_arithmetic_result(result)

    def addm(self):
        """
        Add memory
        (A) <- (A) + ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value + self.data_bus
        self.update_arithmetic_result(result)

    def adi(self):
        """
        Add immediate
        (A) <- (A) + (byte2)
        """
        self.fetch_byte()
        result = self.A.value + self.data_bus
        self.update_arithmetic_result(result)

    def adc(self):
        """
        Add immediate
        (A) <- (A) + (r) + Carry
        """
        result = self.A.value + self.register_decode_source().value + self.Carry
        self.update_arithmetic_result(result)

    def adcm(self):
        """
        Add memory with carry
        (A) <- (A) + ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value + self.data_bus + self.Carry
        self.update_arithmetic_result(result)

    def aci(self):
        """
        Add immediate with carry
        (A) <- (A) + (byte2) + carry
        """
        self.fetch_byte()
        result = self.A.value + self.data_bus + self.Carry
        self.update_arithmetic_result(result)

    def sub(self):
        """
        Subtract register
        (A) <- (A) - (r)
        """
        result = self.A.value - self.register_decode_source().value
        self.update_arithmetic_result(result)

    def subm(self):
        """
        Subtract memory
        (A) <- (A) -((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value - self.data_bus
        self.update_arithmetic_result(result)

    def sui(self):
        """
        Subtract immediate
        (A) <- (A) - (byte2)
        """
        self.fetch_byte()
        result = self.A.value - self.data_bus
        self.update_arithmetic_result(result)

    def sbb(self):
        """
        Subtract register with borrow
        (A) <- (A) - (r) - carry
        """
        result = self.A.value - self.register_decode_source().value - self.Carry
        self.update_arithmetic_result(result)

    def sbbm(self):
        """
        Subtract memory with borrow
        (A) <- (A) -((H)(L)) - carry
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value - self.data_bus - self.Carry
        self.update_arithmetic_result(result)

    def sbi(self):
        """
        Subtract immediate with borrow
        (A) <- (A) - (byte2) - carry
        """
        self.fetch_byte()
        result = self.A.value - self.data_bus - self.Carry
        self.update_arithmetic_result(result)

    def inr(self):
        """
        Increment register
        (r) <- (r) +1
        """
        result = self.register_decode_dest().value + 1
        self.register_decode_dest().value = result
        self.set_flags_zsp(result)

    def inrm(self):
        """
        Increment memory
        ((H)(L)) <- ((H)(L)) +1
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        self.data_bus += 1
        self.memory_write()
        self.set_flags_zsp(self.data_bus)

    def dcr(self):
        """
        Decrement register
        (r) <- (r) -1
        """
        result = self.register_decode_dest().value - 1
        self.register_decode_dest().value = result
        self.set_flags_zsp(result)

    def dcrm(self):
        """
        Decrement memory
        ((H)(L)) <- ((H)(L)) -1
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        self.data_bus -= 1
        self.memory_write()
        self.set_flags_zsp(self.data_bus)

    def inx(self):
        """
        Increment register pair
        (rh)(rl) <- (rh)(rl)+1
        """
        rh, rl = self.decode_rp()
        inc = (self.get_word(rh.value, rl.value) + 1) & 0xFFFF
        rh.value = inc >> 8
        rl.value = inc & 0xFF

    def dcx(self):
        """
        Decrement register pair
        (rh)(rl) <- (rh)(rl) -1
        """
        rh, rl = self.decode_rp()
        dec = (self.get_word(rh.value, rl.value) - 1) & 0xFFFF
        rh.value = dec >> 8
        rl.value = dec & 0xFF

    def dad(self):
        # Add rp to HL  - (H)(L) <- (H)(L)+(rh)(rl)
        rh, rl = self.decode_rp()
        result = self.get_word(rh.value, rl.value) + self.get_word(self.H.value, self.L.value)
        if result > 0xFFFF:
            self.Carry = 1
        self.H.value = (result >> 8) & 0xFF
        self.L.value = result & 0xFF
        self.cycles += 2

    def daa(self):
        """
        Decimal adjust accumulator
        """
        # todo - not implemented
        pass

    ##################################################################
    #  Logical Instruction Group
    ##################################################################

    def ana(self):
        """
        AND register
        (A) <- (A) & r
        """
        result = self.A.value & self.register_decode_source().value
        self.update_logical_result(result)

    def anam(self):
        """
        AND memory
        (A) <- (A) & ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value & self.data_bus
        self.update_logical_result(result)

    def ani(self):
        """
        AND immediate
        (A) <- (A) & (byte2)
        """
        self.fetch_byte()
        result = self.A.value & self.data_bus
        self.update_logical_result(result)

    def xra(self):
        """
        XOR register
        (A) <- (A) ^ r
        """
        result = self.A.value ^ self.register_decode_source().value
        self.update_logical_result(result)

    def xram(self):
        """
        XOR memory
        (A) <- (A) ^ ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value ^ self.data_bus
        self.update_logical_result(result)

    def xri(self):
        """
        XOR immediate
        (A) <- (A) ^ (byte2)
        """
        self.fetch_byte()
        result = self.A.value ^ self.data_bus
        self.update_logical_result(result)

    def ora(self):
        """
        OR register
        (A) <- (A) | r
        """
        result = self.A.value | self.register_decode_source().value
        self.update_logical_result(result)

    def oram(self):
        """
        OR memory
        (A) <- (A) | ((H)(L))
        :return:
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value | self.data_bus
        self.update_logical_result(result)

    def ori(self):
        """
        OR immediate
        (A) <- (A) | (byte2)
        """
        self.fetch_byte()
        result = self.A.value | self.data_bus
        self.update_logical_result(result)

    def cmp(self):
        """
        Compare register
        (A) - r
        """
        result = self.A.value - self.register_decode_source().value
        self.Carry = 1 if self.A.value < self.register_decode_source().value else 0
        self.set_flags_zsp(result)

    def cmpm(self):
        """
        Compare memory
        (A) - ((H)(L))
        """
        self.address_bus = self.get_word(self.H.value, self.L.value)
        self.memory_read()
        result = self.A.value - self.data_bus
        self.Carry = 1 if self.A.value < self.data_bus else 0
        self.set_flags_zsp(result)

    def cpi(self):
        """
        Compare immediate
        (A) - (byte2)
        """
        self.fetch_byte()
        result = self.A.value - self.data_bus
        self.Carry = 1 if self.A.value < self.data_bus else 0
        self.set_flags_zsp(result)

    def rlc(self):
        # Rotate left   (A) <- (A)
        highbit = (self.A.value & 0x80) >> 7
        self.A.value = (self.A.value << 1) & 0xFF
        self.A.value |= highbit  # highbit transferred to low bit
        self.Carry = highbit

    def rrc(self):
        # Rotate right   (A) <- (A)
        lowbit = self.A.value & 0x01
        self.A.value = (self.A.value >> 1) & 0xFF
        self.A.value |= (lowbit << 7)  # lowbit transferred to highbit
        self.Carry = lowbit

    def ral(self):
        # Rotate left through carry  (A) <- (A)
        highbit = (self.A.value & 0x80) >> 7
        self.A.value = (self.A.value << 1) & 0xFF
        self.A.value |= self.Carry  # Carry transferred to low bit
        self.Carry = highbit  # highbit transferred to Carry

    def rar(self):
        # Rotate right through carry   (A) <- (A)
        lowbit = self.A.value & 0x01
        self.A.value = (self.A.value >> 1) & 0xFF
        self.A.value |= (self.Carry << 7)  # Carry transferred to highbit
        self.Carry = lowbit  # lowbit transferred to Carry

    def cma(self):
        # Complement accumulator (bitwise negate) (A) <- ~(A)
        self.A.value = self.A.value ^ 0xFF

    def cmc(self):
        # Complement carry - (negate Carry flag) (Cy) <- ~(Cy)
        self.Carry = self.Carry ^ 0x01

    def stc(self):
        # Set Carry  - (Cy) <- 1
        self.Carry = 1

    ##########################################################################
    # Branch Instructions
    ##########################################################################

    def jmp(self):
        # Jump   (PC) <- (Byte3)(Byte2)
        self.PC = self.get_direct_address()

    def jnz(self):
        # Jump not zero (PC) <- (Byte3)(Byte2)
        if self.Zero == 0:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jz(self):
        # Jump zero (PC) <- (Byte3)(Byte2)
        if self.Zero == 1:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jnc(self):
        # Jump no carry (PC) <- (Byte3)(Byte2)
        if self.Carry == 0:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jc(self):
        # Jump carry (PC) <- (Byte3)(Byte2)
        if self.Carry == 1:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jpo(self):
        # Jump parity odd (PC) <- (Byte3)(Byte2)
        if self.Parity == 0:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jpe(self):
        # Jump parity even (PC) <- (Byte3)(Byte2)
        if self.Parity == 1:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jp(self):
        # Jump plus (PC) <- (Byte3)(Byte2)
        if self.Sign == 0:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def jm(self):
        # Jump plus (PC) <- (Byte3)(Byte2)
        if self.Sign == 1:
            self.PC = self.get_direct_address()
        else:
            self.PC += 2

    def call(self):
        # Call ((SP)-1) <- (PCH), ((SP)-2) <- (PCL), (SP) < SP - 2, (PC) <- (Byte3)(Byte2)
        self.data_bus = self.PC >> 8  # PC high byte
        self.push_stack()
        self.data_bus = self.PC & 0xFF  # PC low byte
        self.push_stack()
        self.PC = self.get_direct_address()

    def cnz(self):
        # call not zero
        if self.Zero == 0:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cz(self):
        # Call not zero (PC) <- (Byte3)(Byte2)
        if self.Zero == 1:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cnc(self):
        # Call no carry (PC) <- (Byte3)(Byte2)
        if self.Carry == 0:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cc(self):
        # Call carry (PC) <- (Byte3)(Byte2)
        if self.Carry == 1:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cpo(self):
        # Call parity odd (PC) <- (Byte3)(Byte2)
        if self.Parity == 0:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cpe(self):
        # Call parity even (PC) <- (Byte3)(Byte2)
        if self.Parity == 1:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cp(self):
        # Call plus (PC) <- (Byte3)(Byte2)
        if self.Sign == 0:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def cm(self):
        # Call  plus (PC) <- (Byte3)(Byte2)
        if self.Sign == 1:
            self.call()
        else:
            # Add 2 cycles as conditional call uses 3 cycles if condition not met
            self.cycles += 2

    def ret(self):
        # Return  (PCH) <- ((SP)), (PCL) <- ((SP+1)), (SP) <- (SP) + 2
        self.pop_stack()
        msb = self.data_bus
        self.pop_stack()
        lsb = self.data_bus
        self.PC = self.get_word(msb, lsb)

    def rnz(self):
        # return not zero
        if self.Zero == 0:
            self.ret()

    def rz(self):
        # Return not zero
        if self.Zero == 1:
            self.ret()

    def rnc(self):
        # Return no carry
        if self.Carry == 0:
            self.ret()

    def rc(self):
        # Return carry
        if self.Carry == 1:
            self.ret()

    def rpo(self):
        # Return parity odd
        if self.Parity == 0:
            self.ret()

    def rpe(self):
        # Return parity even
        if self.Parity == 1:
            self.ret()

    def rp(self):
        # Return plus
        if self.Sign == 0:
            self.ret()

    def rm(self):
        # Return  plus
        if self.Sign == 1:
            self.ret()

    def rst(self):
        # Reset nnn ((SP)-1) <- (PCH), ((SP)-2) <- (PCL), (SP) < SP - 2, (PC) <- nnn*8
        self.data_bus = self.PC >> 8  # PC high byte
        self.push_stack()
        self.data_bus = self.PC & 0xFF  # PC low byte
        self.push_stack()
        nnn = (self.IR >> 3) & 0x07  # 3 bit number from instruction
        self.PC = self.get_word(0, nnn << 3)

    ####################################################################################
    # Stack Instructions
    ####################################################################################

    def pchl(self):
        # jump to (H)(L)
        self.PC = self.get_word(self.H.value, self.L.value)

    def push(self):
        # Push register pair  ((SP) -1 ) <- (rh), ((SP) -2) <- (rl), (SP) <- (SP) -2
        rh, rl = self.decode_rp()
        self.data_bus = rh.value
        self.push_stack()
        self.data_bus = rl.value
        self.push_stack()

    def pushpsw(self):
        # Push Status word ((SP)-1) <- (A), ((SP)-2) <- (F)
        self.data_bus = self.A.value
        self.push_stack()
        self.data_bus = self.F
        self.push_stack()

    def pop(self):
        # Pop register pair (rh) <- (SP), (rl) <- ((SP) +1),  (SP) <- (SP) +2
        rh, rl = self.decode_rp()
        self.pop_stack()
        rl.value = self.data_bus
        self.pop_stack()
        rh.value = self.data_bus

    def poppsw(self):
        # Pop Status Word (F) <- (SP), (A) <- ((SP) +1),  (SP) <- (SP) +2
        self.pop_stack()
        self.pop_flags(self.data_bus)  # set all the Flags according to the data byte
        self.pop_stack()
        self.A.value = self.data_bus

    def xthl(self):
        # Exchange Stack with HL  (L) <-> ((SP), (H) <-> ((SP) +1)
        sp = self.get_word(self.S.value, self.P.value)
        tmpl = self.L.value
        self.address_bus = sp
        self.memory_read()
        self.L.value = self.data_bus
        self.data_bus = tmpl
        self.memory_write()
        tmph = self.H.value
        self.address_bus = sp + 1
        self.memory_read()
        self.H.value = self.data_bus
        self.data_bus = tmph
        self.memory_write()

    def sphl(self):
        # move HL to SP  (SP) <- (H)(L)
        self.set_stackpointer(self.get_word(self.H.value, self.L.value))

    def in_port(self):
        """Input (A) <- (data)"""
        self.fetch_byte()
        if self.data_bus == 1: # pseudo keyboard input port
            # cheat and read the buffer direct rather than pass through data bus
            if len(self.input_buffer) > 0:
                self.A.value = self.input_buffer.pop(0)  # pop next item
        self.cycles += 2

    def out_port(self):
        """Output (data) <- (A)"""
        self.fetch_byte()
        if self.data_bus == 2: # pseudo terminal output port
            self.output_buffer.append(self.A.value)
        self.cycles += 2

    def ei(self):
        """Enable interrupts"""
        # todo implement interrupts
        pass

    def di(self):
        """Disable interrupts"""
        # todo implement interrupts
        pass

    def hlt(self):
        """Halt processor"""
        self.halt = True

    def nop(self):
        """Do nothing - nop instruction"""

