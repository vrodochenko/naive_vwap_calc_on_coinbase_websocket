import json

import pytest
from _pytest.capture import CaptureFixture

from app.coinbase_client import CoinbaseClient
from app.plugins.stop_on_limit import StopOnLimit


@pytest.mark.asyncio
async def test_client_works_with_coinbase(capfd: CaptureFixture) -> None:
    client = CoinbaseClient()
    client.add_plugin(StopOnLimit(max_messages=1))
    await client.run()

    out, err = capfd.readouterr()
    assert err == ""
    printed_result: dict[str, float] = json.loads(out.replace("'", '"'))
    assert set(client.products) == printed_result.keys()
    assert all([isinstance(price, float) for price in printed_result.values()])
