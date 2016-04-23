start:
JMP main

test2:
HALT

test:
JMP test2

main:
SET R0, 1
JMP test
HALT

