# Small and simple, pure Virtual Machine.
<p align="center">
  <img src="https://github.com/radx64/vm/blob/master/logo.png?raw=true" alt="Logo image" width="20%" height="20%"/>
</p>
## Rationale
The purpose of this project is to implement simple virtual machine, which is capable to run 
CPU specific machine code and compiler capable of assembling mnemonic code to machine one.
Project is written in Python 3. 

Travis status: 
[![Build Status](https://travis-ci.org/radx64/vm.svg?branch=master)](https://travis-ci.org/radx64/vm)

Coveralls status:
[![Coverage Status](https://coveralls.io/repos/github/radx64/vm/badge.svg?branch=master)](https://coveralls.io/github/radx64/vm?branch=master)

## Virtual Machine design
```
╒════════════════════════════════════════╤═══════════════════════════╕
│ Parameter                              │ Value                     │
╞════════════════════════════════════════╪═══════════════════════════╡
│ Architecture (word size, address bus)  │ 8 bit                     │
├────────────────────────────────────────┼───────────────────────────┤
│ Random Access Memory size              │ 256 words                 │
├────────────────────────────────────────┼───────────────────────────┤
│ Read Only Memory (Program memory)      │ 256 words                 │
├────────────────────────────────────────┼───────────────────────────┤
│ Registers set:                         │ 20 registers              │
│           general purpose registers    │ R0 .. R7                  │
│           program counter              │ PC                        │
│           stack pointer                │ SP                        │
│           flag register                │ FR                        │
│           interrupt registers          │ I0 .. I3 I4 .. I7         │
│           maskable interrupt enable    │ IE                        │
╘════════════════════════════════════════╧═══════════════════════════╛
```
As written above, architecture of CPU is 8 bit. As CPU address bus is connected to fragment 
of a memory it is able to directly address 256 cells of it, one byte each. General purpose
registers can be used by programmer. 

Program counter points to next CPU instruction that will be executed after current one (except 
situation when interrupt or jump is performed). CPU instructions are stored in ROM which 
is initialized before CPU start.

Stack pointer points to top of a stack in RAM (initially 0xFF address of memory) and stack grows in 
lower addresses direction.

Flag register holds information about current CPU state:
* ZF (zero flag) bit 0:
 - if 0 - result of last comparison is different than zero
 - if 1 - result of last comparison is zero
* CF (carry flag) bit 1:
 - if 0 - result of last comparison didn't lead to carry out
 - if 1 - otherwise 

## Virtual machine block diagram
```
                                     ╒══════════════════╕
                                     │     Central      │
                                     │                  │
╒══════════════════╕   Memory bus    │                  │    Memory bus    ╒══════════════════╕
│Random Access Mem.│ <-------------> │    Processing    │  <-------------> │  Program memory  │
╘══════════════════╛                 │                  │                  ╘══════════════════╛
╒══════════════════╕ Interrupt line  │                  │
│Progammable timer │ <-------------> │       Unit       │
╘══════════════════╛                 ╘══════════════════╛
         ^                                    │
         |        Configuration port          │
         ╘----------------------------------->│
                                             ╒═══╕
╒══════════════════╕         Data Port       │ I │
│     Terminal     │ <---------------------->│ / │
╘══════════════════╛        Control Port     │ O │
          .                                  │   │
          .                                  │ B │
          .                                  │ U │
    more devices                             │ S │
          .                                  ╘═══╛      
          .                                    │
          .                                    V
                                            
```
## Central Processing Unit Instruction Set Reference

+ RDST - destination register [R0 .. R7]
+ RSRC - source register      [R0 .. R7]
+ immv - immediate value (constant from machine code)
```
╒═══════════════╤═════════╤══════════════╤══════════════════════════════════╕
│  Instruction  │ OpCode  │   Operands   │           Description            │
╞═══════════════╧═════════╧══════════════╧══════════════════════════════════╡
│                         Memory Handling                                   │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ MOV           │ 0x00    │ RDST, RSRC   │ Copy data from RSRC to RDST      │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SET           │ 0x01    │ RDST, immv   │ Copy immv to RDST                │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ LOAD          │ 0x02    │ RDST, RSRC   │ Load data from memory at address │
│               │         │              │ pointed by RSRC to RDST register │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ STOR          │ 0x03    │ RDST, RSRC   │ Store data to memory at address  │
│               │         │              │ pointed by RDST from RSRC reg.   │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                    Mathematical and logic operations                      │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ ADD           │ 0x10    │ RDST, RSRC   │ Add value from RSRC to RDST and  │
│               │         │              │ store result in RDST             │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SUB           │ 0x11    │ RDST, RSRC   │ Subtract value of RSRC from RDST │
│               │         │              │ and store result in RDST         │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ MUL           │ 0x12    │ RDST, RSRC   │ Multiply value of RDST by RSRC   │
│               │         │              │ and store result in RDST         │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ DIV           │ 0x13    │ RDST, RSRC   │ Divide value of RDST by RSRC and │
│               │         │              │ store result in RDST             │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ MOD           │ 0x14    │ RDST, RSRC   │ Store reminder of division RDST  │
│               │         │              │ by RSRC in RDST                  │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ OR            │ 0x15    │ RDST, RSRC   │ Store result of logical OR       │
│               │         │              │ operation "RDST or RSRC" in RDST │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ AND           │ 0x16    │ RDST, RSRC   │ Store result of logical AND      │
│               │         │              │ operation "RDST and RSRC" in RDST│
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ XOR           │ 0x17    │ RDST, RSRC   │ Store result of logical XOR      │
│               │         │              │ operation "RDST xor RSRC" in RDST│
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ NOT           │ 0x18    │ RDST         │ Negate value stored in RDST      │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SHL           │ 0x19    │ RDST         │ Shift left bits in RDST          │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SHR           │ 0x1A    │ RDST         │ Shift right bits in RDST         │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                  Comparisons and conditionals jumps                       │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ CMP           │ 0x20    │ RDST, RSRC   │ Checks if subtraction of RSRC    │
│               │         │              │ from RDST is equal 0. If yes it  │
│               │         │              │ sets ZF bit in FR register to 1, │
│               │         │              │ 0 otherwise. If subtraction      │
│               │         │              │ gives negative value CF is set   │
│               │         │              │ to 1, otherwise 0.               │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JZ            │ 0x21    │ immv         │ If ZF is set increase PC of immv │
│               │         │              │ (PC + immv mod 2^8).             │
│               │         │              │ If ZF is not set do nothing      │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JNZ           │ 0x22    │ immv         │ If ZF is not set increase PC of  │
│               │         │              │ immv (PC + immv mod 2^8).        │
│               │         │              │ If ZF is set do nothing.         │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JC            │ 0x23    │ immv         │ If CF is set increase PC of immv │
│               │         │              │ (PC + immv mod 2^8).             │
│               │         │              │ If CF is not set do nothing.     │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JNC           │ 0x24    │ immv         │ If CF is not set increase PC of  │
│               │         │              │ immv (PC + immv mod 2^8).        │
│               │         │              │ If CF is not set do nothing.     │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JBE           │ 0x25    │ immv         │ If CF or ZF is set increase PC of│
│               │         │              │ immv (PC + immv mod 2^8).        │
│               │         │              │ Otherwise do nothing.            │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JA            │ 0x26    │ immv         │ If CF is set and ZF is not set   │
│               │         │              │ increase PC of immv (PC + immv   │
│               │         │              │ mod 2^8).                        │
│               │         │              │ Otherwise do nothing.            │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                            Stack handling                                 │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ PUSH          │ 0x30    │ RSRC         │ Push value from RSRC onto stack. │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ POP           │ 0x31    │ RDST         │ Pop value from stack to RDST.    │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                 Unconditional jumps and function calls                    │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ JMP           │ 0x40    │ immv         │ Jump to address relative to immv.│
│               │         │              │ (PC + immv mod 2^8)              │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JMPR          │ 0x41    │ RSRC         │ Jump to address absolute         │
│               │         │              │ in RSRC register.                │
│               │         │              │ (PC = RSRC)                      │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ CALL          │ 0x42    │ immv         │ Calls function relative to immv. │
│               │         │              │                                  │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ CALR          │ 0x43    │ RSRC         │ Calls function from address in   │
│               │         │              │ RSRC register.                   │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ RET           │ 0x44    │              │ Get return address from stack and│
│               │         │              │ jumps to it.                     │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                      Input / Output ports handling                        │
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ IN            │ 0x50    │ immv, RDST   │ Read value from port at address  │
│               │         │              │ immv to RDST register            │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ OUT           │ 0x51    │ immv, RSRC   │ Write value to port at address   │
│               │         │              │ immv from RSRC register          │ 
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                              Stopping CPU                                 │ 
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ HALT          │ 0xFF    │              │ Stop executing further           │
│               │         │              │ instructions                     │
╘═══════════════╧═════════╧══════════════╧══════════════════════════════════╛
 to be continued (no externals devices and interrupts support instructions)

```
## Central Processing Unit Registers Identifiers

```
 General registers       Interrupt registers    CPU operating registers
╒══════════╤══════╕      ╒══════════╤══════╕      ╒══════════╤══════╕
│ Register │ Id   │      │ Register │ Id   │      │ Register │ Id   │
╞══════════╪══════╡      ╞══════════╪══════╡      ╞══════════╪══════╡
│ R0       │ 0x00 │      │ I0       │ 0x10 │      │ IE       │ 0xFC │
├──────────┼──────┤      ├──────────┼──────┤      ├──────────┼──────┤
│ R1       │ 0x01 │      │ I1       │ 0x11 │      │ FR       │ 0xFD │ 
├──────────┼──────┤      ├──────────┼──────┤      ├──────────┼──────┤ 
│ R2       │ 0x02 │      │ I2       │ 0x12 │      │ SP       │ 0xFE │ 
├──────────┼──────┤      ├──────────┼──────┤      ├──────────┼──────┤
│ R3       │ 0x03 │      │ I3       │ 0x13 │      │ PC       │ 0xFF │
├──────────┼──────┤      ├──────────┼──────┤      ╘══════════╧══════╛
│ R4       │ 0x04 │      │ I4       │ 0x14 │     
├──────────┼──────┤      ├──────────┼──────┤     
│ R5       │ 0x05 │      │ I5       │ 0x15 │     
├──────────┼──────┤      ├──────────┼──────┤     
│ R6       │ 0x06 │      │ I6       │ 0x16 │     
├──────────┼──────┤      ├──────────┼──────┤     
│ R7       │ 0x07 │      │ I7       │ 0x17 │     
╘══════════╧══════╛      ╘══════════╧══════╛     

```

## Connected devices ports addresses

```
╒═══════════════════════╤═══════════╕
│ Device port           │ Address   │
╞═══════════════════════╪═══════════╡
│ Terminal control      │ 0x00      │ 
├───────────────────────┼───────────┤
│ Terminal data in      │ 0x01      │ 
├───────────────────────┼───────────┤ 
│ Terminal data out     │ 0x02      │
├───────────────────────┼───────────┤
│ PIT control           │ 0x03      │
╘═══════════════════════╧═══════════╛ 
```

## Terminal device usage

Terminal device is connected via I/O bus on addresses 0x00 - 0x02.

### Flags
Terminal control port:
* bit 0 - DATA_READY
* bits 1-7 are unused for now.

### Writing to terminal

To write character on terminal CPU need to send ASCII character byte to data out port(0x02). 

### Reading from terminal

Reading character operation should be done in two steps. First terminal control port(0x00) should 
be read to check if there is any character in buffer available. If flag DATA_READY (bit 0) is set, 
byte of data could be read from terminal data in port(0x01). Otherwise reading operation will be blocking,
causing processor to stop unitl new data is ready. 

### Interrupts from terminal
[[To be specified]]

## Running tests

In root directory of project just run:
``
nosetests
``

## To be done
- [ ] Interrupts
- [ ] More example programs
