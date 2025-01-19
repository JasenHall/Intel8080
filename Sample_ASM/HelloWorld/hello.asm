;
; Name: hello.asm
;
; Date: 18th Jan 2025
;
; Purpose: Simple test of z80asm cross dev for CPM
;          Code will output string to console and end
;
        ORG 100H
BDOS    EQU     0005H  ; BDOS entry point
WSTR    EQU     0009H  ; BDOS output string
        MVI     C,WSTR
        LXI     D,MSG$
        CALL    BDOS
        RET     
MSG$:   DB      'Hello CPM World!$'
        END