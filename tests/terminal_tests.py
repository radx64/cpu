import unittest
import sys
from io import StringIO
from vm.terminal import Terminal
from unittest.mock import Mock

class TerminalTests(unittest.TestCase):
    def __init__(self, parameters):
        unittest.TestCase.__init__(self, parameters)
        self.terminal = Terminal()

    def test_IfItCanPrintSomeText(self):
        normalStdOut = sys.stdout
        out = StringIO()
        sys.stdout = out
        self.terminal.dataOutPort.write(65)
        self.terminal.dataOutPort.write(66)
        self.terminal.dataOutPort.write(67)
        self.terminal.dataOutPort.write(10)
        self.assertEqual(out.getvalue().strip(), "ABC")
        sys.stdout = normalStdOut

    def test_IfItCanReadSomeTextToBuffer(self):
        self.terminal._getInput = Mock(return_value="SOME_TEXT")
        char = self.terminal.dataInPort.read()
        self.assertEqual(chr(char) + self.terminal.readbuffer, 'SOME_TEXT')

    def test_IfItReturnCorrectControlByte(self):
        self.assertEqual(self.terminal.controlPort.read(), 0x0)
        self.terminal._getInput = Mock(return_value="SOME_TEXT")
        char = self.terminal.dataInPort.read()
        self.assertEqual(self.terminal.controlPort.read(), 0x1)
