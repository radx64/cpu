class Cpu:    
    WORD_SIZE = 1 << 8
    CARRY_FLAG = 1 << 1
    ZERO_FLAG = 1 << 0

    available_registers = {
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7",
    "I0", "I1", "I2", "I3", "I4", "I5", "I6", "I7",
    "IE", "FR", "SP", "PC"
    }

    def _initRegisters(self):
        self.registers = {}
        for register in self.available_registers:
            self.registers[register] = 0;
        self.registers["SP"] = 0xFF   

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

    @staticmethod
    def __registerIdToName(registerId):
        registerIdToName = {
        0x00 : "R0",
        0x01 : "R1",
        0x02 : "R2",
        0x03 : "R3",
        0x04 : "R4",
        0x05 : "R5",
        0x06 : "R6",
        0x07 : "R7",
        0x10 : "I0",
        0x11 : "I1",
        0x12 : "I2",
        0x13 : "I3",
        0x14 : "I4",
        0x15 : "I5",
        0x16 : "I6",
        0x17 : "I7",
        0xFD : "FR",
        0xFE : "SP",
        0xFF : "PC",
        }
        try:
            return registerIdToName[registerId]
        except KeyError:
            raise Exception("Unknown register " + str(id))
    
    def __init__(self, ram, terminal):
        self.ram = ram
        self.rom = []
        self.running = False
        self.terminal = terminal
        self._initRegisters()
        self.opcodeToHandlerMapping = self._getOpcodeToHandlerMapping()

    def __fetchNextByteFromRom(self):
        byte = self.rom[self.registers["PC"]]
        self.registers["PC"] += 1
        return byte

    def __setRegisterValueById(self, id, value):
        print ("[DEBUG] Setting register {0}, with {1}".format(id,value))
        self.registers[self.__registerIdToName(id)] = value

    def __getRegisterValueById(self, id):
        print ("[DEBUG] Fetching register {0}".format(id))
        return self.registers[self.__registerIdToName(id)]

    def __validateAddress(self, address):
        if address >= len(self.ram) or address < 0:
            raise Exception ("Address 0x{0:02X} points outside memory "
                "address space (avail. 0x00-0x{1:02X})".format(address, len(self.ram)-1))    

    def __getMemoryValueAt(self, address):
        self.__validateAddress(address)
        return self.ram[address]

    def __setMemoryValueAt(self, address, value):
        self.__validateAddress(address)
        self.ram[address] = value

    def __setCarryFlag(self):
        self.registers["FR"] |= self.CARRY_FLAG

    def __clearCarryFlag(self):
        self.registers["FR"] &= (~self.CARRY_FLAG)

    def __setZeroFlag(self):
        self.registers["FR"] |= self.ZERO_FLAG

    def __clearZeroFlag(self):
        self.registers["FR"] &= (~self.ZERO_FLAG)

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
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        memoryAddress = self.__getRegisterValueById(sourceRegisterId)
        memoryValue = self.__getMemoryValueAt(memoryAddress)
        self.__setRegisterValueById(destinationRegisterId, memoryValue)

    def __STOR(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        memoryAddress = self.__getRegisterValueById(destinationRegisterId)
        memoryValue = self.__getRegisterValueById(sourceRegisterId)
        self.__setMemoryValueAt(memoryAddress, memoryValue)

    def __ADD(self):
        self.__clearCarryFlag()
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        if A + B >= self.WORD_SIZE:
            self.__setCarryFlag()
        result = (A + B) % self.WORD_SIZE
        self.__setRegisterValueById(destinationRegisterId, result)

    def __SUB(self):
        self.__clearCarryFlag()
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        result = B - A
        if result < 0:
            self.__setCarryFlag()
            result = self.WORD_SIZE - B
        self.__setRegisterValueById(destinationRegisterId, result)

    def __MUL(self):
        self.__clearCarryFlag()
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        if A * B >= self.WORD_SIZE:
            self.__setCarryFlag()
        result = (A * B) % self.WORD_SIZE
        self.__setRegisterValueById(destinationRegisterId, result)

    def __DIV(self):
        self.__clearCarryFlag()
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        if A == 0:
            raise Exception("Division by 0 error")
        result = B // A
        self.__setRegisterValueById(destinationRegisterId, result)

    def __MOD(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        if A == 0:
            raise Exception("Division by 0 error")
        result = B % A
        self.__setRegisterValueById(destinationRegisterId, result)

    def __OR(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        result = (B | A)
        self.__setRegisterValueById(destinationRegisterId, result)

    def __AND(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        result = (B & A)
        self.__setRegisterValueById(destinationRegisterId, result)

    def __XOR(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(sourceRegisterId)
        B = self.__getRegisterValueById(destinationRegisterId)
        result = (B ^ A)
        self.__setRegisterValueById(destinationRegisterId, result)

    def __NOT(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(destinationRegisterId)
        result = (~ A) % self.WORD_SIZE
        self.__setRegisterValueById(destinationRegisterId, result)

    def __SHL(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(destinationRegisterId)
        result = (A << 1) 
        if result >= self.WORD_SIZE :
            result %= self.WORD_SIZE
            self.__setCarryFlag()
        self.__setRegisterValueById(destinationRegisterId, result)

    def __SHR(self):
        destinationRegisterId = self.__fetchNextByteFromRom()
        A = self.__getRegisterValueById(destinationRegisterId)
        result = (A >> 1) 
        self.__setRegisterValueById(destinationRegisterId, result)
        
    def __CMP(self):
        self.__clearCarryFlag()
        self.__clearZeroFlag()
        destinationRegisterId = self.__fetchNextByteFromRom()
        sourceRegisterId = self.__fetchNextByteFromRom()
        B = self.__getRegisterValueById(destinationRegisterId)
        A = self.__getRegisterValueById(sourceRegisterId)
        result = B - A
        if result < 0:
            self.__setCarryFlag()
            result = self.WORD_SIZE - B
        elif result == 0:
            self.__setZeroFlag()
        self.__setRegisterValueById(destinationRegisterId, result)

    def __JZ(self):
        raise Exception("Not yet implemented instruction!")
    def __JNZ(self):
        raise Exception("Not yet implemented instruction!")
    def __JC(self):
        raise Exception("Not yet implemented instruction!")
    def __JNC(self):
        raise Exception("Not yet implemented instruction!")
    def __JBE(self):
        raise Exception("Not yet implemented instruction!")
    def __JA(self):
        raise Exception("Not yet implemented instruction!")
    def __PUSH (self):
        raise Exception("Not yet implemented instruction!")
    def __POP(self):
        raise Exception("Not yet implemented instruction!")
    def __JMP(self):
        raise Exception("Not yet implemented instruction!")
    def __JMPR(self):
        raise Exception("Not yet implemented instruction!")
    def __CALL(self):
        raise Exception("Not yet implemented instruction!") 
    def __CALR(self):
        raise Exception("Not yet implemented instruction!")
    def __RET(self):
        raise Exception("Not yet implemented instruction!")
    def __HALT(self):
        self.running = False

    def run(self, programm):
        self.registers["PC"] = 0
        self.rom = programm
        self.running = True
        while self.running: 
            instruction = self.__fetchNextByteFromRom()
            print ("[DEBUG] Executing instruction: 0x{0:02X}".format(instruction))
            try:
                self.opcodeToHandlerMapping[instruction]() 
            except Exception as e: 
                print (e)
                raise Exception(e)
