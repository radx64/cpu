from cpu import Cpu
from memory import Memory
from terminal import Terminal

class VirtualMachine:
	def __init__(self):
		self.cpu = Cpu("RAM", "ROM", "TERMINAL")