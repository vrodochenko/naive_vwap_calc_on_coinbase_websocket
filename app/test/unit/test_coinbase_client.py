from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.coinbase_client import CoinbaseClient
from app.plugins.vwap_calculator import VWAPCalculator
from app.test.common import fake_feed, long_fake_feed


@pytest.mark.asyncio
async def test_client_processes_messages() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = fake_feed()
        with patch.object(client, "_on_message") as on_message_mock:
            await client.run()
            assert on_message_mock.called


@pytest.mark.asyncio
async def test_client_calculates_averages() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    client._plugins[0]._send_averages = MagicMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = fake_feed()
        await client.run()
        plugin = client._plugins[0]
        assert isinstance(plugin, VWAPCalculator)
        assert plugin._averages["BTC-USD"] == 1.5


@pytest.mark.asyncio
async def test_client_calculates_on_long_feeds() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    client._plugins[0]._send_averages = MagicMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = long_fake_feed()
        await client.run()
        plugin = client._plugins[0]
        assert isinstance(plugin, VWAPCalculator)
        assert plugin._averages["BTC-USD"] == 100000.0
