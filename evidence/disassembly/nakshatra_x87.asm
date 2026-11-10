; ==============================================================================
; Jagannatha Hora Reverse Engineering - Disassembly Artifact
; Function: sub.calc_nakshatra_pada
; Target Address: 0x00454600
; Input:  [ebp + 8] = double lon_nirayana (0.0 <= lon < 360.0)
; Output: EAX = nakshatra (0..26), EDX = pada (1..4), [ebp - 8] = elapsed arc
; ==============================================================================

sub.calc_nakshatra_pada:
    push    ebp
    mov     ebp, esp
    sub     esp, 20

    ; Load Nirayana Longitude and divide by 13.333333333333334 degrees
    fld     qword [ebp + 8]
    fdiv    qword [0x0046b080]      ; ST(0) = lon / 13.333333333333334

    ; Set Rounding Control to Truncate (RC = 11b)
    fnstcw  word [ebp - 10]
    mov     ax, word [ebp - 10]
    or      ax, 0x0c00              ; Truncate mode
    mov     word [ebp - 12], ax
    fldcw   word [ebp - 12]

    ; Store integer Nakshatra index (0..26)
    fist    dword [ebp - 16]
    fldcw   word [ebp - 10]         ; Restore original control word

    ; Calculate elapsed arc within the nakshatra: lon - nak_idx * 13.333...
    fild    dword [ebp - 16]
    fmul    qword [0x0046b080]
    fld     qword [ebp + 8]
    fsubp   st(1), st(0)            ; ST(0) = elapsed_arc
    fst     qword [ebp - 8]         ; Store elapsed arc

    ; Divide by Pada Span (3.333333333333333)
    fdiv    qword [0x0046b088]
    fldcw   word [ebp - 12]         ; Truncate mode
    fistp   dword [ebp - 20]        ; Store pada index (0..3)
    fldcw   word [ebp - 10]         ; Restore control word
    fstp    st(0)                   ; Pop stack

    ; Return registers
    mov     eax, dword [ebp - 16]   ; EAX = nakshatra (0..26)
    mov     edx, dword [ebp - 20]
    inc     edx                     ; EDX = pada (1..4)

    mov     esp, ebp
    pop     ebp
    ret
