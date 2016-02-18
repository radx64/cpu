import unittest
from decompiler import Decompiler

class DecomplierTests(unittest.TestCase):
	def __init__(self, parameters):
		unittest.TestCase.__init__(self, parameters)
		self.decompiler = Decompiler()

	def testExceptionThrowWhenRegisterDecodingFailed(self):
		self.decompiler.load([0x00, 0xAA, 0x02])
		self.assertRaises(Exception, self.decompiler.run)

	def testExceptionThrowWhenInstructionDecodingFailed(self):
		self.decompiler.load([0x04])
		self.assertRaises(Exception, self.decompiler.run)

	def testExceptionThrowWhenNotEnoughOperands(self):
		self.decompiler.load([0x00, 0x00])
		self.assertRaises(Exception, self.decompiler.run)

	def testIfItsPutCommaBetweenTwoOperands(self):
		self.decompiler.load([0x00, 0x01, 0x02])
		self.decompiler.run()
		result = self.decompiler.getDecompiled()
		self.assertEqual(result, "MOV R1, R2")

	def testIfItsNotPutCommaBetweenTwoOperands(self):
		self.decompiler.load([0x18, 0x01])
		self.decompiler.run()
		result = self.decompiler.getDecompiled()
		self.assertEqual(result, "NOT R1")

	def testIfItsPuttingConstantsHexadecimaly(self):
		self.decompiler.load([0x44, 0xFA])
		self.decompiler.run()
		result = self.decompiler.getDecompiled()
		self.assertEqual(result, "RET 0xFA")

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(DecomplierTests)
	unittest.TextTestRunner(verbosity=2).run(suite)