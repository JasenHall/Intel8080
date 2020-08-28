"""
Main entry point for Intel 8080 based machine
"""
from cpu import CPU
from monitor import Monitor


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
