import sys
from pathlib import Path
import json
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

@pytest.fixture
def fixtures_dir():
    return REPO_ROOT / "fixtures"

@pytest.fixture
def vimshottari_fixture(fixtures_dir):
    with open(fixtures_dir / "dashas" / "vimshottari_cases.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def positions_fixture(fixtures_dir):
    with open(fixtures_dir / "positions" / "grahas_golden.json", "r", encoding="utf-8") as f:
        return json.load(f)
