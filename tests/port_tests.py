import unittest
from unittest.mock import Mock
from vm.port import Port

class PortTests(unittest.TestCase):
    def __init__(self, parameters):
        unittest.TestCase.__init__(self, parameters)

    def test_ExceptionThrowWhenReadHandleIsNotCallable(self):
        notCallable = int()
        callable = lambda: None
        self.assertRaises(Exception, Port, notCallable, callable)

    def test_ExceptionThrowWhenWriteHandleIsNotCallable(self):
        notCallable = int()
        callable = lambda: None
        self.assertRaises(Exception, Port, callable, notCallable)

    def test_IfItReadCallableFunctionIsCalled(self):
        mock = Mock()
        port = Port(mock, None)
        port.read()
        mock.assert_called_with()

    def test_IfItWriteCallableFunctionIsCalled(self):
        mock = Mock()
        argument = 0xc00fee
        port = Port(None, mock)
        port.write(argument)
        mock.assert_called_with(argument)