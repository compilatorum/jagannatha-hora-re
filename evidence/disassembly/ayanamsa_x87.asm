; ==============================================================================
; Jagannatha Hora Reverse Engineering - Disassembly Artifact
; Function: sub.calc_ayanamsa_lahiri
; Target Address: 0x004542B0
; Calling Convention: cdecl / returns result in ST(0)
; ==============================================================================

sub.calc_ayanamsa_lahiri:
    push    ebp
    mov     ebp, esp
    sub     esp, 16                 ; local storage for T and nutation

    ; Compute T = (JD - 2451545.0) / 36525.0
    fld     qword [ebp + 8]         ; ST(0) = Julian Day UT
    fsub    qword [0x0046b040]      ; ST(0) = JD - 2451545.0 (Days since J2000.0)
    fdiv    qword [0x0046b048]      ; ST(0) = T (Julian centuries)
    fst     qword [ebp - 8]         ; store T, keep ST(0)

    ; Polynomial: (1.11113 * T + 5029.0966) * T
    fmul    qword [0x0046b050]      ; ST(0) = T * 1.11113
    fadd    qword [0x0046b058]      ; ST(0) = 1.11113*T + 5029.0966
    fmul    qword [ebp - 8]         ; ST(0) = Precession arcsec
    fdiv    qword [0x0046b060]      ; ST(0) = Precession in degrees (/ 3600.0)

    ; Add base J2000 Lahiri Ayanamsa (23.857091666667 deg = 23° 51' 25.53")
    fadd    qword [0x0046b068]      ; ST(0) = Mean Ayanamsa degrees

    ; Nutation in longitude correction: delta_psi * cos(eps)
    fld     qword [ebp - 16]        ; ST(0) = delta_psi, ST(1) = Mean Ayanamsa
    fmul    qword [0x0046b070]      ; ST(0) = delta_psi * cos(eps)
    faddp   st(1), st(0)            ; ST(0) = True Ayanamsa degrees

    mov     esp, ebp
    pop     ebp
    ret
