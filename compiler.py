RegisterToId = {
    "R0" : 0x00,
    "R1" : 0x01,
    "R2" : 0x02,
    "R3" : 0x03,
    "R4" : 0x04,
    "R5" : 0x05,
    "R6" : 0x06,
    "R7" : 0x07,
    "FR" : 0xFD,
    "SP" : 0xFE,
    "PC" : 0xFF
}

# R - register name after instruction
# I - constant value (immv)
# A - relative address
MnemonicToOpcode = {
    "MOV"  : (0x00, "R", "R"),
    "SET"  : (0x01, "R", "I"),
    "LOAD" : (0x02, "R", "R"),
    "STOR" : (0x03, "R", "R"),
    "ADD"  : (0x10, "R", "R"),
    "SUB"  : (0x11, "R", "R"),
    "MUL"  : (0x12, "R", "R"),
    "DIV"  : (0x13, "R", "R"),
    "MOD"  : (0x14, "R", "R"),
    "OR"   : (0x15, "R", "R"),
    "AND"  : (0x16, "R", "R"),
    "XOR"  : (0x17, "R", "R"),
    "NOT"  : (0x18, "R"),
    "SHL"  : (0x19, "R"),
    "SHR"  : (0x1A, "R"),
    "CMP"  : (0x20, "R", "R"),
    "JZ"   : (0x21, "A"),
    "JNZ"  : (0x22, "A"),
    "JC"   : (0x23, "A"),
    "JNC"  : (0x24, "A"),
    "JBE"  : (0x25, "A"),
    "JA"   : (0x26, "A"),
    "PUSH" : (0x30, "R"), 
    "POP"  : (0x31, "R"),
    "JMP"  : (0x40, "A"), 
    "JMPR" : (0x41, "R"),
    "CALL" : (0x42, "A"), 
    "CALR" : (0x43, "R"),
    "RET"  : (0x44, ), 
    "IN"   : (0x50, "I", "R"),
    "OUT"  : (0x51, "I", "R"),
    "HALT" : (0xFF, )
}

WORD_SIZE = 1 << 8

class DecodeRegisterEx(Exception):
    pass

class Compiler:
    def __init__(self):
        self.binary = list()
        self.labels = dict()

    @staticmethod
    def __decodeRegisterId(registerName):
        try:
            return RegisterToId[registerName]
        except KeyError as e:
            raise DecodeRegisterEx("Unknown register name: " + registerName) from None

    @staticmethod
    def __tokenize(source):
        sourcePreprocessed = source.replace(',','')
        tokens = sourcePreprocessed.split()
        for token in tokens:
            yield token

    def __decodeLabelOrAddress(self, labelOrAddress, isSecondPass = False):
        try:
            result = int(labelOrAddress)
            return result
        except Exception as e:
            pass
        try:
            result = int(labelOrAddress, 16)
            return result
        except Exception as e:
            pass  
        try:
            address = self.labels[labelOrAddress];
            return address
        except KeyError as e:
            if isSecondPass:
                raise Exception("Unknown label: " + labelOrAddress)
            return labelOrAddress #this is left for second compiler pass

    def __decodeImmValue(self, value):
        try:
            result = int(value)
            return result
        except Exception as e:
            pass
        try:
            result = int(value, 16)
            return result
        except Exception as e:
            pass
        raise Exception("Couldn't decode immediate value of: " + value)

    def __handleInstruction(self, tokenizer):
        result = []
        mnemonic = next(tokenizer)
        if mnemonic[-1] == ":":
            self.labels[mnemonic.replace(":","")] = len(self.binary)
        else:
            try:
                opcode = MnemonicToOpcode[mnemonic][0]
                result.append(opcode)
                if len(MnemonicToOpcode[mnemonic]) == 1:
                    return result
                for argumentType in MnemonicToOpcode[mnemonic][1:]:
                    if argumentType == "I":
                        result.append(self.__decodeImmValue(next(tokenizer)))
                    elif argumentType == "R":
                        registerId = self.__decodeRegisterId(next(tokenizer))
                        result.append(registerId)
                    elif argumentType == "A":
                        address = self.__calculateRelativeJump(len(self.binary), 
                            self.__decodeLabelOrAddress(next(tokenizer)))
                        result.append(address)
                    else:
                        raise Exception("Internal compiler error. LUT wrong!") # pragma: no cover

            except KeyError as e:
                raise Exception("Unknown mnemocnic: " + mnemonic) from None
            except StopIteration as e:
                raise Exception("Not enough arguments for mnemonic: " + mnemonic) from None
            except DecodeRegisterEx as e:
                raise Exception(e) from None        
        return result

    @staticmethod
    def __removeComments(line):
        return line.rsplit(';')[0]

    def compile(self, source):
        self.binary = []
        for lineIndex, line in enumerate(source.splitlines()):
            line = self.__removeComments(line)
            if len(line) == 0:
                continue
            tokenizer = self.__tokenize(line)
            try:
                result = self.__handleInstruction(tokenizer)
                self.binary.extend(result)
            except Exception as e:
                raise Exception("Compilation failed at line {0} due to error:\n\t{1}"
                    .format(lineIndex + 1, e)) from None
        self.__resolveForwardLabels()
        return self.binary

    @staticmethod
    def __calculateRelativeJump(current, desired):
        if isinstance(desired, str):
            return desired
        if desired < current:
            return (desired - current - 2) % WORD_SIZE
        else:
            return (desired - current - 1) % WORD_SIZE

    def __resolveForwardLabels(self):
        for idx, element in enumerate(self.binary):
            try:
                if type(element) is str and not element.isdigit():
                    self.binary[idx] = self.__calculateRelativeJump(idx, 
                        self.__decodeLabelOrAddress(element, True))
            except Exception as e:
                raise e

import sys
import array
def help():  # pragma: no cover
    helpText = ("Usage: compiler.py source.asm output.bin\n"
                "\t source.asm - filename with source code\n"
                "\t output.bin - compiled program filename\n")
    print(helpText)

def readSource():  # pragma: no cover
    try:
        source = open(sys.argv[1], 'r')
        return source.read()
    except FileNotFoundError as e:
        raise Exception ("Source file " + sys.argv[1] + " not found")

def writeOutput(data):  # pragma: no cover
    try:
        output = open(sys.argv[2], 'wb')
        output.write(array.array('B', data))
    except FileNotFoundError as e:
        raise Exception ("Couldn't create " + sys.argv[1] + " file") 


def main():  # pragma: no cover
    if len(sys.argv) != 3:
        help()
        return
    compiler = Compiler()
    binary = compiler.compile(readSource())
    writeOutput(binary)
    print("Size of binary: " + str(len(binary)) + " bytes. " 
        + str(WORD_SIZE - len(binary)) + " bytes free left.")

if __name__ == '__main__':  # pragma: no cover
    try:
        main()
    except Exception as e:
        print(e)
