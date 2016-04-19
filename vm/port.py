class Port:
    def __init__(self, readHandle, writeHandle):
        self.readHandle = readHandle
        self.writeHandle = writeHandle
        if not hasattr(self.readHandle, '__call__') and not readHandle == None:
            raise Exception("Read handle is not callable!")

        if not hasattr(self.writeHandle, '__call__') and not writeHandle == None:
            raise Exception("Write handle is not callable!")

    def read(self):
        if not self.readHandle == None:
            return self.readHandle()

    def write(self, value):
        if not self.writeHandle == None:    
            self.writeHandle(value)