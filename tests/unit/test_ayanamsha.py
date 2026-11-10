import math
import pytest
from algorithms.ayanamsha.lahiri import (
    calculate_lahiri_ayanamsa,
    sayana_to_nirayana,
    nirayana_to_sayana,
    normalize_angle_360,
    JD_J2000,
    LAHIRI_J2000_BASE_DEG,
)

def test_j2000_base_ayanamsa():
    """Valida se no epoch J2000.0 o valor de Lahiri coincide com o valor base."""
    ayanamsa = calculate_lahiri_ayanamsa(JD_J2000)
    assert math.isclose(ayanamsa, LAHIRI_J2000_BASE_DEG, rel_tol=1e-12)

def test_sayana_nirayana_roundtrip():
    """Valida que converter Sayana -> Nirayana -> Sayana preserva o valor."""
    sayana_lon = 145.6789
    ayanamsa = 24.1234
    nirayana_lon = sayana_to_nirayana(sayana_lon, ayanamsa)
    recovered = nirayana_to_sayana(nirayana_lon, ayanamsa)
    assert math.isclose(recovered, sayana_lon, rel_tol=1e-10)

def test_spica_chitra_paksha():
    """Valida que a estrela Spica fica exatamente a 180° siderais no epoch J2000.0."""
    spica_sayana = 203.85709166666667
    ayanamsa_j2000 = calculate_lahiri_ayanamsa(JD_J2000)
    nirayana_spica = sayana_to_nirayana(spica_sayana, ayanamsa_j2000)
    assert math.isclose(nirayana_spica, 180.0, abs_tol=1e-7)
