import unittest
from vm.cpu import Cpu

class CpuTests(unittest.TestCase):
		def __init__(self, parameters):
		   unittest.TestCase.__init__(self, parameters)
		   self.cpu = Cpu()