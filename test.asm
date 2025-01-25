;
; Name: hello.asm
;
; Date: 18th Jan 2025
;
; Purpose: Simple test of z80asm cross dev for CPM
;          Code will output string to console and end
;
        ORG 100H
MSG$:   DB      0CH,0DH,0AH,'Hello CPM World!$'
        END 