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