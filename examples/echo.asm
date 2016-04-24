constants:
SET R2, 0x00; 0 constant

loop:
IN 0x01, R1 ; Read character
IN 0x00, R0 ; Read terminal flag
CMP R2, R0  ; Compare if more data is avalable
OUT 0x02, R1; Read character
JZ end
JMP loop

end:
SET R0, 10
OUT 0x02, R0
HALT

