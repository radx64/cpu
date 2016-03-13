import unittest
from vm.cpu import Cpu

class CpuTests(unittest.TestCase):
	def __init__(self, parameters):
		unittest.TestCase.__init__(self, parameters)
		self.ram = [0x00] * 256;
		self.cpu = Cpu(self.ram, None) # (RAM, ROM, TERMINAL) NotYetImpl

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

	def test_HALT_instructionHandling(self):
		programm = [0xFF]
		self.cpu.run(programm)
		self.assertEquals(self.cpu.PC, 0x01)

	def test_SET_instructionHandling(self):
		programm = [0x01, 0x0, 0xAB, 0xFF]
		self.cpu.run(programm);
		self.assertEquals(self.cpu.R0, 0xAB)

	def test_MOV_instructionHandling(self):
		self.cpu.R0 = 0xAB
		programm = [0x00, 0x01, 0x00, 0xFF] # SET and then MOV
		self.cpu.run(programm)
		self.assertEquals(self.cpu.R1, 0xAB)