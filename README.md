# Small and simple, pure virtual CPU.

## Rationale
The purpose of this project is to implement simple virtual machine, which is capable to run 
CPU specific machine code and compiler capable of assembling mnemonic code to machine one.
Project is written in Python 3. 

## Project parts
* [ ] CPU design - ongoing
* [ ] Virtual machine implementation
* [ ] Decompiler implementation
* [ ] Compiler implementation
* [ ] Example programs

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
╒══════════════════╕   In/Out Port   ╒══════════════════╕
│     Terminal     │ <-------------> │     Central      │
╘══════════════════╛                 │                  │
╒══════════════════╕   Memory bus    │                  │    Memory bus    ╒══════════════════╕
│Random Access Mem.│ <-------------> │    Processing    │  <-------------> │ Read Only Memory │
╘══════════════════╛                 │                  │                  ╘══════════════════╛
╒══════════════════╕ Interrupt line  │                  │
│Progammable timer │ <-------------> │       Unit       │
╘══════════════════╛                 ╘══════════════════╛
```
## Central Processing Unit Instruction Set Reference

+ RDST - destination register [R0 .. R7]
+ RSRC - source register      [R0 .. R7]
+ immv - immediate value (constant from machine code)
```
╒═══════════════╤═════════╤══════════════╤══════════════════════════════════╕
│ Instruction   │ OpCode  │ Operands     │ Description                      │
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
│                  Mathematical and logic operations                        │ 
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ ADD           │ 0x10    │ RDST, RSRC   │ Add value from RSRC to RDST and  │
│               │         │              │ store result in RDST             │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SUB           │ 0x11    │ RDST, RSRC   │ Subtract value of RSTC from RDST │
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
│               │         │              │                                  │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ SHR           │ 0x1A    │ RDST         │ Shift right bits in RDST         │
│               │         │              │                                  │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                   Comparisions and conditionals jumps                     │ 
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ CMP           │ 0x20    │ RDST, RSRC   │ Checks if substraction of RSRC   │
│               │         │              │ from RDST is equal 0. If yes it  │
│               │         │              │ sets ZF bit in FR register to 1, │
│               │         │              │ 0 otherwise. If substraction     │
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
│ JA            │ 0x26    │ immv         │ If CF is set increase and ZF is  │
│               │         │              │ not set increase PC of immv      │
│               │         │              │ (PC + immv mod 2^8).             │
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
│ JMP           │ 0x40    │ immv         │ Jump to addrres relative to immv.│
│               │         │              │ (PC + immv mod 2^8)              │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ JMR           │ 0x41    │ RSRC         │ Jump to addrres relative to addr │
│               │         │              │ in RSRC register.                │
│               │         │              │ (PC + RSRC mod 2^8)              │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ CALL          │ 0x42    │ immv         │ Calls function from address immv.│
│               │         │              │                                  │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ CALR          │ 0x43    │ RSRC         │ Calls function from address in   │
│               │         │              │ RSRC register.                   │
├───────────────┼─────────┼──────────────┼──────────────────────────────────┤
│ RET           │ 0x44    │ RSRC         │ Get return address from stack and│
│               │         │              │ jumps to it.                     │
├───────────────┴─────────┴──────────────┴──────────────────────────────────┤
│                              Stopping CPU                                 │ 
├───────────────┬─────────┬──────────────┬──────────────────────────────────┤
│ HLT           │ 0xFF    │              │ Stop executing further           │
│               │         │              │ instructions                     │
╘═══════════════╧═════════╧══════════════╧══════════════════════════════════╛

```