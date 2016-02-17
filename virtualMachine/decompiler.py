
# R - register name after instruction
# C - constant value (immv)
opcodeToMnemonic = {
    0x00 : ("MOV", "R", "R"),
    0x01 : ("SET", "R", "C"),
    0x02 : ("LD",  "R", "R"),
    0x03 : ("STR", "R", "R"),
    0x03 : ("STR", "R", "R"),
    0x10 : ("ADD", "R", "R"),
    0x11 : ("SUB", "R", "R"),
    0x12 : ("MUL", "R", "R"),
    0x13 : ("DIV", "R", "R"),
    0x14 : ("MOD", "R", "R"),
    0x15 : ("OR",  "R", "R"),
    0x16 : ("AND", "R", "R"),
    0x17 : ("XOR", "R", "R"),
    0x18 : ("NOT", "R"),
    0x19 : ("SHL", "R"),
    0x1A : ("SHR", "R"),
    0x20 : ("CMP", "R", "R"),
    0x21 : ("JZ",  "C"),
    0x22 : ("JNZ", "C"),
    0x23 : ("JC",  "C"),
    0x24 : ("JNC", "C"),
    0x25 : ("JBE", "C"),
    0x26 : ("JA",  "C"),
    0x30 : ("PSH", "R"), 
    0x31 : ("POP", "R"),
}

generalRegisterIdToName = {
    0x00 : "R0",
    0x01 : "R1",
    0x02 : "R2",
    0x03 : "R3",
    0x04 : "R4",
    0x05 : "R5",
    0x06 : "R6",
    0x07 : "R7",
    0x10 : "I0",
    0x11 : "I1",
    0x12 : "I2",
    0x13 : "I3",
    0x14 : "I4",
    0x15 : "I5",
    0x16 : "I6",
    0x17 : "I7",
    0xFC : "IE",
    0xFD : "FR",
    0xFE : "SP",
    0xFF : "PC"
}

class Decompiler:
    def __init__(self):
        self.binary = ""

    def load(self, binaryStream):
        self.binary = binaryStream
        self.source = ""

    def run(self):
        index = 0;
        try:
            while index < len(self.binary):
                currentByte = self.binary[index]
                index = self._decode(index)
        except Exception as e:
            print("Exception was thrown: {0}".format(e))
            self.source = ""

    def printDecompiled(self):
        print (self.source[0:-1])

    def _appendToEndOfASource(self, code):
        self.source += code

    def _appendNewLineToSource(self):
        self.source +="\n"

    def _decodeConstant(self, index):
        constantValue = "0x{0:02x}".format(self.binary[index])
        self._appendToEndOfASource(constantValue)

    def _decodeRegister(self, index):
        try :
            byte = self.binary[index]
            self._appendToEndOfASource(generalRegisterIdToName[byte])
        except KeyError :
            print ("Couldn't decode register 0x{0:02x} at byte 0x{1:02x}".format(byte, index))
            raise Exception("Decompilation failed!")

    def _decodeOperands(self, opcode, index):
        operandsCount = len(opcodeToMnemonic[opcode])
        for operIndex, operand in enumerate(opcodeToMnemonic[opcode]):
            if operIndex == 0:   #skipping operand 0 as its mnemonic name
                self._appendToEndOfASource(operand + " ")
                continue
            if operand == "R":
                self._decodeRegister(index+operIndex)
            elif operand == "C":
                self._decodeConstant(index+operIndex)
            else:
                raise Exception("Error! Unknown operand type")
            if (operIndex < operandsCount-1):
                self._appendToEndOfASource(", ")
        self._appendNewLineToSource()
        return operandsCount

    def _decode(self,index):
        opcode = self.binary[index]
        newIndex = index + self._decodeOperands(opcode, index)
        return newIndex;

if __name__ == '__main__':
    d = Decompiler()
    programm = [
    0x00, 0x02, 0x00, 0x03, 0x01, 0x02,
    0x01, 0x02, 0x00, 0x03, 0x01, 0x02,
    ]
    print("Loading programm...")
    d.load(programm)
    print("Decompiling...")
    d.run()
    print("Decompiled:")
    d.printDecompiled()