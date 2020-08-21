
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
        self.opcodes = {
            0x00: {"Instruction": "NOP", "Bytes": 1, "Method": self.nop},
            0x01: {"Instruction": "LXI B,{:04X}", "Bytes": 3, "Method": self.lxi},
            0x03: {"Instruction": "STAX B", "Bytes": 1, "Method": self.stax},
            0x04: {"Instruction": "INX B", "Bytes": 1, "Method": self.inx},
            0x05: {"Instruction": "INR B", "Bytes": 1, "Method": self.dcr},
            0x06: {"Instruction": "MVI B,{:02X}", "Bytes": 2, "Method": self.lxi},
            0x07: {"Instruction": "RLC", "Bytes": 1, "Method": self.rlc},
            0x08: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x09: {"Instruction": "DAD B", "Bytes": 1, "Method": self.dad},
            0x0A: {"Instruction": "LDAX B", "Bytes": 3, "Method": self.ldax},
            0x0B: {"Instruction": "DCX B", "Bytes": 1, "Method": self.dcx},
            0x0C: {"Instruction": "INR C", "Bytes": 1, "Method": self.inr},
            0x0D: {"Instruction": "DCR C", "Bytes": 1, "Method": self.dcr},
            0x0E: {"Instruction": "MVI C,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x0F: {"Instruction": "RRC", "Bytes": 1, "Method": self.rrc},

            0x10: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x11: {"Instruction": "LXI D,{:04X}", "Bytes": 3, "Method": self.lxi},
            0x12: {"Instruction": "STAX D", "Bytes": 1, "Method": self.stax},
            0x13: {"Instruction": "INX D", "Bytes": 1, "Method": self.inx},
            0x14: {"Instruction": "INR D", "Bytes": 1, "Method": self.inr},
            0x15: {"Instruction": "DCR D", "Bytes": 1, "Method": self.dcr},
            0x16: {"Instruction": "MVI D,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x17: {"Instruction": "RAL", "Bytes": 1, "Method": self.ral},
            0x18: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x19: {"Instruction": "DAD D", "Bytes": 1, "Method": self.dad},
            0x1A: {"Instruction": "LDAX D", "Bytes": 1, "Method": self.ldax},
            0x1B: {"Instruction": "DCX D", "Bytes": 1, "Method": self.dcx},
            0x1C: {"Instruction": "INR E", "Bytes": 1, "Method": self.inr},
            0x1D: {"Instruction": "DCR E", "Bytes": 1, "Method": self.dcr},
            0x1E: {"Instruction": "MVI E,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x1F: {"Instruction": "RAR", "Bytes": 1, "Method": self.rar},

            0x20: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x21: {"Instruction": "LXI H,{:04X}", "Bytes": 3, "Method": self.lxi},
            0x22: {"Instruction": "SHLD {:04X}", "Bytes": 3, "Method": self.shld},
            0x23: {"Instruction": "INX H", "Bytes": 1, "Method": self.inx},
            0x24: {"Instruction": "INR H", "Bytes": 1, "Method": self.inr},
            0x25: {"Instruction": "DCR H", "Bytes": 1, "Method": self.dcr},
            0x26: {"Instruction": "MVI H,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x27: {"Instruction": "DAA", "Bytes": 1, "Method": self.daa},
            0x28: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x29: {"Instruction": "DAD H", "Bytes": 1, "Method": self.dad},
            0x2A: {"Instruction": "LHLD {:04x}", "Bytes": 3, "Method": self.lhld},
            0x2B: {"Instruction": "DCX H", "Bytes": 1, "Method": self.dcx},
            0x2C: {"Instruction": "INR L", "Bytes": 1, "Method": self.inr},
            0x2D: {"Instruction": "DCR L", "Bytes": 1, "Method": self.dcr},
            0x2E: {"Instruction": "MVI L,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x2F: {"Instruction": "CMA", "Bytes": 1, "Method": self.cma},

            0x30: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x31: {"Instruction": "LXI SP,{:04X}", "Bytes": 3, "Method": self.lxi},
            0x32: {"Instruction": "STA {:04X}", "Bytes": 3, "Method": self.sta},
            0x33: {"Instruction": "INX SP", "Bytes": 1, "Method": self.inx},
            0x34: {"Instruction": "INR M", "Bytes": 1, "Method": self.inr},
            0x35: {"Instruction": "DCR M", "Bytes": 1, "Method": self.dcr},
            0x36: {"Instruction": "MVI M,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x37: {"Instruction": "STC", "Bytes": 1, "Method": self.stc},
            0x38: {"Instruction": "*NOP", "Bytes": 1, "Method": self.nop},
            0x39: {"Instruction": "DAD SP", "Bytes": 1, "Method": self.dad},
            0x3A: {"Instruction": "LDA {:04x}", "Bytes": 3, "Method": self.lda},
            0x3B: {"Instruction": "DCX SP", "Bytes": 1, "Method": self.dcx},
            0x3C: {"Instruction": "INR A", "Bytes": 1, "Method": self.inr},
            0x3D: {"Instruction": "DCR A", "Bytes": 1, "Method": self.dcr},
            0x3E: {"Instruction": "MVI A,{:02X}", "Bytes": 2, "Method": self.mvi},
            0x3F: {"Instruction": "CMC", "Bytes": 1, "Method": self.cmc},

            0x40: {"Instruction": "MOV B,B", "Bytes": 1, "Method": self.mov},
            0x41: {"Instruction": "MOV B,C", "Bytes": 1, "Method": self.mov},
            0x42: {"Instruction": "MOV B,D", "Bytes": 1, "Method": self.mov},
            0x43: {"Instruction": "MOV B,E", "Bytes": 1, "Method": self.mov},
            0x44: {"Instruction": "MOV B,H", "Bytes": 1, "Method": self.mov},
            0x45: {"Instruction": "MOV B,L", "Bytes": 1, "Method": self.mov},
            0x46: {"Instruction": "MOV B,M", "Bytes": 1, "Method": self.movrm},
            0x47: {"Instruction": "MOV B,A", "Bytes": 1, "Method": self.mov},
            0x48: {"Instruction": "MOV C,B", "Bytes": 1, "Method": self.mov},
            0x49: {"Instruction": "MOV C,C", "Bytes": 1, "Method": self.mov},
            0x4A: {"Instruction": "MOV C,D", "Bytes": 1, "Method": self.mov},
            0x4B: {"Instruction": "MOV C,E", "Bytes": 1, "Method": self.mov},
            0x4C: {"Instruction": "MOV C,H", "Bytes": 1, "Method": self.mov},
            0x4D: {"Instruction": "MOV C,L", "Bytes": 1, "Method": self.mov},
            0x4E: {"Instruction": "MOV C,M", "Bytes": 1, "Method": self.movrm},
            0x4F: {"Instruction": "MOV C,A", "Bytes": 1, "Method": self.mov},

            0x50: {"Instruction": "MOV D,B", "Bytes": 1, "Method": self.mov},
            0x51: {"Instruction": "MOV D,C", "Bytes": 1, "Method": self.mov},
            0x52: {"Instruction": "MOV D,D", "Bytes": 1, "Method": self.mov},
            0x53: {"Instruction": "MOV D,E", "Bytes": 1, "Method": self.mov},
            0x54: {"Instruction": "MOV D,H", "Bytes": 1, "Method": self.mov},
            0x55: {"Instruction": "MOV D,L", "Bytes": 1, "Method": self.mov},
            0x56: {"Instruction": "MOV D,M", "Bytes": 1, "Method": self.movrm},
            0x57: {"Instruction": "MOV D,A", "Bytes": 1, "Method": self.mov},
            0x58: {"Instruction": "MOV E,B", "Bytes": 1, "Method": self.mov},
            0x59: {"Instruction": "MOV E,C", "Bytes": 1, "Method": self.mov},
            0x5A: {"Instruction": "MOV E,D", "Bytes": 1, "Method": self.mov},
            0x5B: {"Instruction": "MOV E,E", "Bytes": 1, "Method": self.mov},
            0x5C: {"Instruction": "MOV E,H", "Bytes": 1, "Method": self.mov},
            0x5D: {"Instruction": "MOV E,L", "Bytes": 1, "Method": self.mov},
            0x5E: {"Instruction": "MOV E,M", "Bytes": 1, "Method": self.movrm},
            0x5F: {"Instruction": "MOV E,A", "Bytes": 1, "Method": self.mov},

            0x60: {"Instruction": "MOV H,B", "Bytes": 1, "Method": self.mov},
            0x61: {"Instruction": "MOV H,C", "Bytes": 1, "Method": self.mov},
            0x62: {"Instruction": "MOV H,D", "Bytes": 1, "Method": self.mov},
            0x63: {"Instruction": "MOV H,E", "Bytes": 1, "Method": self.mov},
            0x64: {"Instruction": "MOV H,H", "Bytes": 1, "Method": self.mov},
            0x65: {"Instruction": "MOV H,L", "Bytes": 1, "Method": self.mov},
            0x66: {"Instruction": "MOV H,M", "Bytes": 1, "Method": self.movrm},
            0x67: {"Instruction": "MOV H,A", "Bytes": 1, "Method": self.mov},
            0x68: {"Instruction": "MOV L,B", "Bytes": 1, "Method": self.mov},
            0x69: {"Instruction": "MOV L,C", "Bytes": 1, "Method": self.mov},
            0x6A: {"Instruction": "MOV L,D", "Bytes": 1, "Method": self.mov},
            0x6B: {"Instruction": "MOV L,E", "Bytes": 1, "Method": self.mov},
            0x6C: {"Instruction": "MOV L,H", "Bytes": 1, "Method": self.mov},
            0x6D: {"Instruction": "MOV L,L", "Bytes": 1, "Method": self.mov},
            0x6E: {"Instruction": "MOV L,M", "Bytes": 1, "Method": self.movrm},
            0x6F: {"Instruction": "MOV L,A", "Bytes": 1, "Method": self.mov},

            0x70: {"Instruction": "MOV M,B", "Bytes": 1, "Method": self.movmr},
            0x71: {"Instruction": "MOV M,C", "Bytes": 1, "Method": self.movmr},
            0x72: {"Instruction": "MOV M,D", "Bytes": 1, "Method": self.movmr},
            0x73: {"Instruction": "MOV M,E", "Bytes": 1, "Method": self.movmr},
            0x74: {"Instruction": "MOV M,H", "Bytes": 1, "Method": self.movmr},
            0x75: {"Instruction": "MOV M,L", "Bytes": 1, "Method": self.movmr},
            0x76: {"Instruction": "HLT", "Bytes": 1, "Method": self.hlt},
            0x77: {"Instruction": "MOV M,A", "Bytes": 1, "Method": self.movmr},
            0x78: {"Instruction": "MOV A,B", "Bytes": 1, "Method": self.mov},
            0x79: {"Instruction": "MOV A,C", "Bytes": 1, "Method": self.mov},
            0x7A: {"Instruction": "MOV A,D", "Bytes": 1, "Method": self.mov},
            0x7B: {"Instruction": "MOV A,E", "Bytes": 1, "Method": self.mov},
            0x7C: {"Instruction": "MOV A,H", "Bytes": 1, "Method": self.mov},
            0x7D: {"Instruction": "MOV A,L", "Bytes": 1, "Method": self.mov},
            0x7E: {"Instruction": "MOV A,M", "Bytes": 1, "Method": self.movrm},
            0x7F: {"Instruction": "MOV A,A", "Bytes": 1, "Method": self.mov},

            0x80: {"Instruction": "ADD B", "Bytes": 1, "Method": self.add},
            0x81: {"Instruction": "ADD C", "Bytes": 1, "Method": self.add},
            0x82: {"Instruction": "ADD D", "Bytes": 1, "Method": self.add},
            0x83: {"Instruction": "ADD E", "Bytes": 1, "Method": self.add},
            0x84: {"Instruction": "ADD H", "Bytes": 1, "Method": self.add},
            0x85: {"Instruction": "ADD L", "Bytes": 1, "Method": self.add},
            0x86: {"Instruction": "ADD M", "Bytes": 1, "Method": self.addm},
            0x87: {"Instruction": "ADD A", "Bytes": 1, "Method": self.add},
            0x88: {"Instruction": "ADC B", "Bytes": 1, "Method": self.adc},
            0x89: {"Instruction": "ADC C", "Bytes": 1, "Method": self.adc},
            0x8A: {"Instruction": "ADC D", "Bytes": 1, "Method": self.adc},
            0x8B: {"Instruction": "ADC E", "Bytes": 1, "Method": self.adc},
            0x8C: {"Instruction": "ADC H", "Bytes": 1, "Method": self.adc},
            0x8D: {"Instruction": "ADC L", "Bytes": 1, "Method": self.adc},
            0x8E: {"Instruction": "ADC M", "Bytes": 1, "Method": self.adcm},
            0x8F: {"Instruction": "ADC A", "Bytes": 1, "Method": self.adc},

            0x90: {"Instruction": "SUB B", "Bytes": 1, "Method": self.sub},
            0x91: {"Instruction": "SUB C", "Bytes": 1, "Method": self.sub},
            0x92: {"Instruction": "SUB D", "Bytes": 1, "Method": self.sub},
            0x93: {"Instruction": "SUB E", "Bytes": 1, "Method": self.sub},
            0x94: {"Instruction": "SUB H", "Bytes": 1, "Method": self.sub},
            0x95: {"Instruction": "SUB L", "Bytes": 1, "Method": self.sub},
            0x96: {"Instruction": "SUB M", "Bytes": 1, "Method": self.subm},
            0x97: {"Instruction": "SUB A", "Bytes": 1, "Method": self.sub},
            0x98: {"Instruction": "SBB B", "Bytes": 1, "Method": self.sbb},
            0x99: {"Instruction": "SBB C", "Bytes": 1, "Method": self.sbb},
            0x9A: {"Instruction": "SBB D", "Bytes": 1, "Method": self.sbb},
            0x9B: {"Instruction": "SBB E", "Bytes": 1, "Method": self.sbb},
            0x9C: {"Instruction": "SBB H", "Bytes": 1, "Method": self.sbb},
            0x9D: {"Instruction": "SBB L", "Bytes": 1, "Method": self.sbb},
            0x9E: {"Instruction": "SBB M", "Bytes": 1, "Method": self.sbbm},
            0x9F: {"Instruction": "SBB A", "Bytes": 1, "Method": self.sbb},

            0xA0: {"Instruction": "ANA B", "Bytes": 1, "Method": self.ana},
            0xA1: {"Instruction": "ANA C", "Bytes": 1, "Method": self.ana},
            0xA2: {"Instruction": "ANA D", "Bytes": 1, "Method": self.ana},
            0xA3: {"Instruction": "ANA E", "Bytes": 1, "Method": self.ana},
            0xA4: {"Instruction": "ANA H", "Bytes": 1, "Method": self.ana},
            0xA5: {"Instruction": "ANA L", "Bytes": 1, "Method": self.ana},
            0xA6: {"Instruction": "ANA M", "Bytes": 1, "Method": self.anam},
            0xA7: {"Instruction": "ANA A", "Bytes": 1, "Method": self.ana},
            0xA8: {"Instruction": "SBB B", "Bytes": 1, "Method": self.sbb},
            0xA9: {"Instruction": "SBB C", "Bytes": 1, "Method": self.sbb},
            0xAA: {"Instruction": "SBB D", "Bytes": 1, "Method": self.sbb},
            0xAB: {"Instruction": "SBB E", "Bytes": 1, "Method": self.sbb},
            0xAC: {"Instruction": "SBB H", "Bytes": 1, "Method": self.sbb},
            0xAD: {"Instruction": "SBB L", "Bytes": 1, "Method": self.sbb},
            0xAE: {"Instruction": "SBB M", "Bytes": 1, "Method": self.sbbm},
            0xAF: {"Instruction": "SBB A", "Bytes": 1, "Method": self.sbb},

            0xB0: {"Instruction": "ORA B", "Bytes": 1, "Method": self.ora},
            0xB1: {"Instruction": "ORA C", "Bytes": 1, "Method": self.ora},
            0xB2: {"Instruction": "ORA D", "Bytes": 1, "Method": self.ora},
            0xB3: {"Instruction": "ORA E", "Bytes": 1, "Method": self.ora},
            0xB4: {"Instruction": "ORA H", "Bytes": 1, "Method": self.ora},
            0xB5: {"Instruction": "ORA L", "Bytes": 1, "Method": self.ora},
            0xB6: {"Instruction": "ORA M", "Bytes": 1, "Method": self.oram},
            0xB7: {"Instruction": "ORA A", "Bytes": 1, "Method": self.ora},
            0xB8: {"Instruction": "CMP B", "Bytes": 1, "Method": self.cmp},
            0xB9: {"Instruction": "CMP C", "Bytes": 1, "Method": self.cmp},
            0xBA: {"Instruction": "CMP D", "Bytes": 1, "Method": self.cmp},
            0xBB: {"Instruction": "CMP E", "Bytes": 1, "Method": self.cmp},
            0xBC: {"Instruction": "CMP H", "Bytes": 1, "Method": self.cmp},
            0xBD: {"Instruction": "CMP L", "Bytes": 1, "Method": self.cmp},
            0xBE: {"Instruction": "CMP M", "Bytes": 1, "Method": self.cmpm},
            0xBF: {"Instruction": "CMP A", "Bytes": 1, "Method": self.cmp},

            0xC0: {"Instruction": "RNZ", "Bytes": 1, "Method": self.rnz},
            0xC1: {"Instruction": "POP B", "Bytes": 1, "Method": self.pop},
            0xC2: {"Instruction": "JNZ {:04X}", "Bytes": 3, "Method": self.jnz},
            0xC3: {"Instruction": "JMP {:04X}", "Bytes": 3, "Method": self.jmp},
            0xC4: {"Instruction": "CNZ {:04X}", "Bytes": 3, "Method": self.cnz},
            0xC5: {"Instruction": "PUSH B", "Bytes": 1, "Method": self.push},
            0xC6: {"Instruction": "ADI {:02X}", "Bytes": 2, "Method": self.oram},
            0xC7: {"Instruction": "RST 0", "Bytes": 1, "Method": self.rst},
            0xC8: {"Instruction": "RZ", "Bytes": 1, "Method": self.rz},
            0xC9: {"Instruction": "RET", "Bytes": 1, "Method": self.ret},
            0xCA: {"Instruction": "JZ {:04X}", "Bytes": 3, "Method": self.jz},
            0xCB: {"Instruction": "*JMP {:04X}", "Bytes": 3, "Method": self.jmp},
            0xCC: {"Instruction": "CZ {:04X}", "Bytes": 3, "Method": self.cz},
            0xCD: {"Instruction": "CALL {:04X}", "Bytes": 3, "Method": self.call},
            0xCE: {"Instruction": "ACI {:02X}", "Bytes": 2, "Method": self.aci},
            0xCF: {"Instruction": "RST 1", "Bytes": 1, "Method": self.rst},

            0xD0: {"Instruction": "RNC", "Bytes": 1, "Method": self.rnc},
            0xD1: {"Instruction": "POP D", "Bytes": 1, "Method": self.pop},
            0xD2: {"Instruction": "JNC {:04X}", "Bytes": 3, "Method": self.jnc},
            0xD3: {"Instruction": "OUT {:02X}", "Bytes": 2, "Method": self.out_port},
            0xD4: {"Instruction": "CNC {:04X}", "Bytes": 3, "Method": self.cnc},
            0xD5: {"Instruction": "PUSH D", "Bytes": 1, "Method": self.push},
            0xD6: {"Instruction": "SUI {:02X}", "Bytes": 2, "Method": self.sui},
            0xD7: {"Instruction": "RST 2", "Bytes": 1, "Method": self.rst},
            0xD8: {"Instruction": "RC", "Bytes": 1, "Method": self.rc},
            0xD9: {"Instruction": "*RET", "Bytes": 1, "Method": self.ret},
            0xDA: {"Instruction": "JC {:04X}", "Bytes": 3, "Method": self.jc},
            0xDB: {"Instruction": "IN {:02X}", "Bytes": 2, "Method": self.in_port},
            0xDC: {"Instruction": "CC {:04X}", "Bytes": 3, "Method": self.cc},
            0xDD: {"Instruction": "*CALL {:04X}", "Bytes": 3, "Method": self.call},
            0xDE: {"Instruction": "SBI {:04X}", "Bytes": 3, "Method": self.aci},
            0xDF: {"Instruction": "RST 3", "Bytes": 1, "Method": self.rst},

            0xE0: {"Instruction": "RPO", "Bytes": 1, "Method": self.rpo},
            0xE1: {"Instruction": "POP H", "Bytes": 1, "Method": self.pop},
            0xE2: {"Instruction": "JPO {:04X}", "Bytes": 3, "Method": self.jpo},
            0xE3: {"Instruction": "XTHL", "Bytes": 1, "Method": self.xthl},
            0xE4: {"Instruction": "CPO {:04X}", "Bytes": 3, "Method": self.cpo},
            0xE5: {"Instruction": "PUSH H", "Bytes": 1, "Method": self.push},
            0xE6: {"Instruction": "ANI {:02X}", "Bytes": 2, "Method": self.ani},
            0xE7: {"Instruction": "RST 4", "Bytes": 1, "Method": self.rst},
            0xE8: {"Instruction": "RPE", "Bytes": 1, "Method": self.rpe},
            0xE9: {"Instruction": "PCHL", "Bytes": 1, "Method": self.pchl},
            0xEA: {"Instruction": "JPE {:04X}", "Bytes": 3, "Method": self.jpe},
            0xEB: {"Instruction": "XCHG", "Bytes": 1, "Method": self.xchg},
            0xEC: {"Instruction": "CPE {:04X}", "Bytes": 3, "Method": self.cpe},
            0xED: {"Instruction": "*CALL {:04X}", "Bytes": 3, "Method": self.call},
            0xEE: {"Instruction": "XRI {:02X}", "Bytes": 2, "Method": self.xri},
            0xEF: {"Instruction": "RST 5", "Bytes": 1, "Method": self.rst},

            0xF0: {"Instruction": "RP", "Bytes": 1, "Method": self.rp},
            0xF1: {"Instruction": "POP PSW", "Bytes": 1, "Method": self.poppsw},
            0xF2: {"Instruction": "JP {:04X}", "Bytes": 3, "Method": self.jp},
            0xF3: {"Instruction": "DI", "Bytes": 1, "Method": self.di},
            0xF4: {"Instruction": "CP {:04X}", "Bytes": 3, "Method": self.cp},
            0xF5: {"Instruction": "PUSH PSW", "Bytes": 1, "Method": self.pushpsw},
            0xF6: {"Instruction": "ORI {:02X}", "Bytes": 2, "Method": self.ori},
            0xF7: {"Instruction": "RST 6", "Bytes": 1, "Method": self.rst},
            0xF8: {"Instruction": "RPM", "Bytes": 1, "Method": self.rm},
            0xF9: {"Instruction": "SPHL", "Bytes": 1, "Method": self.sphl},
            0xFA: {"Instruction": "JM {:04X}", "Bytes": 3, "Method": self.jm},
            0xFB: {"Instruction": "EI", "Bytes": 1, "Method": self.ei},
            0xFC: {"Instruction": "CM {:04X}", "Bytes": 3, "Method": self.cm},
            0xFD: {"Instruction": "*CALL {:04X}", "Bytes": 3, "Method": self.call},
            0xFE: {"Instruction": "CPI {:02X}", "Bytes": 2, "Method": self.cpi},
            0xFF: {"Instruction": "RST 7", "Bytes": 1, "Method": self.rst},
        }

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

    def set_stackpointer(self, sp):
        self.S.value = (sp >> 8) & 0xFF
        self.P.value = sp & 0xFF

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
        r = self.IR & 0x08
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

    ##################################################
    # Data Transfer Instructions                     #
    ##################################################

    def update_logical_result(self, result):
        self.Carry = 0
        self.set_flags_zsp(result)
        self.A.value = result & 0xFF

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

    ##########################################################################
    # Branch Instructions
    ##########################################################################

    def stc(self):
        # Set Carry  - (Cy) <- 1
        self.Carry = 1

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
        sp = self.get_word(self.S.value, self.P.value)
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.PC >> 8  # PC high byte
        self.memory_write()
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.PC & 0xFF  # PC low byte
        self.memory_write()
        self.S.value = (sp >> 8)
        self.P.value = sp & 0xFF
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
        sp = self.get_word(self.S.value, self.P.value)
        self.address_bus = sp
        self.memory_read()
        msb = self.data_bus
        sp += 1
        self.address_bus = sp
        self.memory_read()
        lsb = self.data_bus
        sp += 1
        self.set_stackpointer(sp)
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
        nnn = (self.IR >> 3) & 0x07  # 3 bit number from instruction
        sp = self.get_word(self.S.value, self.P.value)
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.PC >> 8  # PC high byte
        self.memory_write()
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.PC & 0xFF  # PC low byte
        self.memory_write()
        self.set_stackpointer(sp)
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
        sp = self.get_word(self.S.value, self.P.value)
        sp -= 1
        self.address_bus = sp
        self.data_bus = rh.value
        self.memory_write()
        sp -= 1
        self.address_bus = sp
        self.data_bus = rl.value
        self.memory_write()
        self.set_stackpointer(sp)

    def pushpsw(self):
        # Push Status word ((SP)-1) <- (A), ((SP)-2) <- (F)
        sp = self.get_word(self.S.value, self.P.value)
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.A.value
        self.memory_write()
        sp -= 1
        self.address_bus = sp
        self.data_bus = self.F
        self.memory_write()
        self.set_stackpointer(sp)

    def pop(self):
        # Pop register pair (rh) <- (SP), (rl) <- ((SP) +1),  (SP) <- (SP) +2
        rh, rl = self.decode_rp()
        sp = self.get_word(self.S.value, self.P.value)
        self.address_bus = sp
        self.memory_read()
        rh.value = self.data_bus
        sp += 1
        self.address_bus = sp
        self.memory_read()
        rl.value = self.data_bus
        sp += 1
        self.set_stackpointer(sp)

    def poppsw(self):
        # Pop Status Word (F) <- (SP), (A) <- ((SP) +1),  (SP) <- (SP) +2
        sp = self.get_word(self.S.value, self.P.value)
        self.address_bus = sp
        self.memory_read()
        self.pop_flags(self.data_bus)  # set all the Flags according to the data byte
        sp += 1
        self.address_bus = sp
        self.memory_read()
        self.A.value = self.data_bus
        sp += 1
        self.set_stackpointer(sp)

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
        # Input (A) <- (data)
        if self.data_bus == 1: # psuedo keyboard input port
            # cheat and read the buffer direct rather than pass through data bus
            if len(self.input_buffer) > 0:
                self.A.value = self.input_buffer.pop(0)  # pop next item
        self.cycles += 2

    def out_port(self):
        # Output (data) <- (A)
        if self.data_bus == 2: # psuedo terminal output port
            self.output_buffer.append(self.A.value)
        self.cycles += 2

    def ei(self):
        # enable interrupt
        # todo implement interrupts
        pass

    def di(self):
        # disable interrupts
        # todo implement interrupts
        pass

    def hlt(self):
        # Halt
        self.halt = True

    def nop(self):
        # do nothing
        pass
