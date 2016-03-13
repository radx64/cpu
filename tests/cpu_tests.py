import unittest
from vm.cpu import Cpu

class CpuTests(unittest.TestCase):
	def __init__(self, parameters):
		unittest.TestCase.__init__(self, parameters)
		self.ram = [0x00] * 256;	# so much blocks of memory :)
		self.cpu = Cpu(self.ram, None) # (RAM, TERMINAL NotYetImpl

	def test_IfCpuGeneralRegistersHaveCorrectValuesAtFirstBoot(self):
		self.assertEquals(self.cpu.R0, 0x00)
		self.assertEquals(self.cpu.R1, 0x00)
		self.assertEquals(self.cpu.R2, 0x00)
		self.assertEquals(self.cpu.R3, 0x00)
		self.assertEquals(self.cpu.R4, 0x00)
		self.assertEquals(self.cpu.R5, 0x00)
		self.assertEquals(self.cpu.R6, 0x00)
		self.assertEquals(self.cpu.R7, 0x00)

	def test_IfCpuInterruptRegistersHaveCorrectValuesAtBoot(self):
		self.assertEquals(self.cpu.I0, 0x00)
		self.assertEquals(self.cpu.I1, 0x00)
		self.assertEquals(self.cpu.I2, 0x00)
		self.assertEquals(self.cpu.I3, 0x00)
		self.assertEquals(self.cpu.I4, 0x00)
		self.assertEquals(self.cpu.I5, 0x00)
		self.assertEquals(self.cpu.I6, 0x00)
		self.assertEquals(self.cpu.I7, 0x00)

	def test_IfCpuInterruptEnableRegisterHaveCorrectValueAtBoot(self):
		self.assertEquals(self.cpu.IE, 0x00)

	def test_IfCpuFlagRegisterHaveCorrectValueAtBoot(self):
		self.assertEquals(self.cpu.FR, 0x00)

	def test_IfCpuStackPointerRegisterHaveCorrectValueAtBoot(self):
		self.assertEquals(self.cpu.SP, 0xFF)

	def test_IfCpuProgamCounterHaveCorrectValueAtBoot(self):
		self.assertEquals(self.cpu.PC, 0x00)

	def test_IfSourceRegisterDecodingThrowsException(self):
		programm = [0x00,0x00,0xAA]
		self.assertRaises(Exception, self.cpu.run, programm)\

	def test_IfDestinationRegisterDecodingThrowsException(self):
		programm = [0x00,0xAA,0x00]
		self.assertRaises(Exception, self.cpu.run, programm)

	def test_IfMemoryAddressingThrowExceptionForStrageAddressSpaceAccess(self):
		self.cpu.R0 = -0xFF
		programm = [0x02, 0x01, 0x00, 0xFF]
		self.assertRaises(Exception, self.cpu.run, programm)

	def test_MOV_instructionHandling(self):
		self.cpu.R0 = 0xAB
		programm = [0x00, 0x01, 0x00, 0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R1, 0xAB)

	def test_SET_instructionHandling(self):
		programm = [0x01, 0x00, 0xAB, 0xFF]
		self.cpu.run(programm);
		self.assertEquals(self.cpu.R0, 0xAB)

	def test_LOAD_instructionHandling(self):
		self.ram[0xFF] = 0xAB
		self.cpu.R0 = 0xFF
		programm = [0x02, 0x01, 0x00, 0xFF]
		self.cpu.run(programm);
		self.assertEquals(self.cpu.R1, 0xAB)

	def test_STOR_instructionHandling(self):
		self.cpu.R0 = 0xAB
		self.cpu.R1 = 0xFF
		programm = [0x03, 0x01, 0x00, 0xFF]
		self.cpu.run(programm);
		self.assertEquals(self.ram[0xFF], 0xAB)

	def test_ADD_instructionHandling(self):
		self.cpu.R0 = 0x01
		self.cpu.R1 = 0x02
		programm = [0x10, 0x00, 0x01, 0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R0, 0x03)

	def test_ADD_instructionHandlingCarryFlag(self):
		self.cpu.R0 = 0x01
		self.cpu.R1 = 0xFF
		programm = [0x10, 0x00, 0x01, 0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R0, 0x00)
		self.assertEquals(self.cpu.FR, 0x02)  # carry bit set

	def test_SUB_instructionHandling(self):
		self.cpu.R0 = 0x02
		self.cpu.R1 = 0x01
		programm = [0x11, 0x00, 0x01, 0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R0, 0x01)

	def test_SUB_instructionHandlingCarryFlag(self):
		self.cpu.R0 = 0x01
		self.cpu.R1 = 0x02
		programm = [0x11, 0x00, 0x01, 0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R0, 0xFF)
		self.assertEquals(self.cpu.FR, 0x02)  # carry bit set

	def test_HALT_instructionHandling(self):
		programm = [0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.PC, 0x01)