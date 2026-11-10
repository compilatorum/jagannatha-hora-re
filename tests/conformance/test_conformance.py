import math
import pytest
from algorithms.vimshottari.engine import VimshottariDashaEngine, DASHA_DURATIONS

def test_vimshottari_golden_cases(vimshottari_fixture):
    """
    Valida a máquina de estados contra o dataset golden de conformidade.
    """
    engine = VimshottariDashaEngine()
    cases = vimshottari_fixture["cases"]
    
    for case in cases:
        moon_lon = case["moon_nirayana_lon"]
        nak_idx, lord_idx, balance_fraction = engine.calculate_birth_balance(moon_lon)
        
        assert nak_idx == case["expected_nakshatra_idx"], f"Falha no caso {case['case_id']}: nakshatra index"
        assert lord_idx == case["expected_lord_idx"], f"Falha no caso {case['case_id']}: lord index"
        assert math.isclose(balance_fraction, case["expected_balance_fraction"], abs_tol=1e-4), \
            f"Falha no caso {case['case_id']}: balance fraction"
        
        balance_years = balance_fraction * DASHA_DURATIONS[lord_idx]
        assert math.isclose(balance_years, case["expected_balance_years"], abs_tol=1e-3), \
            f"Falha no caso {case['case_id']}: balance years"
