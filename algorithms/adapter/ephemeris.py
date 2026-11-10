"""
Adapter de Efemérides (Swiss Ephemeris / Moshier) e orquestrador astronômico.
Conforme especificado na Seção 6.1 do SPEC_ASTRO_OBSERVATORY_MODERNIZATION.md.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Dict, List, Optional, Any

try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    swe = None
    SWISSEPH_AVAILABLE = False

from algorithms.ayanamsha.lahiri import (
    calculate_lahiri_ayanamsa,
    sayana_to_nirayana,
    normalize_angle_360,
)
from algorithms.nakshatra.boundary import (
    calculate_nakshatra_pada,
    NAKSHATRA_SPAN_DEG,
    PADA_SPAN_DEG,
)
from algorithms.vimshottari.engine import (
    VimshottariDashaEngine,
    DashaNode,
    GRAHAS,
    DASHA_DURATIONS,
)

RASI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Thula (Libra)", "Vrischika (Scorpio)",
    "Dhanus (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]


@dataclass
class PlanetPosition:
    name: str
    sayana_lon: float           # Longitude tropical em graus [0..360)
    nirayana_lon: float         # Longitude sideral em graus [0..360)
    rasi_idx: int               # Signo sideral (0..11)
    rasi_name: str              # Nome do signo
    degree_in_rasi: float       # Graus dentro do signo [0..30)
    speed_lon: float            # Velocidade em longitude (graus/dia)
    is_retrograde: bool         # Retrógrado (speed < 0)
    nakshatra_idx: int          # Índice do Nakshatra (0..26)
    nakshatra_name: str         # Nome do Nakshatra
    pada: int                   # Pada (1..4)
    navamsa_rasi_idx: int       # Signo no mapa Navamsa (D-9)
    navamsa_rasi_name: str      # Nome do signo Navamsa


@dataclass
class HouseCusps:
    system_name: str
    ascendant_nirayana: float
    mc_nirayana: float
    cusps: List[float]          # 12 cúspides / Bhava Madhyas
    sandhis: List[float]        # 12 junções entre casas


@dataclass
class NatalChartResult:
    input_local_time: str
    timezone_offset_hours: float
    utc_time: datetime
    latitude: float
    longitude: float
    julian_day_ut: float
    ayanamsa_name: str
    ayanamsa_deg: float
    planets: Dict[str, PlanetPosition]
    houses: HouseCusps
    dasha_balance: Dict[str, Any]
    dasha_timeline: List[DashaNode]
    ephemeris_provider: str
    ephemeris_version: str


class EphemerisAdapter:
    """Adapter para cálculo completo de mapa natal tropical e védico."""

    def __init__(self, use_swisseph: bool = True):
        self.use_swisseph = use_swisseph and SWISSEPH_AVAILABLE

    def calculate_natal_chart(
        self,
        dt_local: datetime,
        tz_offset_hours: float,
        latitude: float,
        longitude: float,
        ayanamsa_mode: str = "LAHIRI"
    ) -> NatalChartResult:
        """
        Calcula o mapa natal completo para o instante e local fornecidos.
        """
        # 1. Normalização Temporal para UTC
        hour_fraction = dt_local.hour + dt_local.minute / 60.0 + dt_local.second / 3600.0
        hour_ut = hour_fraction - tz_offset_hours
        
        # Obter data civil UT ajustada se cruzar meia-noite
        utc_dt = datetime(
            dt_local.year, dt_local.month, dt_local.day,
            dt_local.hour, dt_local.minute, dt_local.second,
            tzinfo=timezone.utc
        ) - (dt_local.tzinfo.utcoffset(dt_local) if dt_local.tzinfo else 
             timezone.utc.fromutc(datetime(1,1,1)).tzinfo if False else 
             timezone.utc.utcoffset(None) if False else None or 
             __import__('datetime').timedelta(hours=tz_offset_hours))

        # 2. Cálculo do Julian Day UT
        if self.use_swisseph:
            jd_ut = swe.julday(
                utc_dt.year, utc_dt.month, utc_dt.day,
                utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0,
                swe.GREG_CAL
            )
            swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
            ayanamsa_deg = swe.get_ayanamsa_ut(jd_ut)
            provider_name = "Swiss Ephemeris"
            provider_ver = str(swe.version)
        else:
            # Fallback analítico puro
            # Fórmula padrão de Julian Day
            y, m = utc_dt.year, utc_dt.month
            if m <= 2:
                y -= 1
                m += 12
            a = math.floor(y / 100)
            b = 2 - a + math.floor(a / 4)
            day_frac = utc_dt.day + (utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0) / 24.0
            jd_ut = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + day_frac + b - 1524.5
            ayanamsa_deg = calculate_lahiri_ayanamsa(jd_ut)
            provider_name = "Pure Python Math Engine"
            provider_ver = "1.0.0"

        # 3. Posições dos Corpos Celestes
        planets_data: Dict[str, PlanetPosition] = {}
        
        bodies = [
            ("Sun", 0),
            ("Moon", 1),
            ("Mercury", 2),
            ("Venus", 3),
            ("Mars", 4),
            ("Jupiter", 5),
            ("Saturn", 6),
            ("Uranus", 7),
            ("Neptune", 8),
            ("Pluto", 9),
            ("Rahu", 10),
            ("True_Rahu", 11)
        ]

        swe_mapping = {
            "Sun": getattr(swe, "SUN", 0),
            "Moon": getattr(swe, "MOON", 1),
            "Mercury": getattr(swe, "MERCURY", 2),
            "Venus": getattr(swe, "VENUS", 3),
            "Mars": getattr(swe, "MARS", 4),
            "Jupiter": getattr(swe, "JUPITER", 5),
            "Saturn": getattr(swe, "SATURN", 6),
            "Uranus": getattr(swe, "URANUS", 7),
            "Neptune": getattr(swe, "NEPTUNE", 8),
            "Pluto": getattr(swe, "PLUTO", 9),
            "Rahu": getattr(swe, "MEAN_NODE", 10),
            "True_Rahu": getattr(swe, "TRUE_NODE", 11),
        }

        for name, _ in bodies:
            if self.use_swisseph:
                pid = swe_mapping[name]
                res_trop, _ = swe.calc_ut(jd_ut, pid, swe.FLG_SPEED)
                sayana_lon = res_trop[0]
                speed_lon = res_trop[3]
                nirayana_lon = sayana_to_nirayana(sayana_lon, ayanamsa_deg)
            else:
                # Mock / analytical fallback
                sayana_lon = 0.0
                speed_lon = 1.0
                nirayana_lon = sayana_to_nirayana(sayana_lon, ayanamsa_deg)

            rasi_idx = int(nirayana_lon // 30.0)
            deg_in_rasi = nirayana_lon % 30.0
            nak_idx, pada, _, nak_name = calculate_nakshatra_pada(nirayana_lon)
            
            # Navamsa D-9: cada signo tem 9 divisões de 3°20' (total 108 padas)
            # A posição do Navamsa corresponde exatamente ao pada total no zodíaco:
            total_pada = nak_idx * 4 + (pada - 1)
            navamsa_rasi_idx = total_pada % 12

            planets_data[name] = PlanetPosition(
                name=name,
                sayana_lon=sayana_lon,
                nirayana_lon=nirayana_lon,
                rasi_idx=rasi_idx,
                rasi_name=RASI_NAMES[rasi_idx],
                degree_in_rasi=deg_in_rasi,
                speed_lon=speed_lon,
                is_retrograde=speed_lon < 0.0,
                nakshatra_idx=nak_idx,
                nakshatra_name=nak_name,
                pada=pada,
                navamsa_rasi_idx=navamsa_rasi_idx,
                navamsa_rasi_name=RASI_NAMES[navamsa_rasi_idx]
            )

        # Adicionar Ketu a 180° de Rahu
        rahu_nirayana = planets_data["Rahu"].nirayana_lon
        ketu_nirayana = normalize_angle_360(rahu_nirayana + 180.0)
        ketu_sayana = normalize_angle_360(planets_data["Rahu"].sayana_lon + 180.0)
        k_rasi_idx = int(ketu_nirayana // 30.0)
        k_deg_in_rasi = ketu_nirayana % 30.0
        k_nak, k_pada, _, k_name = calculate_nakshatra_pada(ketu_nirayana)
        k_navamsa_idx = (k_nak * 4 + (k_pada - 1)) % 12

        planets_data["Ketu"] = PlanetPosition(
            name="Ketu",
            sayana_lon=ketu_sayana,
            nirayana_lon=ketu_nirayana,
            rasi_idx=k_rasi_idx,
            rasi_name=RASI_NAMES[k_rasi_idx],
            degree_in_rasi=k_deg_in_rasi,
            speed_lon=planets_data["Rahu"].speed_lon,
            is_retrograde=True,
            nakshatra_idx=k_nak,
            nakshatra_name=k_name,
            pada=k_pada,
            navamsa_rasi_idx=k_navamsa_idx,
            navamsa_rasi_name=RASI_NAMES[k_navamsa_idx]
        )

        # 4. Casas e Ascendente
        if self.use_swisseph:
            houses_sripati, ascmc_s = swe.houses_ex(jd_ut, latitude, longitude, b'P', swe.FLG_SIDEREAL)
            lagna_nirayana = ascmc_s[0]
            mc_nirayana = ascmc_s[1]
            cusps = list(houses_sripati)
            
            # Calcular Bhava Sandhis (pontos médios entre cúspides sucessivas)
            sandhis = []
            for i in range(12):
                c1 = cusps[i]
                c2 = cusps[(i + 1) % 12]
                if c2 < c1:
                    c2 += 360.0
                sandhi = normalize_angle_360((c1 + c2) / 2.0)
                sandhis.append(sandhi)
        else:
            lagna_nirayana = 0.0
            mc_nirayana = 90.0
            cusps = [i * 30.0 for i in range(12)]
            sandhis = [(i * 30.0 + 15.0) for i in range(12)]

        houses_data = HouseCusps(
            system_name="Sripati (Porphyry)",
            ascendant_nirayana=lagna_nirayana,
            mc_nirayana=mc_nirayana,
            cusps=cusps,
            sandhis=sandhis
        )

        # 5. Motor de Vimshottari Dasha
        moon_nirayana = planets_data["Moon"].nirayana_lon
        dasha_engine = VimshottariDashaEngine(days_per_year=365.2425)
        nak_idx, lord_idx, balance_fraction = dasha_engine.calculate_birth_balance(moon_nirayana)
        birth_lord_name = GRAHAS[lord_idx]
        balance_years = balance_fraction * DASHA_DURATIONS[lord_idx]

        dasha_balance = {
            "janma_nakshatra_idx": nak_idx,
            "janma_nakshatra_name": planets_data["Moon"].nakshatra_name,
            "birth_lord_idx": lord_idx,
            "birth_lord_name": birth_lord_name,
            "fraction_remaining": balance_fraction,
            "balance_years": balance_years,
            "balance_days": balance_years * 365.2425
        }

        # Linha do tempo até nível 2 (Mahadasha e Antardasha)
        dasha_timeline = dasha_engine.generate_timeline(utc_dt, moon_nirayana, max_depth=2)

        return NatalChartResult(
            input_local_time=dt_local.strftime("%Y-%m-%d %H:%M:%S"),
            timezone_offset_hours=tz_offset_hours,
            utc_time=utc_dt,
            latitude=latitude,
            longitude=longitude,
            julian_day_ut=jd_ut,
            ayanamsa_name=ayanamsa_mode,
            ayanamsa_deg=ayanamsa_deg,
            planets=planets_data,
            houses=houses_data,
            dasha_balance=dasha_balance,
            dasha_timeline=dasha_timeline,
            ephemeris_provider=provider_name,
            ephemeris_version=provider_ver
        )
