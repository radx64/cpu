# Smal and simple, pure virtual CPU.

## Rationale
The purpose of this project is to implement simple virtual machine, which is capable to run 
cpu specific machine code and compiler capable of assembling mnemonic code to machine one.
Project is written in Python 3. 

## Project parts
* [ ] Cpu design
* [ ] Compiler implementation
* [ ] Virtual machine implementation
* [ ] Example programs

## Cpu design
```
╒════════════════════════════════════════╤═══════════════════════════╕
│ Parameter                              │ Value                     │
╞════════════════════════════════════════╪═══════════════════════════╡
│ Architecture (word size, address bus)  │ 8 bit                     │
├────────────────────────────────────────┼───────────────────────────┤
│ Registers set:                         │ 11 registers				 │
│           general purpose registers    │ R0 .. R7                  │
│           program counter              │ PC                        │
│           stack pointer                │ SP                        │
│           flag register                │ FR                        │
│           interrupt registers          │ I0 .. I3 I4 .. I7         │
│           maskable interrupt enable    │ IE                        │
╘════════════════════════════════════════╧═══════════════════════════╛
```
As written above, architecture of CPU is 8bit. As CPU address bus is connected to fragment 
of a memory it is able to directly address 256 cells of it, one byte each. General purpose
registers can be used by programmer. 
* Program counter points to next CPU instruction that will be executed after current one (except 
situation when interrupt or jump is performed). 
* Stack pointer points to top of a stack (initially 0xFF address) and stack grows in lower addresses direction.
* Flag register holds information about current CPU state:
 * ZF (zero flag) bit 0
  * if 0 - result of last comparision is different than zero
  * if 1 - result of last comparision is zero
 * CF (carry flag) bit 1
  * if 0 - result of last comparision didn't lead to carry out
  * if 1 - otherwise 

## Virtual machine design
```
[ONGOING]
```
## Central Processing Unit Instruction Set Reference
```
╒═══════════════╤═════════╤═════════════╕
|Instruction    │OpCode   │Description  │           
╘═══════════════╧═════════╧═════════════╛
```