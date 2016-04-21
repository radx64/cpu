; Simple program that prints 1337 on terminal

main: 
SET R0, 1
PUSH R0
CALL printdigit 
SET R0, 3
PUSH R0
CALL printdigit 
SET R0, 3
PUSH R0
CALL printdigit 
SET R0, 7
PUSH R0
CALL printdigit
CALL flushterminal
HALT

; functions
printdigit:
POP R7		; save return address in R7
POP R0		; get argument from stack to R0
SET R1, 48  ; constant of ASCII 0 character
ADD R0, R1  ; convert digit to ASCII
OUT 0x02, R0 ; print character
PUSH R7
RET

flushterminal:
SET R0, 10
OUT 0x02, R0 ; new line seq to flush terminal buffer
RET

