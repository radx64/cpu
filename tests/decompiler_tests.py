import unittest
from vm.decompiler import Decompiler

class DecomplierTests(unittest.TestCase):
    def __init__(self, parameters):
        unittest.TestCase.__init__(self, parameters)
        self.decompiler = Decompiler()

    def test_ExceptionThrowWhenRegisterDecodingFailed(self):
        self.decompiler.load([0x00, 0xAA, 0x02])
        self.assertRaises(Exception, self.decompiler.run)

    def test_ExceptionThrowWhenInstructionDecodingFailed(self):
        self.decompiler.load([0x04])
        self.assertRaises(Exception, self.decompiler.run)

    def test_ExceptionThrowWhenNotEnoughOperands(self):
        self.decompiler.load([0x00, 0x00])
        self.assertRaises(Exception, self.decompiler.run)

    def test_IfItsPutCommaBetweenTwoOperands(self):
        self.decompiler.load([0x00, 0x01, 0x02])
        self.decompiler.run()
        result = self.decompiler.getDecompiled()
        self.assertEqual(result, "MOV R1, R2")

    def test_IfItsNotPutCommaBetweenMnemonicInstructionAndFirstOperand(self):
        self.decompiler.load([0x18, 0x01])
        self.decompiler.run()
        result = self.decompiler.getDecompiled()
        self.assertEqual(result, "NOT R1")

    def test_IfItsPuttingConstantsHexadecimaly(self):
        self.decompiler.load([0x42, 0xFA])
        self.decompiler.run()
        result = self.decompiler.getDecompiled()
        self.assertEqual(result, "CALL 0xFA")

    def test_IfItCanHandleInstructionWithoutOperands(self):
        self.decompiler.load([0xFF])
        self.decompiler.run()
        result = self.decompiler.getDecompiled()
        self.assertEqual(result, "HALT")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DecomplierTests)
    unittest.TextTestRunner(verbosity=2).run(suite)