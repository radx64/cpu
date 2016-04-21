import sys
import array
from vm.cpu import Cpu
from vm.terminal import Terminal

def help():  # pragma: no cover
    helpText = ("Usage: vm.py program.bin\n"
                "\t program.bin - program filename\n")
    print(helpText)

def readBinary():  # pragma: no cover
    try:
        source = open(sys.argv[1], 'rb')
        return array.array('B', source.read()).tolist()
    except FileNotFoundError as e:
        raise Exception ("Program file " + sys.argv[1] + " not found")

def main():  # pragma: no cover
    if len(sys.argv) != 2:
        help()
        return
    ram = [0xFF] * 256;
    terminal = Terminal()
    cpu = Cpu(ram, terminal)
    program = readBinary()
    cpu.run(program)

if __name__ == '__main__':  # pragma: no cover
    try:
        main()
    except Exception as e:
        print(e)