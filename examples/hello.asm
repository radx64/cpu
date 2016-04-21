; Simple program that prints only HELLO in terminal 
SET R0, 72
OUT 0x02, R0 ; H
SET R0, 69
OUT 0x02, R0 ; E
SET R0, 76
OUT 0x02, R0 ; L
OUT 0x02, R0 ; L
SET R0, 79
OUT 0x02, R0 ; O
SET R0, 10
OUT 0x02, R0 ; new line seq to flush terminal buffer

