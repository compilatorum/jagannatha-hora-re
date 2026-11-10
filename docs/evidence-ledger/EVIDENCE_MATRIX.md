# 📋 Matriz de Cobertura e Ledger de Evidências (JH-RE)
> **Referência Normativa:** [SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md](file:///home/sukata/jagannatha_hora_re/SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md#41-jh-re--de-dossiê-de-re-para-pacote-de-conformidade)  
> **Classificação de Evidências:**  
> - **E0** — Hipótese ou inferência arquitetural não comprovada  
> - **E1** — Evidência documental / manual / literatura externa  
> - **E2** — Evidência direta do binário (disassembly, dumps de memória, xrefs, VMT)  
> - **E3** — Reprodução independente executável  
> - **E4** — Validação diferencial contra saídas de referência (golden datasets)

---

## 1. Matriz de Rastreabilidade: Algoritmo × Evidência × Implementação × Teste

| ID | Componente / Afirmação | Nível | Evidência de Origem (Binário / Dossiê) | Implementação | Teste Automatizado | Status |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **ALG-01** | `GrahaData` Memory Layout (0x58 bytes por graha) | **E2** | Borland x86 stack layout, `imul eax, edi, 0x58` em `sub.calc_all_grahas` | [`GrahaData`](file:///home/sukata/jagannatha_hora_re/01_MEMORY_LAYOUT_AND_STRUCTS.md#24-c-reconstructed-definition) | [`test_memory_layout.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_memory_layout.py) | ✅ Validado |
| **ALG-02** | `BhavaData` Memory Layout (0x148 bytes, 12 cusps + 12 sandhis) | **E2** | VMT dispatch `TFormMain::CalculateHoroscope`, offsets `+0x28`, `+0x88` | [`BhavaData`](file:///home/sukata/jagannatha_hora_re/01_MEMORY_LAYOUT_AND_STRUCTS.md#32-c-definition--house-systems) | [`test_bhavas.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_bhavas.py) | ✅ Validado |
| **ALG-03** | `VargaFactors` Projeção Harmônica D-1 a D-60 | **E1/E3** | BPHS Shodashavarga formalisms + offsets de loop varga no binário | [`VargaEntry`](file:///home/sukata/jagannatha_hora_re/01_MEMORY_LAYOUT_AND_STRUCTS.md#43-c-definition) | [`test_vargas.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_vargas.py) | ⚠️ Parcial (D1, D9, D10) |
| **ALG-04** | Ayanamsa Lahiri / Chitra Paksha Polinômio FPU x87 | **E2/E3** | Rotina FPU `sub.calc_ayanamsa_lahiri` (`0x004542B0`), constantes IAU | [`algorithms/ayanamsha/lahiri.py`](file:///home/sukata/jagannatha_hora_re/algorithms/ayanamsha/lahiri.py) | [`test_ayanamsha.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_ayanamsha.py) | ✅ Validado (E3) |
| **ALG-05** | Nakshatra (13°20') & Pada (3°20') com FPU Truncate CW `0x1F7F` | **E2/E3** | Rotina FPU `sub.calc_nakshatra_pada` (`0x00454600`) | [`algorithms/nakshatra/boundary.py`](file:///home/sukata/jagannatha_hora_re/algorithms/nakshatra/boundary.py) | [`test_nakshatra.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_nakshatra.py) | ✅ Validado (E3) |
| **ALG-06** | Vimshottari Dasha Balanço Inicial (*Bhukta/Bhogya*) | **E2/E4** | Offset de cálculo da Lua `GrahaData[1].lon_nirayana`, ciclo de 120 anos | [`algorithms/vimshottari/engine.py`](file:///home/sukata/jagannatha_hora_re/algorithms/vimshottari/engine.py) | [`test_vimshottari.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_vimshottari.py) | ✅ Validado (E4) |
| **ALG-07** | Vimshottari Subdivisões Multinível (MD, AD, PD, SD, PAD) | **E3/E4** | Regra recursiva $D_{child} = D_{parent} \times \frac{L_{child}}{120}$ | [`VimshottariDashaEngine`](file:///home/sukata/jagannatha_hora_re/algorithms/vimshottari/engine.py) | [`test_vimshottari.py`](file:///home/sukata/jagannatha_hora_re/tests/unit/test_vimshottari.py) | ✅ Validado (E4) |
| **ALG-08** | Integração Swiss Ephemeris (`sweph32.dll`) | **E2** | Imports `_swe_calc_ut`, `_swe_houses`, `_swe_get_ayanamsa_ut` | Adapter especificado em L0 | [`test_conformance.py`](file:///home/sukata/jagannatha_hora_re/tests/conformance/test_conformance.py) | ⏳ Em conformidade |

---

## 2. Ledger de Artefatos e Endereços Desmontados

| Símbolo Desmontado | Endereço Base Virtual | Seção PE | Calling Convention | Descrição da Função |
| :--- | :---: | :---: | :--- | :--- |
| `sym.TFormMain_btnCalculateClick` | `0x00451A20` | `CODE` | Borland `__fastcall` | Disparo VCL da UI ao clicar no botão de cálculo |
| `sym.TFormMain_CalculateHoroscope` | `0x00451F80` | `CODE` | Borland `__fastcall` | Orquestrador master em 8 estágios |
| `sub.calc_all_grahas` | `0x00453100` | `CODE` | cdecl interno | Loop de chamada a `_swe_calc_ut` para Grahas 0..11 |
| `sub.calc_ayanamsa_lahiri` | `0x004542B0` | `CODE` | cdecl / x87 return | Avaliação polinomial da precessão + nutação em `ST(0)` |
| `sub.calc_nakshatra_pada` | `0x00454600` | `CODE` | register return | Divisão angular com `fldcw 0x1F7F` e extração de Pada |

---

## 3. Diretrizes de Governança
1. **Regra de Não-Promoção Silenciosa:** Nenhuma hipótese classificada como `E0` ou `E1` pode ser promovida para `E3`/`E4` sem testes automatizados que usem dados de referência externos verificáveis.
2. **Isolamento de Runtime:** O código de produção nunca importará estruturas diretamente de dumps binários, garantindo independência de plataforma (Linux/macOS/OCI).
