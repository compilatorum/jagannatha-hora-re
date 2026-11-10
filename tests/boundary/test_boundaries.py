import pytest
import math
from algorithms.ayanamsha.lahiri import normalize_angle_360
from algorithms.nakshatra.boundary import calculate_nakshatra_pada, NAKSHATRA_SPAN_DEG
from algorithms.vimshottari.engine import VimshottariDashaEngine

def test_angle_normalization_boundaries():
    assert normalize_angle_360(0.0) == 0.0
    assert normalize_angle_360(360.0) == 0.0
    assert normalize_angle_360(720.0) == 0.0
    assert math.isclose(normalize_angle_360(-0.0001), 359.9999, abs_tol=1e-7)
    assert math.isclose(normalize_angle_360(359.999999), 359.999999, abs_tol=1e-9)

def test_nakshatra_boundary_transitions():
    # Teste imediatamente antes e depois do primeiro limite (13° 20' = 13.333333333333334°)
    boundary = NAKSHATRA_SPAN_DEG
    
    # 1e-8 antes: Ashwini Pada 4
    nak_pre, pada_pre, _, name_pre = calculate_nakshatra_pada(boundary - 1e-8)
    assert nak_pre == 0
    assert pada_pre == 4
    assert name_pre == "Ashwini"

    # Exatamente no limite: Bharani Pada 1
    nak_post, pada_post, _, name_post = calculate_nakshatra_pada(boundary)
    assert nak_post == 1
    assert pada_post == 1
    assert name_post == "Bharani"

def test_zodiac_wrap_boundary():
    # Longitude em 359.9999°
    nak, pada, _, name = calculate_nakshatra_pada(359.9999)
    assert nak == 26
    assert pada == 4
    assert name == "Revati"
    
    engine = VimshottariDashaEngine()
    nak_v, lord_v, bal_v = engine.calculate_birth_balance(359.9999)
    assert nak_v == 26
    assert lord_v == 8  # Mercúrio
    assert bal_v > 0.0 and bal_v < 0.001
