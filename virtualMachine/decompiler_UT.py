import unittest
from decompiler import Decompiler

class DecomplierTests(unittest.TestCase):
	def __init__(self, parameters):
		unittest.TestCase.__init__(self, parameters)
		self.decompiler = Decompiler()

	def testExceptionThrowWhenRegisterDecodingFailed(self):
		self.decompiler.load([0x00, 0xAA, 0x02])
		self.assertRaises(Exception, self.decompiler.run)

	def testExceptionThrowWhenNotEnoughOperands(self):
		self.decompiler.load([0x00, 0x00])
		self.assertRaises(Exception, self.decompiler.run)

	def testMov(self):
		self.decompiler.load([0x00, 0x01, 0x02])
		self.decompiler.run()
		result = self.decompiler.getDecompiled()
		self.assertEqual(result, "MOV R1, R2")

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(DecomplierTests)
	unittest.TextTestRunner(verbosity=2).run(suite)