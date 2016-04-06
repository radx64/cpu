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
    "JMP"  : (0x40, "I"), 
    "JMPR" : (0x41, "R"),
    "CALL" : (0x42, "I"), 
    "CALR" : (0x43, "R"),
    "RET"  : (0x44, "I"), 
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
			print("[DBG]Looking for register: " + registerName)
			return RegisterToId[registerName]
		except KeyError as e:
			raise DecodeRegisterEx("Unknown register name: " + registerName) from None

	@staticmethod
	def __tokenize(source):
		sourcePreprocessed = source.replace(',','')
		tokens = sourcePreprocessed.split()
		for token in tokens:
			yield token

	def __decodeLabelOrAddress(self, labelOrAddress):
		try:
			result = int(labelOrAddress)
			return result
		except Exception as e:
			print("[DBG] Not and INT...")
		try:
			result = int(labelOrAddress, 16)
			return result
		except Exception as e:
			print("[DBG] Not and HEX INT...")		
		try:
			address = self.labels[labelOrAddress];
			return address
		except KeyError as e:
			print("[DBG] Label not found")
			raise Exception("Couldn't decode " + labelOrAddress)

	def __handleInstruction(self, tokenizer):
		result = []
		mnemonic = next(tokenizer)
		if mnemonic[-1] == ":":
			print("[DBG] Looks like I've got an label %s" % mnemonic)
			self.labels[mnemonic.replace(":","")] = len(self.binary)
		else:
			try:
				opcode = MnemonicToOpcode[mnemonic][0]
				result.append(opcode)
				for argumentType in MnemonicToOpcode[mnemonic][1:]:
					if argumentType == "I":
						result.append(next(tokenizer))
					elif argumentType == "R":
						registerId = self.__decodeRegisterId(next(tokenizer))
						result.append(registerId)
					elif argumentType == "A":
						address = self.__calculateRelativeJump(len(self.binary), self.__decodeLabelOrAddress(next(tokenizer)))
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


	def compile(self, source):
		for lineIndex, line in enumerate(source.splitlines()):
			print("[DBG]Line:" + str(lineIndex + 1))
			tokenizer = self.__tokenize(line)
			try:
				result = self.__handleInstruction(tokenizer)
				self.binary.extend(result)
			except Exception as e:
				raise Exception("Compilation failed at line {0} due to error:\n\t{1}".format(lineIndex + 1, e)) from None
		self.__resolveForwardLabels()
		return self.binary

	@staticmethod
	def __calculateRelativeJump(current, desired):
		if desired < current:
			return WORD_SIZE - (desired + current)
		else:
			return desired - current

	def __resolveForwardLabels(self):
		for idx, element in enumerate(self.binary):
			try:
				if type(element) is str and not element.isdigit():
					self.binary[idx] = self.__calculateRelativeJump(idx, self.__decodeLabelOrAddress(element))
			except Exception as e:
				raise e

def main():
	sourceCode = ("start:\n"
				  "MOV R1, R2\n"
				  "SHL R1 \n"
				  "JMP start\n" 
				  "HALT\n"
				  "HALT\n"
				  "end:\n")

	print(sourceCode)
	print("Compiling...")
	try:
		compiler = Compiler()
		binary = compiler.compile(sourceCode)
		print("Binary below:")
		print(binary)
		print("Found labels:")
		print(compiler.labels)

	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()



