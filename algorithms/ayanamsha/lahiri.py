"""
Cálculo de Ayanamsa Lahiri (Chitra Paksha).
Reconstrução fiel do bloco de montagem FPU x87 em sub.calc_ayanamsa_lahiri (0x004542B0).
"""

import math
from typing import Tuple

# Constantes IAU / Spica Chitra Paksha J2000.0
JD_J2000 = 2451545.0
DAYS_PER_JULIAN_CENTURY = 36525.0
LAHIRI_J2000_BASE_DEG = 23.85709166666667  # 23° 51' 25.53"

# Coeficientes polinomiais de precessão média (segundos de arco)
PRECESSION_C1 = 5029.0966
PRECESSION_C2 = 1.11113


def calculate_lahiri_ayanamsa(
    jd_ut: float,
    nutation_lon_deg: float = 0.0,
    obliquity_deg: float = 23.4392911
) -> float:
    """
    Calcula o Ayanamsa Lahiri para uma dada data juliana (UT).
    
    Args:
        jd_ut: Julian Date em Tempo Universal
        nutation_lon_deg: Nutação em longitude (opcional para Ayanamsa verdadeiro)
        obliquity_deg: Obliquidade da eclíptica em graus
        
    Returns:
        Ayanamsa em graus decimais.
    """
    # T em séculos julianos a partir de J2000.0
    t = (jd_ut - JD_J2000) / DAYS_PER_JULIAN_CENTURY

    # Avaliação do polinômio de precessão via método de Horner: (C2 * T + C1) * T
    precession_arcsec = (PRECESSION_C2 * t + PRECESSION_C1) * t
    precession_deg = precession_arcsec / 3600.0

    # Ayanamsa médio
    mean_ayanamsa = LAHIRI_J2000_BASE_DEG + precession_deg

    # Correção de nutação (Ayanamsa verdadeiro)
    if nutation_lon_deg != 0.0:
        nutation_correction = nutation_lon_deg * math.cos(math.radians(obliquity_deg))
        return mean_ayanamsa + nutation_correction

    return mean_ayanamsa


def normalize_angle_360(deg: float) -> float:
    """Normaliza qualquer ângulo para o intervalo semi-aberto [0.0, 360.0)."""
    norm = deg % 360.0
    if norm < 0.0:
        norm += 360.0
    return norm


def sayana_to_nirayana(sayana_lon: float, ayanamsa_deg: float) -> float:
    """Converte longitude tropical (Sayana) para sideral (Nirayana)."""
    return normalize_angle_360(sayana_lon - ayanamsa_deg)


def nirayana_to_sayana(nirayana_lon: float, ayanamsa_deg: float) -> float:
    """Converte longitude sideral (Nirayana) para tropical (Sayana)."""
    return normalize_angle_360(nirayana_lon + ayanamsa_deg)
