"""
Main entry point for Intel 8080 based machine
"""
from cpu import CPU

def main():
    cpu = CPU()
    #########################
    # custom init stuff - we'll borrow some routines from the CPU
    cpu.set_stackpointer(0xEE00)  # set stackpointer to 0xEE00 to give stack space
    ### write a bit of test code
    cpu.memory[0x0000] = 0x00  # nop
    cpu.memory[0x0001] = 0x00  # nop
    cpu.memory[0x0002] = 0x00  # nop
    cpu.memory[0x0003] = 0x01  # lxi B, $AABB
    cpu.memory[0x0004] = 0xBB  # low byte
    cpu.memory[0x0005] = 0xAA  # high byte
    cpu.memory[0x0006] = 0x76  # hlt

    ########################################################################
    # Main processor cycle
    ########################################################################
    while cpu.halt is False:
        cpu.fetch_instruction()
        cpu.execute_instruction()
        cpu.show_registers()

if __name__ == '__main__':
    main()
