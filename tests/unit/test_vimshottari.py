import math
from datetime import datetime
import pytest
from algorithms.vimshottari.engine import (
    VimshottariDashaEngine,
    GRAHAS,
    DASHA_DURATIONS,
    TOTAL_CYCLE_YEARS,
)

def test_vimshottari_birth_balance():
    engine = VimshottariDashaEngine()
    
    # 0.0 graus = Ashwini (Ketu, 7 anos, 100% balance)
    nak, lord, bal = engine.calculate_birth_balance(0.0)
    assert nak == 0
    assert lord == 0
    assert math.isclose(bal, 1.0, rel_tol=1e-5)
    
    # 20.0 graus = Meio de Bharani (Venus, 20 anos, 50% balance)
    nak, lord, bal = engine.calculate_birth_balance(20.0)
    assert nak == 1
    assert lord == 1
    assert math.isclose(bal, 0.5, rel_tol=1e-4)

def test_full_120_year_conservation():
    engine = VimshottariDashaEngine(days_per_year=365.2425)
    birth = datetime(2000, 1, 1, 0, 0, 0)
    
    # Início exato de ciclo
    timeline = engine.generate_timeline(birth, moon_nirayana_lon=0.0, max_depth=1)
    total_days = sum(md.duration_days for md in timeline)
    expected_days = 120.0 * 365.2425
    assert math.isclose(total_days, expected_days, rel_tol=1e-5)

def test_subperiod_antardashas():
    engine = VimshottariDashaEngine(days_per_year=365.2425)
    birth = datetime(2000, 1, 1, 0, 0, 0)
    timeline = engine.generate_timeline(birth, moon_nirayana_lon=0.0, max_depth=2)
    
    # Cada Mahadasha deve ter exatamente 9 Antardashas
    for md in timeline:
        assert len(md.children) == 9
        ad_days_sum = sum(ad.duration_days for ad in md.children)
        assert math.isclose(ad_days_sum, md.duration_days, rel_tol=1e-5)
