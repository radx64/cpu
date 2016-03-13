class Cpu:
    def _initRegisters(self):
        self.R0 = 0x00;
        self.R1 = 0x00;
        self.R2 = 0x00;
        self.R3 = 0x00;
        self.R4 = 0x00;
        self.R5 = 0x00;
        self.R6 = 0x00;
        self.R7 = 0x00;
        self.I0 = 0x00;
        self.I1 = 0x00;
        self.I2 = 0x00;
        self.I3 = 0x00;
        self.I4 = 0x00;
        self.I5 = 0x00;
        self.I6 = 0x00;
        self.I7 = 0x00;
        self.IE = 0x00;
        self.FR = 0x00;
        self.SP = 0xFF;
        self.PC = 0x00;   

    def _getOpcodeToHandlerMapping(self):
        return {
            0x00 : self.__MOV,
            0x01 : self.__SET,
            0x02 : self.__LOAD,
            0x03 : self.__STOR,
            0x10 : self.__ADD,
            0x11 : self.__SUB,
            0x12 : self.__MUL,
            0x13 : self.__DIV,
            0x14 : self.__MOD,
            0x15 : self.__OR,
            0x16 : self.__AND,
            0x17 : self.__XOR,
            0x18 : self.__NOT,
            0x19 : self.__SHL,
            0x1A : self.__SHR,
            0x20 : self.__CMP,
            0x21 : self.__JZ,
            0x22 : self.__JNZ,
            0x23 : self.__JC,
            0x24 : self.__JNC,
            0x25 : self.__JBE,
            0x26 : self.__JA,
            0x30 : self.__PUSH,
            0x31 : self.__POP,
            0x40 : self.__JMP,
            0x41 : self.__JMPR,
            0x42 : self.__CALL,
            0x43 : self.__CALR,
            0x44 : self.__RET,
            0xFF : self.__HALT }
    
    def __init__(self, ram, terminal):
        self.ram = ram
        self.rom = []
        self.running = False
        self.terminal = terminal
        self._initRegisters()
        self.opcodeToHandlerMapping = self._getOpcodeToHandlerMapping()

    def __fetchNextByteFromRom(self):
        byte = self.rom[self.PC]
        self.PC += 1
        return byte

    def __setRegisterValueById(self, id, value):
        print ("Will set register {0}, with {1}".format(id,value))

        if id == 0x00 : 
            self.R0 = value
        elif id == 0x01 : 
            self.R1 = value
        elif id == 0x02 : 
            self.R2 = value
        elif id == 0x03 : 
            self.R3 = value
        elif id == 0x04 : 
            self.R4 = value
        elif id == 0x05 : 
            self.R5 = value
        elif id == 0x06 : 
            self.R6 = value
        elif id == 0x07 : 
            self.R7 = value
        elif id == 0x10 : 
            self.I0 = value
        elif id == 0x11 : 
            self.I1 = value
        elif id == 0x12 : 
            self.I2 = value
        elif id == 0x13 : 
            self.I3 = value
        elif id == 0x14 : 
            self.I4 = value
        elif id == 0x15 : 
            self.I5 = value
        elif id == 0x16 : 
            self.I6 = value
        elif id == 0x17 : 
            self.I7 = value
        elif id == 0xFC : 
            self.IE = value
        elif id == 0xFD : 
            self.FR = value
        elif id == 0xFE : 
            self.SP = value
        elif id == 0xFF : 
            self.PC = value
        else :
            raise Exception("Unknown register " + str(id))

    def __getRegisterValueById(self, id):
        print ("Will get register {0}".format(id))

        if id == 0x00 : 
            return self.R0
        elif id == 0x01 : 
            return self.R1
        elif id == 0x02 : 
            return self.R2
        elif id == 0x03 : 
            return self.R3
        elif id == 0x04 : 
            return self.R4
        elif id == 0x05 : 
            return self.R5
        elif id == 0x06 : 
            return self.R6
        elif id == 0x07 : 
            return self.R7
        elif id == 0x10 : 
            return self.I0
        elif id == 0x11 : 
            return self.I1
        elif id == 0x12 : 
            return self.I2
        elif id == 0x13 : 
            return self.I3
        elif id == 0x14 : 
            return self.I4
        elif id == 0x15 : 
            return self.I5
        elif id == 0x16 : 
            return self.I6
        elif id == 0x17 : 
            return self.I7
        elif id == 0xFC : 
            return self.IE
        elif id == 0xFD : 
            return self.FR
        elif id == 0xFE : 
            return self.SP
        elif id == 0xFF : 
            return self.PC
        else :
            raise Exception("Unknown register " + str(id))

    def __MOV(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        value = self.__getRegisterValueById(sourceRegisterId)
        self.__setRegisterValueById(destinationRegisterId, value)

    def __SET(self):
        registerId = self.__fetchNextByteFromRom()
        constValue = self.__fetchNextByteFromRom()
        self.__setRegisterValueById(registerId, constValue)

    def __LOAD(self):
        pass
    def __STOR(self):
        pass
    def __ADD(self):
        pass
    def __SUB(self):
        pass
    def __MUL(self):
        pass
    def __DIV(self):
        pass
    def __MOD(self):
        pass
    def __OR(self):
        pass
    def __AND(self):
        pass
    def __XOR(self):
        pass
    def __NOT(self):
        pass
    def __SHL(self):
        pass
    def __SHR(self):
        pass
    def __CMP(self):
        pass
    def __JZ(self):
        pass
    def __JNZ(self):
        pass
    def __JC(self):
        pass
    def __JNC(self):
        pass
    def __JBE(self):
        pass
    def __JA(self):
        pass
    def __PUSH (self):
        pass
    def __POP(self):
        pass
    def __JMP(self):
        pass
    def __JMPR(self):
        pass
    def __CALL(self):
        pass 
    def __CALR(self):
        pass
    def __RET(self):
        pass
    def __HALT(self):
        self.running = False

    def run(self, programm):
        self.rom = programm
        self.running = True
        while self.running: 
            instruction = self.__fetchNextByteFromRom()
            print ("Executing: " + str(instruction))
            try:
                self.opcodeToHandlerMapping[instruction]() 
            except Exception as e: 
                print (e)
                raise Exception(e)
