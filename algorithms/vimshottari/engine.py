"""
Máquina de estados e motor de cálculo de Vimshottari Dasha.
Reconstrução fiel das regras do Jagannatha Hora (Parashara Hora Shastra).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import math
from typing import List, Dict, Any, Tuple

GRAHAS: List[str] = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

DASHA_DURATIONS: List[float] = [
    7.0, 20.0, 6.0, 10.0, 7.0, 18.0, 16.0, 19.0, 17.0
]

TOTAL_CYCLE_YEARS: float = 120.0
NAKSHATRA_SPAN_DEG: float = 360.0 / 27.0  # 13.333333333333334°
DEFAULT_DAYS_PER_YEAR: float = 365.2425   # Ano solar médio gregoriano


@dataclass
class DashaNode:
    """Nó hierárquico representando um período (Mahadasha, Antardasha, etc.)."""
    level: int                        # 1: MD, 2: AD, 3: PD, 4: SD, 5: PAD
    lords: List[str]                  # Cadeia de regentes, ex: ["Saturn", "Mercury"]
    start_time: datetime
    end_time: datetime
    duration_days: float
    duration_years: float
    children: List['DashaNode'] = field(default_factory=list)

    @property
    def label(self) -> str:
        return "-".join(self.lords)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "period": self.label,
            "start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_days": round(self.duration_days, 4),
            "duration_years": round(self.duration_years, 4),
            "subperiods": [c.to_dict() for c in self.children]
        }


class VimshottariDashaEngine:
    """
    Motor determinístico de cálculo do sistema Vimshottari Dasha.
    """
    def __init__(self, days_per_year: float = DEFAULT_DAYS_PER_YEAR):
        self.days_per_year = days_per_year

    def calculate_birth_balance(self, moon_nirayana_lon: float) -> Tuple[int, int, float]:
        """
        Calcula o nakshatra natal, regente da primeira dasha e fração não expirada (*Bhogya*).
        
        Args:
            moon_nirayana_lon: Longitude sideral da Lua [0.0, 360.0)
            
        Returns:
            Tuple contendo: (nakshatra_index, birth_lord_index, balance_fraction_remaining)
        """
        lon = moon_nirayana_lon % 360.0
        if lon < 0.0:
            lon += 360.0

        nak_idx = int(math.floor(lon / NAKSHATRA_SPAN_DEG))
        if nak_idx >= 27:
            nak_idx = 26

        nak_start = nak_idx * NAKSHATRA_SPAN_DEG
        elapsed_arc = lon - nak_start
        fraction_remaining = 1.0 - (elapsed_arc / NAKSHATRA_SPAN_DEG)
        lord_idx = nak_idx % 9

        return nak_idx, lord_idx, fraction_remaining

    def generate_timeline(
        self,
        birth_dt: datetime,
        moon_nirayana_lon: float,
        max_depth: int = 2
    ) -> List[DashaNode]:
        """
        Gera a linha do tempo hierárquica das Mahadashas e subperíodos recursivos.
        
        Args:
            birth_dt: Instante de nascimento (UTC recomendado)
            moon_nirayana_lon: Longitude sideral da Lua
            max_depth: Nível máximo de subdivisão (1=MD, 2=AD, 3=PD, 4=SD, 5=PAD)
        """
        if max_depth < 1:
            raise ValueError("max_depth deve ser pelo menos 1")
        if max_depth > 5:
            raise ValueError("max_depth suportado até 5 (Prana Dasha)")

        nak_idx, birth_lord, balance_frac = self.calculate_birth_balance(moon_nirayana_lon)
        current_dt = birth_dt
        mahadashas: List[DashaNode] = []

        for i in range(9):
            lord_idx = (birth_lord + i) % 9
            full_years = DASHA_DURATIONS[lord_idx]
            actual_years = (full_years * balance_frac) if i == 0 else full_years
            span_days = actual_years * self.days_per_year
            end_dt = current_dt + timedelta(days=span_days)

            node = DashaNode(
                level=1,
                lords=[GRAHAS[lord_idx]],
                start_time=current_dt,
                end_time=end_dt,
                duration_days=span_days,
                duration_years=actual_years
            )

            if max_depth >= 2:
                self._subdivide(node, max_depth)

            mahadashas.append(node)
            current_dt = end_dt

        return mahadashas

    def _subdivide(self, parent: DashaNode, max_depth: int):
        if parent.level >= max_depth:
            return

        parent_lord_idx = GRAHAS.index(parent.lords[-1])
        current_dt = parent.start_time
        total_days = parent.duration_days

        for i in range(9):
            child_lord_idx = (parent_lord_idx + i) % 9
            fraction = DASHA_DURATIONS[child_lord_idx] / TOTAL_CYCLE_YEARS
            child_days = total_days * fraction
            end_dt = current_dt + timedelta(days=child_days)

            child = DashaNode(
                level=parent.level + 1,
                lords=parent.lords + [GRAHAS[child_lord_idx]],
                start_time=current_dt,
                end_time=end_dt,
                duration_days=child_days,
                duration_years=child_days / self.days_per_year
            )

            if child.level < max_depth:
                self._subdivide(child, max_depth)

            parent.children.append(child)
            current_dt = end_dt
