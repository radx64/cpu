from vm.port import Port

class Terminal:
    def __init__(self):
        self.readbuffer = ''
        self.writebuffer = ''

        self.controlPort = Port(self._controlPortRead, self._controlPortWrite)
        self.dataInPort  = Port(self._dataInPortRead, None)
        self.dataOutPort = Port(None, self._dataOutPortWrite)

    def _controlPortRead(self):
        if len(self.readbuffer) == 0:
            return 0x0
        else:
            return 0x1

    def _controlPortWrite(self, value):  # pragma: no cover
        pass

    def _getInput(): # pragma: no cover
        return input("INPUT>> ")

    def _dataInPortRead(self):
        while len(self.readbuffer) == 0:
            self.readbuffer = self._getInput()
        
        nextCharacter = self.readbuffer[0]
        self.readbuffer = self.readbuffer[1:]
        return nextCharacter

    def _dataOutPortWrite(self, value):
        if value == "\n":
            print(self.writebuffer)
            self.writebuffer = ''
        else:
            self.writebuffer += value