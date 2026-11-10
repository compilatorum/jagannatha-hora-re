# ADR-002: Política de Uso de Cython 3.x
> **Status:** Aprovado  
> **Data:** 2026-11-09  
> **Contexto:** Política normativa para adoção de extensões compiladas em C/Cython.

---

## Decisão
1. **Python 3.12+ é a Referência Semântica:** Toda função matemática de cálculo possui implementação obrigatória em Python puro que serve de baseline e especificação executável.
2. **Cython Restrito a Gargalos Comprovados:** Módulos em Cython (`.pyx`) só serão introduzidos quando benchmarks identificarem gargalo CPU-bound mensurável (ex: varreduras de trânsitos em longos períodos ou busca de eclipses).
3. **Fallback Automático Obrigatório:** O sistema deve compilar e rodar 100% dos testes sem a extensão compilada disponível, garantindo desenvolvimento contínuo em ambientes sem toolchain C/C++.
4. **Isolamento de Tipos:** A extensão Cython nunca expõe ponteiros nativos C ou layouts de memória do executável original como contrato público.
