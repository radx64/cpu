import unittest
from vm.cpu import Cpu
from vm.port import Port
from unittest.mock import Mock

class TerminalFake:
    def __init__(self):
        self.controlPort = Port(None, None)
        self.dataInPort  = Port(None, None)
        self.dataOutPort = Port(None, None)

class CpuTests(unittest.TestCase):
    def __init__(self, parameters):
        unittest.TestCase.__init__(self, parameters)
        self.ram = [0x00] * 256;    # so much blocks of memory :)
        self.terminal = TerminalFake()
        self.cpu = Cpu(self.ram, self.terminal, True)

    def test_IfCpuGeneralRegistersHaveCorrectValuesAtFirstBoot(self):
        self.assertEquals(self.cpu.registers["R0"], 0x00)
        self.assertEquals(self.cpu.registers["R1"], 0x00)
        self.assertEquals(self.cpu.registers["R2"], 0x00)
        self.assertEquals(self.cpu.registers["R3"], 0x00)
        self.assertEquals(self.cpu.registers["R4"], 0x00)
        self.assertEquals(self.cpu.registers["R5"], 0x00)
        self.assertEquals(self.cpu.registers["R6"], 0x00)
        self.assertEquals(self.cpu.registers["R7"], 0x00)

    def test_IfCpuInterruptRegistersHaveCorrectValuesAtBoot(self):
        self.assertEquals(self.cpu.registers["I0"], 0x00)
        self.assertEquals(self.cpu.registers["I1"], 0x00)
        self.assertEquals(self.cpu.registers["I2"], 0x00)
        self.assertEquals(self.cpu.registers["I3"], 0x00)
        self.assertEquals(self.cpu.registers["I4"], 0x00)
        self.assertEquals(self.cpu.registers["I5"], 0x00)
        self.assertEquals(self.cpu.registers["I6"], 0x00)
        self.assertEquals(self.cpu.registers["I7"], 0x00)

    def test_IfCpuInterruptEnableRegisterHaveCorrectValueAtBoot(self):
        self.assertEquals(self.cpu.registers["IE"], 0x00)

    def test_IfCpuFlagRegisterHaveCorrectValueAtBoot(self):
        self.assertEquals(self.cpu.registers["FR"], 0x00)

    def test_IfCpuStackPointerRegisterHaveCorrectValueAtBoot(self):
        self.assertEquals(self.cpu.registers["SP"], 0xFF)

    def test_IfCpuProgamCounterHaveCorrectValueAtBoot(self):
        self.assertEquals(self.cpu.registers["PC"], 0x00)

    def test_IfSourceRegisterDecodingThrowsException(self):
        program = [0x00,0x00,0xAA]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_IfDestinationRegisterDecodingThrowsException(self):
        program = [0x00,0xAA,0x00]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_IfMemoryAddressingThrowExceptionForStrageAddressSpaceAccess(self):
        self.cpu.registers["R0"] = -0xFF
        program = [0x02, 0x01, 0x00, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_MOV_instructionHandling(self):
        self.cpu.registers["R0"] = 0xAB
        program = [0x00, 0x01, 0x00, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R1"], 0xAB)

    def test_SET_instructionHandling(self):
        program = [0x01, 0x00, 0xAB, 0xFF]
        self.cpu.run(program);
        self.assertEquals(self.cpu.registers["R0"], 0xAB)

    def test_LOAD_instructionHandling(self):
        self.ram[0xFF] = 0xAB
        self.cpu.registers["R0"] = 0xFF
        program = [0x02, 0x01, 0x00, 0xFF]
        self.cpu.run(program);
        self.assertEquals(self.cpu.registers["R1"], 0xAB)

    def test_STOR_instructionHandling(self):
        self.cpu.registers["R0"] = 0xAB
        self.cpu.registers["R1"] = 0xFF
        program = [0x03, 0x01, 0x00, 0xFF]
        self.cpu.run(program);
        self.assertEquals(self.ram[0xFF], 0xAB)

    def test_ADD_instructionHandling(self):
        self.cpu.registers["R0"] = 0x01
        self.cpu.registers["R1"] = 0x02
        program = [0x10, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x03)

    def test_ADD_instructionHandlingCarryFlag(self):
        self.cpu.registers["R0"] = 0x01
        self.cpu.registers["R1"] = 0xFF
        program = [0x10, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x00)
        self.assertEquals(self.cpu.registers["FR"], 0x02)  # carry bit set

    def test_SUB_instructionHandling(self):
        self.cpu.registers["R0"] = 0x02
        self.cpu.registers["R1"] = 0x01
        program = [0x11, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x01)

    def test_SUB_instructionHandlingCarryFlag(self):
        self.cpu.registers["R0"] = 0x01
        self.cpu.registers["R1"] = 0x02
        program = [0x11, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0xFF)
        self.assertEquals(self.cpu.registers["FR"], 0x02)  # carry bit set

    def test_MUL_instructionHandling(self):
        self.cpu.registers["R0"] = 0x02
        self.cpu.registers["R1"] = 0x03
        program = [0x12, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x06)

    def test_MUL_instructionHandlingCarryFlag(self):
        self.cpu.registers["R0"] = 0xFF
        self.cpu.registers["R1"] = 0x02
        program = [0x12, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0xFE)
        self.assertEquals(self.cpu.registers["FR"], 0x02)  # carry bit set

    def test_DIV_instructionHandling(self):
        self.cpu.registers["R0"] = 0x06
        self.cpu.registers["R1"] = 0x02
        program = [0x13, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x03)

    def test_DIV_instructionHandlingThrowsWhenDividingBy0(self):
        self.cpu.registers["R0"] = 0x06
        self.cpu.registers["R1"] = 0x00
        program = [0x13, 0x00, 0x01, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_MOD_instructionHandling(self):
        self.cpu.registers["R0"] = 0x07
        self.cpu.registers["R1"] = 0x02
        program = [0x14, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x01)

    def test_MOD_instructionHandlingThrowsWhenDividingBy0(self):
        self.cpu.registers["R0"] = 0x06
        self.cpu.registers["R1"] = 0x00
        program = [0x14, 0x00, 0x01, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_OR_instructionHandling(self):
        self.cpu.registers["R0"] = 0x02
        self.cpu.registers["R1"] = 0x01
        program = [0x15, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x03)

    def test_AND_instructionHandling(self):
        self.cpu.registers["R0"] = 0x02
        self.cpu.registers["R1"] = 0x01
        program = [0x16, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x00)

    def test_XOR_instructionHandling(self):
        self.cpu.registers["R0"] = 0x03
        self.cpu.registers["R1"] = 0x01
        program = [0x17, 0x00, 0x01, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x02)

    def test_NOT_instructionHandling(self):
        self.cpu.registers["R0"] = 0xAA
        program = [0x18, 0x00, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x55)

    def test_SHL_instructionHandling(self):
        self.cpu.registers["R0"] = 0x01
        program = [0x19, 0x00, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x02)

    def test_SHL_instructionHandlingCarryFlag(self):
        self.cpu.registers["R0"] = 0xFF
        program = [0x19, 0x00, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0xFE)
        self.assertEquals(self.cpu.registers["FR"], 0x02)  # carry bit set

    def test_SHR_instructionHandling(self):
        self.cpu.registers["R0"] = 0x04
        program = [0x1A, 0x00, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x02)

    def test_HALT_instructionHandling(self):
        program = [0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x01)

    def test_CMP_instructionHandlingZF(self):
        program = [0x20, 0x00, 0x01, 0xFF]
        self.cpu.registers["R0"] = 0x2
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["FR"] & 0x01, 0x00)

        program = [0x20, 0x00, 0x01, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["FR"] & 0x01, 0x01)

    def test_CMP_instructionHandlingCF(self):
        program = [0x20, 0x00, 0x01, 0xFF]
        self.cpu.registers["R0"] = 0x2
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["FR"] & 0x02, 0x00)

        program = [0x20, 0x00, 0x01, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x2
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["FR"] & 0x02, 0x02)    

    def test_JZ_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x21, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

    def test_JNZ_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x22, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x2
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

    def test_JC_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x23, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x2
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

    def test_JNC_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x24, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

    def test_JBE_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x25, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x1
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

        program = [0x20, 0x00, 0x01, 0x25, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x2
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)       

    def test_JA_instructionHandling(self):
        program = [0x20, 0x00, 0x01, 0x26, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x1
        self.cpu.registers["R1"] = 0x2
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)

    def test_PUSH_instructionHandling(self):
        program = [0x30, 0x00, 0xFF]
        self.cpu.registers["R0"] = 0xAB
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["SP"], 0xFE)
        self.assertEquals(self.cpu.ram[0xFE], 0xAB)

    def test_PUSH_instructionHandlingThrowsWhenNoMoreSpace(self):
        program = [0x30, 0x00, 0xFF]
        self.cpu.registers["SP"] = 0x00
        self.assertRaises(Exception, self.cpu.run, program)    

    def test_POP_instructionHandling(self):
        program = [0x31, 0x00, 0xFF]
        self.cpu.ram[0xFE] = 0xAB
        self.cpu.registers["SP"] = 0xFE
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0xAB)
        self.assertEquals(self.cpu.registers["SP"], 0xFF)

    def test_POP_instructionHandlingThrowsWhenNothingMoreToPop(self):
        program = [0x31, 0x00, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_JMP_instructionHandling(self):
        program = [0x40, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x06)

    def test_JMPR_instructionHandling(self):
        program = [0x41, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x03
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x04)

    def test_CALL_instuctionHandling(self):
        program = [0x42, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x07)
        self.assertEquals(self.cpu.ram[0xFE], 0x02)

    def test_CALR_instuctionHandling(self):
        program = [0x43, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["R0"] = 0x04
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x05)
        self.assertEquals(self.cpu.ram[0xFE], 0x02)

    def test_RET_instructionHandling(self):
        program = [0x44, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.cpu.registers["SP"] = 0xFE
        self.cpu.ram[0xFE] = 0x02
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["PC"], 0x03)

    def test_IN_instructionHandling(self):
        program = [0x50, 0x01, 0x00, 0xFF]
        self.cpu.terminal.dataInPort.read = Mock(return_value=0x12)
        self.cpu.run(program)
        self.assertEquals(self.cpu.registers["R0"], 0x12)

    def test_IN_instructionHandlingRaisesWhenNoDeviceAvailable(self):
        program = [0x50, 0x99, 0x00, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)

    def test_OUT_instructionHandling(self):
        program = [0x51, 0x02, 0x00, 0xFF]
        self.cpu.registers["R0"] = 0x12
        self.cpu.terminal.dataOutPort.write = Mock()
        self.cpu.run(program)
        self.cpu.terminal.dataOutPort.write.assert_called_with(0x12)

    def test_OUT_instructionHandlingRaisesWhenNoDeviceAvailable(self):
        program = [0x51, 0x99, 0x00, 0xFF]
        self.assertRaises(Exception, self.cpu.run, program)