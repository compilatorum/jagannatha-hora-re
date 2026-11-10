# 💾 Borland C++ Builder 5/6 Memory Layout & Offsets
> **Referência Normativa:** [SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md](file:///home/sukata/jagannatha_hora_re/SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md#41-jh-re--de-dossiê-de-re-para-pacote-de-conformidade)

---

## 1. `GrahaData` Offset Table (Tamanho: 88 bytes / `0x58`)

| Offset (Hex) | Tipo | Tamanho | Membro | Descrição |
| :--- | :--- | :---: | :--- | :--- |
| `+0x00` | `int32_t` | 4B | `graha_id` | Identificador do planeta (0..12) |
| `+0x04` | `int32_t` | 4B | `rasi` | Signo zodiacal (0..11) |
| `+0x08` | `double` | 8B | `lon_nirayana` | Longitude sideral (graus decimais) |
| `+0x10` | `double` | 8B | `lon_sayana` | Longitude tropical (graus decimais) |
| `+0x18` | `double` | 8B | `lat` | Latitude eclíptica |
| `+0x20` | `double` | 8B | `speed_lon` | Movimento diário em longitude |
| `+0x28` | `double` | 8B | `speed_lat` | Movimento diário em latitude |
| `+0x30` | `double` | 8B | `dist_au` | Distância geocêntrica em UA |
| `+0x38` | `double` | 8B | `speed_dist` | Variação radial da distância |
| `+0x40` | `int32_t` | 4B | `nakshatra` | Índice do Nakshatra (0..26) |
| `+0x44` | `int32_t` | 4B | `pada` | Quarto do Nakshatra (1..4) |
| `+0x48` | `double` | 8B | `nak_elapsed` | Fração percorrida no Nakshatra [0.0..1.0] |
| `+0x50` | `uint32_t`| 4B | `flags` | Bitmask de status (Retrograde, Combust, etc.) |
| `+0x54` | `int32_t` | 4B | `dignity` | Dignidade do planeta (0=Exaltado..8=Debilitado) |

---

## 2. `BhavaData` Offset Table (Tamanho: 328 bytes / `0x148`)

| Offset (Hex) | Tipo | Tamanho | Membro | Descrição |
| :--- | :--- | :---: | :--- | :--- |
| `+0x00` | `int32_t` | 4B | `house_system` | Sistema de casas (0=Equal, 1=Sripati, 2=Placidus) |
| `+0x04` | `int32_t` | 4B | `lagna_rasi` | Signo do Ascendente |
| `+0x08` | `double` | 8B | `ascendant_lon` | Longitude do Ascendente |
| `+0x10` | `double` | 8B | `mc_lon` | Longitude do Meio do Céu (MC) |
| `+0x18` | `double` | 8B | `armc` | Tempo Sideral / ARMC |
| `+0x20` | `double` | 8B | `vertex_lon` | Longitude do Vertex |
| `+0x28` | `double[12]` | 96B | `cusps` | Longitudes das 12 cúspides / Bhava Madhyas |
| `+0x88` | `double[12]` | 96B | `sandhis` | Pontos de junção entre casas adjacentes |
| `+0xE8` | `int32_t[12]`| 48B | `cusp_rasi` | Signos ocupados pelas 12 cúspides |
| `+0x118`| `int32_t[12]`| 48B | `cusp_nakshatra`| Nakshatras ocupados pelas 12 cúspides |
