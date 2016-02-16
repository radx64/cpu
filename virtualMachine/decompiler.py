
# R - register name after instruction
# C - constant value (immv)
opcodeToMnemonic = {
    0x00 : ("MOV", "R", "R"),
    0x01 : ("SET", "R", "C"),
    0x02 : ("LD",  "R", "R"),
    0x03 : ("STR", "R", "R")
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
        print (self.source)

    def _appendToEndOfASource(self, code):
        self.source += code

    def _appendNewLineToSource(self):
        self.source +="\n"

    def _decodeConstant(self, index):
        pass
    def _decodeRegister(self, index):
        try :
            byte = self.binary[index]
            self._appendToEndOfASource(generalRegisterIdToName[byte])
        except KeyError :
            print ("Couldn't decode register 0x{0:02x} at byte 0x{1:02x}".format(byte, index))
            raise Exception("Decompilation failed!")

    def _decodeOperands(self, opcode, index):
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
            if (operIndex < len(opcodeToMnemonic[opcode])-1):
                self._appendToEndOfASource(", ")
        self._appendNewLineToSource()
        operandsCount = len(opcodeToMnemonic[opcode])
        return operandsCount

    def _decode(self,index):
        opcode = self.binary[index]
        newIndex = index + self._decodeOperands(opcode, index)
        return newIndex;




if __name__ == '__main__':
    d = Decompiler()
    programm = []
    programm.append(0x00)
    programm.append(0x21)
    programm.append(0x02)
    programm.append(0x03)
    programm.append(0x01)
    programm.append(0x02)
    d.load(programm)
    d.run()
    d.printDecompiled()