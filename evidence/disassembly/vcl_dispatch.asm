; ==============================================================================
; Jagannatha Hora Reverse Engineering - Disassembly Artifact
; Function: sym.TFormMain_btnCalculateClick
; Target Address: 0x00451A20
; Calling Convention: Borland __fastcall (EAX = this, EDX = Sender)
; ==============================================================================

sym.TFormMain_btnCalculateClick:
    push    ebp
    mov     ebp, esp
    push    ebx
    mov     ebx, eax                ; ebx = this (TFormMain*)

    ; Fetch text from Date edit box: this->edtBirthDate (offset +0x328)
    mov     eax, dword [ebx + 0x328]
    call    sym.TControl_GetText

    ; Fetch text from Time edit box: this->edtBirthTime (offset +0x32C)
    mov     edx, dword [ebx + 0x32c]
    mov     eax, edx
    call    sym.TControl_GetText

    ; Invoke Master Calculation Routine
    mov     eax, ebx                ; EAX = this
    call    sym.TFormMain_CalculateHoroscope

    pop     ebx
    pop     ebp
    ret
