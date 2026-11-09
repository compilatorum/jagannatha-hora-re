#!/usr/bin/env python3
"""
Vimshottari Dasha State Machine & Calculation Engine
Reverse-engineered from Jagannatha Hora Win32 Borland C++ Binary
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import math
from typing import List, Dict, Any

GRAHAS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_DURATIONS = [7.0, 20.0, 6.0, 10.0, 7.0, 18.0, 16.0, 19.0, 17.0]
TOTAL_CYCLE_YEARS = 120.0
NAKSHATRA_SPAN = 360.0 / 27.0  # 13° 20' = 13.333333333333334°

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Moola", "Purvashadha", "Uttarashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

@dataclass
class DashaNode:
    level: int                        # 1: MD, 2: AD, 3: PD, 4: SD, 5: PAD
    lords: List[str]                  # Chain of lords, e.g. ["Saturn", "Mercury"]
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
            "duration_days": round(self.duration_days, 2),
            "subperiods": [c.to_dict() for c in self.children]
        }


class VimshottariDashaEngine:
    def __init__(self, days_per_year: float = 365.2425):
        self.days_per_year = days_per_year

    def calculate_birth_balance(self, moon_lon: float):
        """Calculates birth nakshatra, lord index, and unexpired fraction."""
        lon = moon_lon % 360.0
        nak_idx = int(math.floor(lon / NAKSHATRA_SPAN))
        nak_start = nak_idx * NAKSHATRA_SPAN
        elapsed_arc = lon - nak_start
        balance_fraction = 1.0 - (elapsed_arc / NAKSHATRA_SPAN)
        lord_idx = nak_idx % 9
        return nak_idx, lord_idx, balance_fraction

    def generate_timeline(self, birth_dt: datetime, moon_lon: float, max_depth: int = 2) -> List[DashaNode]:
        """
        Generates hierarchical Dasha timeline up to max_depth (1=MD, 2=AD, 3=PD, etc.).
        """
        nak_idx, birth_lord, balance_frac = self.calculate_birth_balance(moon_lon)
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


if __name__ == "__main__":
    engine = VimshottariDashaEngine()
    birth = datetime(1990, 8, 15, 14, 30, 0)
    moon_lon = 129.54  # Magha Nakshatra (Index 9, Ketu Lord)

    nak_idx, lord_idx, balance = engine.calculate_birth_balance(moon_lon)
    print("=" * 60)
    print(f"Janma Nakshatra: {NAKSHATRAS[nak_idx]} (Lord: {GRAHAS[lord_idx]})")
    print(f"Balance of First Dasha: {balance * 100:.2f}% remaining ({balance * DASHA_DURATIONS[lord_idx]:.2f} years)")
    print("=" * 60)

    timeline = engine.generate_timeline(birth, moon_lon, max_depth=2)
    print("\n--- Mahadasha & Antardasha Schedule ---")
    for md in timeline:
        print(f"🌟 MD: {md.label:<8} | Start: {md.start_time.strftime('%Y-%m-%d')} | End: {md.end_time.strftime('%Y-%m-%d')} | Span: {md.duration_years:5.2f} yrs")
        for ad in md.children:
            print(f"    ├─ AD: {ad.label:<16} | {ad.start_time.strftime('%Y-%m-%d')} -> {ad.end_time.strftime('%Y-%m-%d')} ({ad.duration_days:6.1f} d)")
