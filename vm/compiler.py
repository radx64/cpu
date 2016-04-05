RegisterToId = {
    "R0" : 0x00,
    "R1" : 0x01,
    "R2" : 0x02,
    "R3" : 0x03,
    "R4" : 0x04,
    "R5" : 0x05,
    "R6" : 0x06,
    "R7" : 0x07,
    "I0" : 0x10,
    "I1" : 0x11,
    "I2" : 0x12,
    "I3" : 0x13,
    "I4" : 0x14,
    "I5" : 0x15,
    "I6" : 0x16,
    "I7" : 0x17,
    "IE" : 0xFC,
    "FR" : 0xFD,
    "SP" : 0xFE,
    "PC" : 0xFF
}

# R - register name after instruction
# I - constant value (immv)

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
    "JZ"   : (0x21, "I"),
    "JNZ"  : (0x22, "I"),
    "JC"   : (0x23, "I"),
    "JNC"  : (0x24, "I"),
    "JBE"  : (0x25, "I"),
    "JA"   : (0x26, "I"),
    "PUSH" : (0x30, "R"), 
    "POP"  : (0x31, "R"),
    "JMP"  : (0x40, "I"), 
    "JMPR" : (0x41, "R"),
    "CALL" : (0x42, "I"), 
    "CALR" : (0x43, "R"),
    "RET"  : (0x44, "I"), 
    "IN"   : (0x50, "I", "R"),
    "OUT"  : (0x51, "I", "R"),
    "HALT" : (0xFF, )
}

class DecodeRegisterEx(Exception):
	pass


def tokenize(source):
	sourcePreprocessed = source.replace(',','')
	tokens = sourcePreprocessed.split()
	for token in tokens:
		yield token

def decodeRegisterId(registerName):
	try:
		print("[DBG]Looking for register: " + registerName)
		return RegisterToId[registerName]
	except KeyError as e:
		raise DecodeRegisterEx("Unknown register name: " + registerName) from None

def handleInstruction(tokenizer):
	result = []
	mnemonic = next(tokenizer)
	try:
		opcode = MnemonicToOpcode[mnemonic][0]
		result.append(opcode)
		for argumentType in MnemonicToOpcode[mnemonic][1:]:
			if argumentType == "I":
				result.append(next(tokenizer))
			elif argumentType == "R":
				registerId = decodeRegisterId(next(tokenizer))
				result.append(registerId)
			else:
				raise Exception("Internal compiler error. LUT wrong!")

	except KeyError as e:
		raise Exception("Unknown mnemocnic: " + mnemonic) from None
	except StopIteration as e:
		raise Exception("Not enough arguments for mnemonic: " + mnemonic) from None
	except DecodeRegisterEx as e:
		raise Exception(e) from None		

	print("[DBG]Got mnemonic: {0}".format(mnemonic))
	return result

def compile(source):
	binary = []
	for lineIndex, line in enumerate(source.splitlines()):
		print("[DBG]Line:" + str(lineIndex + 1))
		tokenizer = tokenize(line)
		try:
			result = handleInstruction(tokenizer)
			binary.extend(result)
		except Exception as e:
			raise Exception("Compilation failed at line {0} due to error:\n\t{1}".format(lineIndex + 1, e)) from None
	return binary

def main():
	sourceCode = ("MOV R1, R2\n"
				  "HALT\n" 
				  "HALT\n"
				  "HALT\n")

	print(sourceCode)
	print("Compiling...")
	try:
		binary = compile(sourceCode)
		print("Binary below:")
		print(binary)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()




