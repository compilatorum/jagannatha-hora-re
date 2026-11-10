# ⚠️ Registro de Discrepâncias e Limitações Conhecidas (JH-RE)
> **Referência Normativa:** [SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md](file:///home/sukata/jagannatha_hora_re/SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md#41-jh-re--de-dossiê-de-re-para-pacote-de-conformidade)

---

## 1. Discrepâncias Mapeadas entre o Binário Legado e Motores Modernos

| ID | Área | Comportamento Legado (Jagannatha Hora) | Comportamento Moderno / Observatório | Impacto / Mitigação |
| :--- | :--- | :--- | :--- | :--- |
| **DISC-01** | **Duração do Ano em Dashas** | Permite alternar entre Ano Solar Gregoriano (365,2425 dias), Ano Savana (360 dias) e Ano Sideral (365,2563 dias). | `VimshottariDashaEngine` aceita parâmetro explícito `days_per_year`. Padrão documentado: 365,2425 dias. | Declarar explicitamente a convenção em toda emissão de timeline. |
| **DISC-02** | **Cúspides Sripati vs Sandhis** | No cálculo de Bhava Chalita, cúspides representam *Bhava Madhyas* (centros de casa) e os *Sandhis* delimitam a fronteira entre casas adjacentes. | Separar em campos distintos na entidade `BhavaData` e no schema da API. Nunca colapsar cusp e sandhi num único campo. | Mantida separação estrita no modelo de domínio L2B. |
| **DISC-03** | **Precisão FPU x87 vs IEEE 754 de 64 bits** | O compilador Borland C++ Builder usa registradores estendidos x87 de 80 bits internamente, arredondando para 64 bits apenas no armazenamento em memória. | Python e Cython modernos utilizam 64 bits (double precision) com registradores SSE2/AVX. | Divergência observada na ordem de $10^{-11}$ graus (sub-miliarcsegundo), irrelevante para astrologia prática. |
| **DISC-04** | **Nós Lunares (Rahu/Ketu)** | Suporta Mean Node (nó médio) e True Node (nó verdadeiro osculante). | Ambos os modos são suportados via flag no adapter de efemérides. Ketu é rigorosamente $(\lambda_{\text{Rahu}} + 180^\circ) \pmod{360^\circ}$. | Expor `node_calc_mode` no `CalculationProfile`. |
| **DISC-05** | **Normalização de Ângulo em 360°** | Implementada via loop condicional `fprem1` com tratamento de resíduo negativo. | Normalização robusta com `fmod(deg, 360.0)` e correção positiva para $[0.0, 360.0)$. | Testes de fronteira em $0.0^\circ$, $360.0^\circ$, $-0.0001^\circ$ e $359.9999^\circ$. |
