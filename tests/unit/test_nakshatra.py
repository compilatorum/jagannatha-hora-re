import pytest
from algorithms.nakshatra.boundary import (
    calculate_nakshatra_pada,
    NAKSHATRA_SPAN_DEG,
    PADA_SPAN_DEG,
)

def test_ashwini_pada1_start():
    nak_idx, pada, elapsed, name = calculate_nakshatra_pada(0.0)
    assert nak_idx == 0
    assert pada == 1
    assert elapsed == 0.0
    assert name == "Ashwini"

def test_bharani_pada_progression():
    # Bharani começa em 13°20' (13.333333333333334)
    # Cada pada tem 3°20' (3.333333333333333)
    b_start = NAKSHATRA_SPAN_DEG
    
    # Pada 1
    nak, pada, _, _ = calculate_nakshatra_pada(b_start + 1.0)
    assert nak == 1 and pada == 1

    # Pada 2
    nak, pada, _, _ = calculate_nakshatra_pada(b_start + PADA_SPAN_DEG + 0.5)
    assert nak == 1 and pada == 2

    # Pada 4
    nak, pada, _, _ = calculate_nakshatra_pada(b_start + 3 * PADA_SPAN_DEG + 0.5)
    assert nak == 1 and pada == 4

def test_revati_pada4_end():
    # Revati é o último nakshatra (idx 26)
    nak_idx, pada, elapsed, name = calculate_nakshatra_pada(359.9)
    assert nak_idx == 26
    assert pada == 4
    assert name == "Revati"
