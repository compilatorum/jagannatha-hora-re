"""
Módulo de cálculo de Nakshatras e Padas.
"""
from .boundary import (
    calculate_nakshatra_pada,
    NAKSHATRA_NAMES,
    NAKSHATRA_SPAN_DEG,
    PADA_SPAN_DEG,
    TOTAL_NAKSHATRAS,
    TOTAL_PADAS,
)

__all__ = [
    "calculate_nakshatra_pada",
    "NAKSHATRA_NAMES",
    "NAKSHATRA_SPAN_DEG",
    "PADA_SPAN_DEG",
    "TOTAL_NAKSHATRAS",
    "TOTAL_PADAS",
]
