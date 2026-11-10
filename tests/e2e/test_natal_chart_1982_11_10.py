"""
Teste End-to-End (E2E) do Mapa Natal:
Data: 10 de Novembro de 1982, 09:42 AM
Local: Belo Horizonte - MG, Brasil
Coordenadas: Lat -19° 55' 15" (-19.920833°), Lon -43° 56' 16" (-43.937778°)
Fuso Horário: America/Sao_Paulo (UTC-3, sem horário de verão em 1982)
"""

from datetime import datetime, timezone
import math
import pytest

from algorithms.adapter.ephemeris import EphemerisAdapter, NatalChartResult


@pytest.fixture(scope="module")
def natal_chart() -> NatalChartResult:
    adapter = EphemerisAdapter(use_swisseph=True)
    dt_local = datetime(1982, 11, 10, 9, 42, 0)
    tz_offset = -3.0
    lat = -19.920833
    lon = -43.937778
    return adapter.calculate_natal_chart(
        dt_local=dt_local,
        tz_offset_hours=tz_offset,
        latitude=lat,
        longitude=lon,
        ayanamsa_mode="LAHIRI"
    )


def test_time_normalization(natal_chart):
    """Valida a conversão de horário civil local para UTC e Julian Day."""
    # 09:42 BRT (UTC-3) -> 12:42 UTC
    assert natal_chart.utc_time.hour == 12
    assert natal_chart.utc_time.minute == 42
    assert natal_chart.utc_time.second == 0
    # JD esperado aproximadamente 2445284.029167
    assert math.isclose(natal_chart.julian_day_ut, 2445284.029167, abs_tol=1e-4)


def test_lahiri_ayanamsa(natal_chart):
    """Valida o Ayanamsa Lahiri para novembro de 1982."""
    # Ayanamsa esperado ~ 23° 37' 04" = 23.6176°
    assert math.isclose(natal_chart.ayanamsa_deg, 23.61765, abs_tol=1e-2)


def test_ascendant_and_houses(natal_chart):
    """Valida o Ascendente (Lagna) e cúspides de casas."""
    # Lagna sideral deve estar no final de Sagitário (Dhanus) ~ 28° 45' = 268.75°
    lagna = natal_chart.houses.ascendant_nirayana
    assert math.isclose(lagna, 268.75, abs_tol=0.2)
    assert int(lagna // 30.0) == 8  # Signo 8 = Dhanus (Sagittarius)
    
    # Valida 12 cúspides e 12 sandhis calculados
    assert len(natal_chart.houses.cusps) == 12
    assert len(natal_chart.houses.sandhis) == 12


def test_moon_position_and_nakshatra(natal_chart):
    """Valida a posição da Lua, Nakshatra natal e Pada."""
    moon = natal_chart.planets["Moon"]
    # Lua sideral em Leão (Simha) ~ 22° 55' = 142.91°
    assert math.isclose(moon.nirayana_lon, 142.91, abs_tol=0.2)
    assert moon.rasi_name == "Simha (Leo)"
    
    # Nakshatra Purva Phalguni (índice 10), regido por Vênus
    assert moon.nakshatra_idx == 10
    assert moon.nakshatra_name == "Purva Phalguni"
    assert moon.pada == 3
    
    # Navamsa da Lua: Pada 3 de Purva Phalguni cai em Libra (Thula)
    assert moon.navamsa_rasi_name == "Thula (Libra)"


def test_sun_and_planetary_stellium(natal_chart):
    """Valida o grandioso Stellium de 5 planetas em Libra (Thula)."""
    sun = natal_chart.planets["Sun"]
    venus = natal_chart.planets["Venus"]
    saturn = natal_chart.planets["Saturn"]
    jupiter = natal_chart.planets["Jupiter"]
    mercury = natal_chart.planets["Mercury"]

    # Todos no signo 6 (Thula / Libra)
    assert sun.rasi_idx == 6
    assert venus.rasi_idx == 6
    assert saturn.rasi_idx == 6
    assert jupiter.rasi_idx == 6
    assert mercury.rasi_idx == 6

    # Saturno exaltado (Uccha) em Libra nos primeiros graus
    assert math.isclose(saturn.nirayana_lon, 184.27, abs_tol=0.2)
    
    # Vênus em domicílio (Swakshetra) em Libra
    assert math.isclose(venus.nirayana_lon, 205.80, abs_tol=0.2)


def test_mars_and_lunar_nodes(natal_chart):
    """Valida Marte e os nós lunares Rahu e Ketu."""
    mars = natal_chart.planets["Mars"]
    rahu = natal_chart.planets["Rahu"]
    ketu = natal_chart.planets["Ketu"]

    # Marte em Sagitário (Dhanus) na casa 1
    assert mars.rasi_idx == 8
    assert math.isclose(mars.nirayana_lon, 253.56, abs_tol=0.2)

    # Rahu em Gêmeos (Mithuna) e Ketu em Sagitário (Dhanus)
    assert rahu.rasi_idx == 2  # Mithuna (Gemini)
    assert ketu.rasi_idx == 8  # Dhanus (Sagittarius)
    
    # Oposição exata de 180° entre Rahu e Ketu
    diff = abs(ketu.nirayana_lon - rahu.nirayana_lon)
    assert math.isclose(diff, 180.0, abs_tol=1e-5)


def test_vimshottari_dasha_schedule(natal_chart):
    """Valida a máquina de estados Vimshottari para o mapa natal."""
    bal = natal_chart.dasha_balance
    assert bal["birth_lord_name"] == "Venus"
    # Balanço de Vênus ~ 5.63 anos restantes
    assert math.isclose(bal["balance_years"], 5.63, abs_tol=0.1)

    timeline = natal_chart.dasha_timeline
    assert len(timeline) == 9

    # Sequência: Vênus -> Sol -> Lua -> Marte -> Rahu -> Júpiter -> Saturno -> Mercúrio -> Ketu
    expected_sequence = ["Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu"]
    for i, md in enumerate(timeline):
        assert md.lords[0] == expected_sequence[i]

    # Validação do período ativo no ano de 2026: Mahadasha de Rahu!
    # Rahu iniciou por volta de 2011 e vai até 2029
    rahu_md = timeline[4]
    assert rahu_md.lords[0] == "Rahu"
    date_2026 = datetime(2026, 11, 10, tzinfo=timezone.utc)
    assert rahu_md.start_time <= date_2026 <= rahu_md.end_time
