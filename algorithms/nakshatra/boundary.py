"""
Cálculo de limites de Nakshatra (13°20') e Pada (3°20').
Reconstrução fiel da rotina FPU x87 sub.calc_nakshatra_pada (0x00454600).
"""

import math
from typing import Tuple

NAKSHATRA_SPAN_DEG = 360.0 / 27.0   # 13° 20' = 13.333333333333334 graus (800')
PADA_SPAN_DEG = NAKSHATRA_SPAN_DEG / 4.0  # 3° 20' = 3.333333333333333 graus (200')
TOTAL_NAKSHATRAS = 27
TOTAL_PADAS = 108

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Moola", "Purvashadha", "Uttarashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


def calculate_nakshatra_pada(nirayana_lon_deg: float) -> Tuple[int, int, float, str]:
    """
    Calcula o índice de Nakshatra (0..26), o Pada (1..4) e a fração percorrida.
    
    Args:
        nirayana_lon_deg: Longitude sideral em graus [0.0, 360.0)
        
    Returns:
        Tuple contendo:
        - nakshatra_idx (int): 0 a 26
        - pada (int): 1 a 4
        - elapsed_fraction (float): Fração percorrida no nakshatra atual [0.0, 1.0)
        - nakshatra_name (str): Nome tradicional em sânscrito
    """
    # Normalização segura do ângulo
    lon = nirayana_lon_deg % 360.0
    if lon < 0.0:
        lon += 360.0

    # Truncamento idêntico à FPU x87 (RC = 11b / fistp)
    nakshatra_idx = int(math.floor(lon / NAKSHATRA_SPAN_DEG))
    if nakshatra_idx >= TOTAL_NAKSHATRAS:
        nakshatra_idx = TOTAL_NAKSHATRAS - 1

    # Arco percorrido dentro do nakshatra
    nak_start = nakshatra_idx * NAKSHATRA_SPAN_DEG
    elapsed_arc = lon - nak_start
    elapsed_fraction = elapsed_arc / NAKSHATRA_SPAN_DEG

    # Determinação do Pada (1..4)
    pada_idx = int(math.floor(elapsed_arc / PADA_SPAN_DEG))
    if pada_idx > 3:
        pada_idx = 3
    pada = pada_idx + 1

    return nakshatra_idx, pada, elapsed_fraction, NAKSHATRA_NAMES[nakshatra_idx]
