print ("Cpu imported.")

class Cpu:
	def __init__(self, ram, rom, terminal):
		print ("Cpu created.")
		self.ram = ram
		self.rom = rom
		self.terminal = terminal
		