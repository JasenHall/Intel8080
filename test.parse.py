from asm import Assembler

test =Assembler(0x100)

while True:
    code = input("Enter a line of code (type 'exit' to quit): ")
    if code == 'exit':
        break
    test.current_line = test.clean(code)
    if test.current_line is not None:
        label, command, arg = test.parse()
        print(f"Label: {label}, Command: {command}, Argument: {arg}")