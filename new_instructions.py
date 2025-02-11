INSTRUCTION_SET = {
            0x00: {"Instruction": "NOP", "Bytes": 1 },
            0x01: {"Instruction": "LXI B,", "Bytes": 3 },
            0x02: {"Instruction": "STAX B", "Bytes": 1 },
            0x03: {"Instruction": "INX B", "Bytes": 1 },
            0x04: {"Instruction": "INR B", "Bytes": 1 },
            0x05: {"Instruction": "DCR B", "Bytes": 1 },
            0x06: {"Instruction": "MVI B,", "Bytes": 2},
            0x07: {"Instruction": "RLC", "Bytes": 1},
            0x08: {"Instruction": "*NOP", "Bytes": 1},
            0x09: {"Instruction": "DAD B", "Bytes": 1},
            0x0A: {"Instruction": "LDAX B", "Bytes": 1},
            0x0B: {"Instruction": "DCX B", "Bytes": 1},
            0x0C: {"Instruction": "INR C", "Bytes": 1},
            0x0D: {"Instruction": "DCR C", "Bytes": 1},
            0x0E: {"Instruction": "MVI C,", "Bytes": 2},
            0x0F: {"Instruction": "RRC", "Bytes": 1},

            0x10: {"Instruction": "*NOP", "Bytes": 1},
            0x11: {"Instruction": "LXI D,", "Bytes": 3},
            0x12: {"Instruction": "STAX D", "Bytes": 1},
            0x13: {"Instruction": "INX D", "Bytes": 1},
            0x14: {"Instruction": "INR D", "Bytes": 1},
            0x15: {"Instruction": "DCR D", "Bytes": 1},
            0x16: {"Instruction": "MVI D,", "Bytes": 2},
            0x17: {"Instruction": "RAL", "Bytes": 1},
            0x18: {"Instruction": "*NOP", "Bytes": 1},
            0x19: {"Instruction": "DAD D", "Bytes": 1},
            0x1A: {"Instruction": "LDAX D", "Bytes": 1},
            0x1B: {"Instruction": "DCX D", "Bytes": 1},
            0x1C: {"Instruction": "INR E", "Bytes": 1},
            0x1D: {"Instruction": "DCR E", "Bytes": 1},
            0x1E: {"Instruction": "MVI E,", "Bytes": 2},
            0x1F: {"Instruction": "RAR", "Bytes": 1},

            0x20: {"Instruction": "*NOP", "Bytes": 1},
            0x21: {"Instruction": "LXI H,", "Bytes": 3},
            0x22: {"Instruction": "SHLD", "Bytes": 3},
            0x23: {"Instruction": "INX H", "Bytes": 1},
            0x24: {"Instruction": "INR H", "Bytes": 1},
            0x25: {"Instruction": "DCR H", "Bytes": 1},
            0x26: {"Instruction": "MVI H,", "Bytes": 2},
            0x27: {"Instruction": "DAA", "Bytes": 1},
            0x28: {"Instruction": "*NOP", "Bytes": 1},
            0x29: {"Instruction": "DAD H", "Bytes": 1},
            0x2A: {"Instruction": "LHLD", "Bytes": 3},
            0x2B: {"Instruction": "DCX H", "Bytes": 1},
            0x2C: {"Instruction": "INR L", "Bytes": 1},
            0x2D: {"Instruction": "DCR L", "Bytes": 1},
            0x2E: {"Instruction": "MVI L,", "Bytes": 2},
            0x2F: {"Instruction": "CMA", "Bytes": 1},

            0x30: {"Instruction": "*NOP", "Bytes": 1},
            0x31: {"Instruction": "LXI SP,", "Bytes": 3},
            0x32: {"Instruction": "STA", "Bytes": 3},
            0x33: {"Instruction": "INX SP", "Bytes": 1},
            0x34: {"Instruction": "INR M", "Bytes": 1},
            0x35: {"Instruction": "DCR M", "Bytes": 1},
            0x36: {"Instruction": "MVI M,", "Bytes": 2},
            0x37: {"Instruction": "STC", "Bytes": 1},
            0x38: {"Instruction": "*NOP", "Bytes": 1},
            0x39: {"Instruction": "DAD SP", "Bytes": 1},
            0x3A: {"Instruction": "LDA", "Bytes": 3},
            0x3B: {"Instruction": "DCX SP", "Bytes": 1},
            0x3C: {"Instruction": "INR A", "Bytes": 1},
            0x3D: {"Instruction": "DCR A", "Bytes": 1},
            0x3E: {"Instruction": "MVI A,", "Bytes": 2},
            0x3F: {"Instruction": "CMC", "Bytes": 1},

            0x40: {"Instruction": "MOV B,B", "Bytes": 1},
            0x41: {"Instruction": "MOV B,C", "Bytes": 1},
            0x42: {"Instruction": "MOV B,D", "Bytes": 1},
            0x43: {"Instruction": "MOV B,E", "Bytes": 1},
            0x44: {"Instruction": "MOV B,H", "Bytes": 1},
            0x45: {"Instruction": "MOV B,L", "Bytes": 1},
            0x46: {"Instruction": "MOV B,M", "Bytes": 1},
            0x47: {"Instruction": "MOV B,A", "Bytes": 1},
            0x48: {"Instruction": "MOV C,B", "Bytes": 1},
            0x49: {"Instruction": "MOV C,C", "Bytes": 1},
            0x4A: {"Instruction": "MOV C,D", "Bytes": 1},
            0x4B: {"Instruction": "MOV C,E", "Bytes": 1},
            0x4C: {"Instruction": "MOV C,H", "Bytes": 1},
            0x4D: {"Instruction": "MOV C,L", "Bytes": 1},
            0x4E: {"Instruction": "MOV C,M", "Bytes": 1},
            0x4F: {"Instruction": "MOV C,A", "Bytes": 1},

            0x50: {"Instruction": "MOV D,B", "Bytes": 1},
            0x51: {"Instruction": "MOV D,C", "Bytes": 1},
            0x52: {"Instruction": "MOV D,D", "Bytes": 1},
            0x53: {"Instruction": "MOV D,E", "Bytes": 1},
            0x54: {"Instruction": "MOV D,H", "Bytes": 1},
            0x55: {"Instruction": "MOV D,L", "Bytes": 1},
            0x56: {"Instruction": "MOV D,M", "Bytes": 1},
            0x57: {"Instruction": "MOV D,A", "Bytes": 1},
            0x58: {"Instruction": "MOV E,B", "Bytes": 1},
            0x59: {"Instruction": "MOV E,C", "Bytes": 1},
            0x5A: {"Instruction": "MOV E,D", "Bytes": 1},
            0x5B: {"Instruction": "MOV E,E", "Bytes": 1},
            0x5C: {"Instruction": "MOV E,H", "Bytes": 1},
            0x5D: {"Instruction": "MOV E,L", "Bytes": 1},
            0x5E: {"Instruction": "MOV E,M", "Bytes": 1},
            0x5F: {"Instruction": "MOV E,A", "Bytes": 1},

            0x60: {"Instruction": "MOV H,B", "Bytes": 1},
            0x61: {"Instruction": "MOV H,C", "Bytes": 1},
            0x62: {"Instruction": "MOV H,D", "Bytes": 1},
            0x63: {"Instruction": "MOV H,E", "Bytes": 1},
            0x64: {"Instruction": "MOV H,H", "Bytes": 1},
            0x65: {"Instruction": "MOV H,L", "Bytes": 1},
            0x66: {"Instruction": "MOV H,M", "Bytes": 1},
            0x67: {"Instruction": "MOV H,A", "Bytes": 1},
            0x68: {"Instruction": "MOV L,B", "Bytes": 1},
            0x69: {"Instruction": "MOV L,C", "Bytes": 1},
            0x6A: {"Instruction": "MOV L,D", "Bytes": 1},
            0x6B: {"Instruction": "MOV L,E", "Bytes": 1},
            0x6C: {"Instruction": "MOV L,H", "Bytes": 1},
            0x6D: {"Instruction": "MOV L,L", "Bytes": 1},
            0x6E: {"Instruction": "MOV L,M", "Bytes": 1},
            0x6F: {"Instruction": "MOV L,A", "Bytes": 1},

            0x70: {"Instruction": "MOV M,B", "Bytes": 1},
            0x71: {"Instruction": "MOV M,C", "Bytes": 1},
            0x72: {"Instruction": "MOV M,D", "Bytes": 1},
            0x73: {"Instruction": "MOV M,E", "Bytes": 1},
            0x74: {"Instruction": "MOV M,H", "Bytes": 1},
            0x75: {"Instruction": "MOV M,L", "Bytes": 1},
            0x76: {"Instruction": "HLT", "Bytes": 1},
            0x77: {"Instruction": "MOV M,A", "Bytes": 1},
            0x78: {"Instruction": "MOV A,B", "Bytes": 1},
            0x79: {"Instruction": "MOV A,C", "Bytes": 1},
            0x7A: {"Instruction": "MOV A,D", "Bytes": 1},
            0x7B: {"Instruction": "MOV A,E", "Bytes": 1},
            0x7C: {"Instruction": "MOV A,H", "Bytes": 1},
            0x7D: {"Instruction": "MOV A,L", "Bytes": 1},
            0x7E: {"Instruction": "MOV A,M", "Bytes": 1},
            0x7F: {"Instruction": "MOV A,A", "Bytes": 1},

            0x80: {"Instruction": "ADD B", "Bytes": 1},
            0x81: {"Instruction": "ADD C", "Bytes": 1},
            0x82: {"Instruction": "ADD D", "Bytes": 1},
            0x83: {"Instruction": "ADD E", "Bytes": 1},
            0x84: {"Instruction": "ADD H", "Bytes": 1},
            0x85: {"Instruction": "ADD L", "Bytes": 1},
            0x86: {"Instruction": "ADD M", "Bytes": 1},
            0x87: {"Instruction": "ADD A", "Bytes": 1},
            0x88: {"Instruction": "ADC B", "Bytes": 1},
            0x89: {"Instruction": "ADC C", "Bytes": 1},
            0x8A: {"Instruction": "ADC D", "Bytes": 1},
            0x8B: {"Instruction": "ADC E", "Bytes": 1},
            0x8C: {"Instruction": "ADC H", "Bytes": 1},
            0x8D: {"Instruction": "ADC L", "Bytes": 1},
            0x8E: {"Instruction": "ADC M", "Bytes": 1},
            0x8F: {"Instruction": "ADC A", "Bytes": 1},

            0x90: {"Instruction": "SUB B", "Bytes": 1},
            0x91: {"Instruction": "SUB C", "Bytes": 1},
            0x92: {"Instruction": "SUB D", "Bytes": 1},
            0x93: {"Instruction": "SUB E", "Bytes": 1},
            0x94: {"Instruction": "SUB H", "Bytes": 1},
            0x95: {"Instruction": "SUB L", "Bytes": 1},
            0x96: {"Instruction": "SUB M", "Bytes": 1},
            0x97: {"Instruction": "SUB A", "Bytes": 1},
            0x98: {"Instruction": "SBB B", "Bytes": 1},
            0x99: {"Instruction": "SBB C", "Bytes": 1},
            0x9A: {"Instruction": "SBB D", "Bytes": 1},
            0x9B: {"Instruction": "SBB E", "Bytes": 1},
            0x9C: {"Instruction": "SBB H", "Bytes": 1},
            0x9D: {"Instruction": "SBB L", "Bytes": 1},
            0x9E: {"Instruction": "SBB M", "Bytes": 1},
            0x9F: {"Instruction": "SBB A", "Bytes": 1},

            0xA0: {"Instruction": "ANA B", "Bytes": 1},
            0xA1: {"Instruction": "ANA C", "Bytes": 1},
            0xA2: {"Instruction": "ANA D", "Bytes": 1},
            0xA3: {"Instruction": "ANA E", "Bytes": 1},
            0xA4: {"Instruction": "ANA H", "Bytes": 1},
            0xA5: {"Instruction": "ANA L", "Bytes": 1},
            0xA6: {"Instruction": "ANA M", "Bytes": 1},
            0xA7: {"Instruction": "ANA A", "Bytes": 1},
            0xA8: {"Instruction": "SBB B", "Bytes": 1},
            0xA9: {"Instruction": "SBB C", "Bytes": 1},
            0xAA: {"Instruction": "SBB D", "Bytes": 1},
            0xAB: {"Instruction": "SBB E", "Bytes": 1},
            0xAC: {"Instruction": "SBB H", "Bytes": 1},
            0xAD: {"Instruction": "SBB L", "Bytes": 1},
            0xAE: {"Instruction": "SBB M", "Bytes": 1},
            0xAF: {"Instruction": "SBB A", "Bytes": 1},

            0xB0: {"Instruction": "ORA B", "Bytes": 1},
            0xB1: {"Instruction": "ORA C", "Bytes": 1},
            0xB2: {"Instruction": "ORA D", "Bytes": 1},
            0xB3: {"Instruction": "ORA E", "Bytes": 1},
            0xB4: {"Instruction": "ORA H", "Bytes": 1},
            0xB5: {"Instruction": "ORA L", "Bytes": 1},
            0xB6: {"Instruction": "ORA M", "Bytes": 1},
            0xB7: {"Instruction": "ORA A", "Bytes": 1},
            0xB8: {"Instruction": "CMP B", "Bytes": 1},
            0xB9: {"Instruction": "CMP C", "Bytes": 1},
            0xBA: {"Instruction": "CMP D", "Bytes": 1},
            0xBB: {"Instruction": "CMP E", "Bytes": 1},
            0xBC: {"Instruction": "CMP H", "Bytes": 1},
            0xBD: {"Instruction": "CMP L", "Bytes": 1},
            0xBE: {"Instruction": "CMP M", "Bytes": 1},
            0xBF: {"Instruction": "CMP A", "Bytes": 1},

            0xC0: {"Instruction": "RNZ", "Bytes": 1},
            0xC1: {"Instruction": "POP B", "Bytes": 1},
            0xC2: {"Instruction": "JNZ", "Bytes": 3},
            0xC3: {"Instruction": "JMP", "Bytes": 3},
            0xC4: {"Instruction": "CNZ", "Bytes": 3},
            0xC5: {"Instruction": "PUSH B", "Bytes": 1},
            0xC6: {"Instruction": "ADI", "Bytes": 2},
            0xC7: {"Instruction": "RST 0", "Bytes": 1},
            0xC8: {"Instruction": "RZ", "Bytes": 1},
            0xC9: {"Instruction": "RET", "Bytes": 1},
            0xCA: {"Instruction": "JZ", "Bytes": 3},
            0xCB: {"Instruction": "*JMP", "Bytes": 3},
            0xCC: {"Instruction": "CZ", "Bytes": 3},
            0xCD: {"Instruction": "CALL", "Bytes": 3},
            0xCE: {"Instruction": "ACI", "Bytes": 2},
            0xCF: {"Instruction": "RST 1", "Bytes": 1},

            0xD0: {"Instruction": "RNC", "Bytes": 1},
            0xD1: {"Instruction": "POP D", "Bytes": 1},
            0xD2: {"Instruction": "JNC", "Bytes": 3},
            0xD3: {"Instruction": "OUT", "Bytes": 2},
            0xD4: {"Instruction": "CNC", "Bytes": 3},
            0xD5: {"Instruction": "PUSH D", "Bytes": 1},
            0xD6: {"Instruction": "SUI", "Bytes": 2},
            0xD7: {"Instruction": "RST 2", "Bytes": 1},
            0xD8: {"Instruction": "RC", "Bytes": 1},
            0xD9: {"Instruction": "*RET", "Bytes": 1},
            0xDA: {"Instruction": "JC", "Bytes": 3},
            0xDB: {"Instruction": "IN", "Bytes": 2},
            0xDC: {"Instruction": "CC", "Bytes": 3},
            0xDD: {"Instruction": "*CALL", "Bytes": 3},
            0xDE: {"Instruction": "SBI", "Bytes": 3},
            0xDF: {"Instruction": "RST 3", "Bytes": 1},

            0xE0: {"Instruction": "RPO", "Bytes": 1},
            0xE1: {"Instruction": "POP H", "Bytes": 1},
            0xE2: {"Instruction": "JPO", "Bytes": 3},
            0xE3: {"Instruction": "XTHL", "Bytes": 1},
            0xE4: {"Instruction": "CPO", "Bytes": 3},
            0xE5: {"Instruction": "PUSH H", "Bytes": 1},
            0xE6: {"Instruction": "ANI", "Bytes": 2},
            0xE7: {"Instruction": "RST 4", "Bytes": 1},
            0xE8: {"Instruction": "RPE", "Bytes": 1},
            0xE9: {"Instruction": "PCHL", "Bytes": 1},
            0xEA: {"Instruction": "JPE", "Bytes": 3},
            0xEB: {"Instruction": "XCHG", "Bytes": 1},
            0xEC: {"Instruction": "CPE", "Bytes": 3},
            0xED: {"Instruction": "*CALL", "Bytes": 3},
            0xEE: {"Instruction": "XRI", "Bytes": 2},
            0xEF: {"Instruction": "RST 5", "Bytes": 1},

            0xF0: {"Instruction": "RP", "Bytes": 1},
            0xF1: {"Instruction": "POP PSW", "Bytes": 1},
            0xF2: {"Instruction": "JP", "Bytes": 3},
            0xF3: {"Instruction": "DI", "Bytes": 1},
            0xF4: {"Instruction": "CP", "Bytes": 3},
            0xF5: {"Instruction": "PUSH PSW", "Bytes": 1},
            0xF6: {"Instruction": "ORI", "Bytes": 2},
            0xF7: {"Instruction": "RST 6", "Bytes": 1},
            0xF8: {"Instruction": "RPM", "Bytes": 1},
            0xF9: {"Instruction": "SPHL", "Bytes": 1},
            0xFA: {"Instruction": "JM", "Bytes": 3},
            0xFB: {"Instruction": "EI", "Bytes": 1},
            0xFC: {"Instruction": "CM", "Bytes": 3},
            0xFD: {"Instruction": "*CALL", "Bytes": 3},
            0xFE: {"Instruction": "CPI", "Bytes": 2},
            0xFF: {"Instruction": "RST 7", "Bytes": 1},
}