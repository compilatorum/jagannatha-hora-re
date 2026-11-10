# 📑 Architecture Decision Records (ADR)
> **Referência Normativa:** [SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md](file:///home/sukata/jagannatha_hora_re/SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md#14-adrs-obrigatórios-antes-de-implementação)

Esta pasta documenta as decisões arquiteturais fundamentais tomadas antes da implementação do motor modernizado Astro-Observatory e da conformidade com o JH-RE.

---

## 📋 Catálogo de ADRs

| ADR | Título | Decisão Principal | Status |
| :--- | :--- | :--- | :---: |
| [**ADR-001**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-001-ephemeris-backend.md) | Seleção de Backend de Efemérides | Padrão Swiss Ephemeris (`pyswisseph`) sob AGPL/Comercial com fallback Moshier puro | **Aprovado** |
| [**ADR-002**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-002-cython-acceleration-policy.md) | Política de Uso de Cython 3.x | Python 3.12 como referência semântica; Cython apenas após profiling comprovado | **Aprovado** |
| [**ADR-003**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-003-time-scales-and-timezones.md) | Escalas de Tempo e Fusos Horários | UTC persistido com timezone IANA; $\Delta T$ explícito (TT = UT1 + $\Delta T$) | **Aprovado** |
| [**ADR-004**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-004-ayanamsha-models-and-epochs.md) | Modelos e Épocas de Ayanamsa | Lahiri Chitra Paksha (J2000), Raman, KP como enumerações estritas e versionadas | **Aprovado** |
| [**ADR-005**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-005-house-systems-cusp-sandhi.md) | Semântica de Cúspides, Madhyas e Sandhis | Separação estrita de campos; Placidus e Whole Sign prioritários | **Aprovado** |
| [**ADR-006**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-006-persistence-precision-numeric.md) | Tipagem Numérica e Persistência PostgreSQL | `DECIMAL(12, 7)` para coordenadas angulares; JSONB para metadados de execução | **Aprovado** |
| [**ADR-007**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-007-api-contracts-and-idempotency.md) | Contratos FastAPI e Idempotência | Pydantic v2 com UUIDv7 idempotente e OpenAPI gerado | **Aprovado** |
| [**ADR-008**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-008-frontend-architecture.md) | Frontend Next.js e Gráficos Vetoriais | TypeScript strict, Next.js App Router, renderização de mandalas em SVG puro | **Aprovado** |
| [**ADR-009**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-009-licensing-compliance.md) | Conformidade de Licenças | Compatibilidade de dependências e isolamento estrito de artefatos de RE | **Aprovado** |
| [**ADR-010**](file:///home/sukata/jagannatha_hora_re/docs/adr/ADR-010-jh-re-fixture-integration.md) | Integração de Fixtures JH-RE com o Observatório | Ingestão de fixtures JSON via suite de testes sem dependência direta de código | **Aprovado** |
