# 📦 Binary Manifest & Extraction Provenance
> **Referência Normativa:** [SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md](file:///home/sukata/jagannatha_hora_re/SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md#41-jh-re--de-dossiê-de-re-para-pacote-de-conformidade)

---

## 1. Perfil do Alvo Analisado

| Atributo | Valor / Especificação |
| :--- | :--- |
| **Aplicação** | Jagannatha Hora (JH) |
| **Autor Original** | P.V.R. Narasimha Rao |
| **Formato Binário** | PE32 (Portable Executable 32-bit x86 Intel) |
| **Compilador** | Borland C++ Builder 5.0 / 6.0 |
| **Subsystem** | Win32 GUI (`IMAGE_SUBSYSTEM_WINDOWS_GUI`) |
| **Framework de UI** | Borland Visual Component Library (VCL) |
| **Alinhamento de Memória** | `#pragma pack(4)` para estruturas VCL, `double` 8 bytes IEEE 754 |
| **FPU Default Control Word** | `0x137F` (64-bit precision, round-to-nearest) |
| **FPU Truncate Control Word**| `0x1F7F` (Round toward zero / Truncate para Nakshatra/Pada) |
| **Efemérides Embutidas** | Swiss Ephemeris (`sweph32.dll` / biblioteca estática C) |

---

## 2. Seções PE32 Mapeadas

```
Section     Virtual Address  Virtual Size  Raw Size    Flags
------------------------------------------------------------------
CODE        0x00401000       0x001B4000    0x001B4000  0x60000020 (RX)
DATA        0x005B5000       0x00028000    0x00018000  0xC0000040 (RW)
BSS         0x005DD000       0x00012000    0x00000000  0xC0000000 (RW)
.idata      0x005EF000       0x00005000    0x00005000  0x40000040 (R)
.tls        0x005F4000       0x00001000    0x00001000  0xC0000000 (RW)
.rsrc       0x005F5000       0x00042000    0x00042000  0x40000040 (R)
```

---

## 3. Disassembly Files no Repositório

- [evidence/disassembly/ayanamsa_x87.asm](file:///home/sukata/jagannatha_hora_re/evidence/disassembly/ayanamsa_x87.asm)
- [evidence/disassembly/nakshatra_x87.asm](file:///home/sukata/jagannatha_hora_re/evidence/disassembly/nakshatra_x87.asm)
- [evidence/disassembly/vcl_dispatch.asm](file:///home/sukata/jagannatha_hora_re/evidence/disassembly/vcl_dispatch.asm)
