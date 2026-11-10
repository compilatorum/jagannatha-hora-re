# ADR-001: Seleção de Backend de Efemérides
> **Status:** Aprovado  
> **Data:** 2026-11-09  
> **Contexto:** Necessidade de cálculo astronômico com alta precisão sem depender de binários legados do Windows.

---

## Decisão
1. **Backend Primário:** Swiss Ephemeris (`pyswisseph` / C library wrapper), acessado exclusivamente por um `EphemerisAdapter` agnóstico de fornecedor.
2. **Licenciamento:** O uso será em conformidade com GNU AGPL v3 (para projetos open-source) ou licença comercial profissional caso haja distribuição fechada.
3. **Backend Secundário / Fallback:** Moshier Ephemeris puro em Python/C para ambientes que não puderem vincular a biblioteca C do Swiss Ephemeris.
4. **Transparência de Provedor:** A API e as entidades do banco registrarão obrigatoriamente `ephemeris_provider` e `provider_version` em cada cálculo. Fallback silencioso é terminantemente proibido.
