from unittest.mock import patch

import pytest

from app.models import MatchModel
from app.plugins.vwap_calculator import VWAPCalculator


@pytest.fixture()
def calc() -> VWAPCalculator:
    return VWAPCalculator(["BTC-USD"])


def test_it_processes_a_valid_message(calc: VWAPCalculator) -> None:
    match = MatchModel.validate(
        {
            "type": "match",
            "product_id": "BTC-USD",
            "size": "0.5",
            "price": "100000.0",
        }
    )
    calc.process(match.dict())
    assert calc._prices["BTC-USD"][0] == 50000.0
    assert calc._averages["BTC-USD"] == 50000.0


def test_it_skips_invalid_messages(calc: VWAPCalculator) -> None:
    calc.process({"type": "Skip me"})
    assert len(calc._prices["BTC-USD"]) == 0
    assert calc._averages["BTC-USD"] == 0


def test_it_sends_averages_for_valid_messages(calc: VWAPCalculator) -> None:
    with patch.object(calc, "_send_averages") as send_mock:
        calc.process({"skip": "me"})
        calc.process(
            {
                "type": "match",
                "product_id": "BTC-USD",
                "size": "0.5",
                "price": "100000.0",
            }
        )
        assert send_mock.call_count == 1
