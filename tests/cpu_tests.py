import unittest
from vm.cpu import Cpu

class CpuTests(unittest.TestCase):
	def __init__(self, parameters):
		unittest.TestCase.__init__(self, parameters)
		self.cpu = Cpu(None, None, None)

	def test_IfCpuRegistersHaveCorrectValuesAtFirstBoot(self):
		self.assertEquals(self.cpu.R0, 0x00)
		self.assertEquals(self.cpu.R1, 0x00)
		self.assertEquals(self.cpu.R2, 0x00)
		self.assertEquals(self.cpu.R3, 0x00)
		self.assertEquals(self.cpu.R4, 0x00)
		self.assertEquals(self.cpu.R5, 0x00)
		self.assertEquals(self.cpu.R6, 0x00)
		self.assertEquals(self.cpu.R7, 0x00)
		self.assertEquals(self.cpu.I0, 0x00)
		self.assertEquals(self.cpu.I1, 0x00)
		self.assertEquals(self.cpu.I2, 0x00)
		self.assertEquals(self.cpu.I3, 0x00)
		self.assertEquals(self.cpu.I4, 0x00)
		self.assertEquals(self.cpu.I5, 0x00)
		self.assertEquals(self.cpu.I6, 0x00)
		self.assertEquals(self.cpu.I7, 0x00)
		self.assertEquals(self.cpu.IE, 0x00)
		self.assertEquals(self.cpu.FR, 0x00)
		self.assertEquals(self.cpu.SP, 0xFF)
		self.assertEquals(self.cpu.PC, 0x00)