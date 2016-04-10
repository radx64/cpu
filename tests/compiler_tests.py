import unittest
from vm.compiler import Compiler

class CpuTests(unittest.TestCase):
    def __init__(self, parameters):
        unittest.TestCase.__init__(self, parameters)
        self.compiler = Compiler() # (RAM, TERMINAL NotYetImpl

    def test_IfCanCompileEmptySourceCode(self):
        sourceCode = ""
        binary = self.compiler.compile(sourceCode)
        self.assertEquals(binary, [])

    def test_IfCouldDecodeRegisters(self):
        sourceCode = "MOV R0, R1"
        binary = self.compiler.compile(sourceCode)
        self.assertEquals(binary, [0x00, 0x00, 0x01])

    def test_IfItHandleLabels(self):
        sourceCode = ("start:\n"
            "MOV R0, R1\n")

        binary = self.compiler.compile(sourceCode)
        self.assertIn('start', self.compiler.labels)      

    def test_IfItHandleLabelsDeclaredAfterUse(self):
        sourceCode = ("start:\n"
            "JMP end\n"
            "end:\n")

        binary = self.compiler.compile(sourceCode)
        self.assertEquals(binary, [0x40, 0x01])