BDOS:   EQU     5
WCONF:  EQU     2
        ORG:    100H
        MVI     C,WCONF
        MVI     E,'$'
        CALL    BDOS
        JMP     0
        END
