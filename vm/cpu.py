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
            0x44 : self.__RET }

    def _getidToRegisterMapping(self):
        return {
            0x00 : self.R0,
            0x01 : self.R1,
            0x02 : self.R2,
            0x03 : self.R3,
            0x04 : self.R4,
            0x05 : self.R5,
            0x06 : self.R6,
            0x07 : self.R7,
            0x10 : self.I0,
            0x11 : self.I1,
            0x12 : self.I2,
            0x13 : self.I3,
            0x14 : self.I4,
            0x15 : self.I5,
            0x16 : self.I6,
            0x17 : self.I7,
            0xFC : self.IE,
            0xFD : self.FR,
            0xFE : self.SP,
            0xFF : self.PC}
    
    def __init__(self, ram, rom, terminal):
        print ("Cpu created.")
        self.ram = ram
        self.rom = rom
        self.terminal = terminal
        self._initRegisters()
        self.opcodeToHandlerMapping = self._getOpcodeToHandlerMapping()
        self.idToRegisterMapping = self._getidToRegisterMapping()

    def __MOV(self):
        pass
    def __SET(self):
        pass
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


if __name__ == '__main__':
    cpu = Cpu("RAM","ROM","TERMINAL")