import itertools
import json
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import WSMessage, WSMsgType

from app.client import CoinbaseClient
from app.test.common import fake_feed


@pytest.mark.asyncio
async def test_client_calculates_averages() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    client._send_averages = MagicMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = fake_feed()
        await client.run()
        assert client._averages["BTC-USD"] == 1.5


async def massive_fake_feed() -> AsyncIterator[WSMessage]:
    cheap_trades = (
        WSMessage(
            type=WSMsgType.TEXT,
            data=json.dumps(
                {
                    "type": "match",
                    "product_id": "BTC-USD",
                    "size": "1.0",
                    "price": "1000.0",
                }
            ),
            extra="",
        ),
    ) * 200
    more_expensive_trades = (
        (
            WSMessage(
                type=WSMsgType.TEXT,
                data=json.dumps(
                    {
                        "type": "match",
                        "product_id": "BTC-USD",
                        "size": "1.0",
                        "price": "100000.0",
                    }
                ),
                extra="",
            )
        ),
    ) * 200
    closed = (WSMessage(type=WSMsgType.CLOSED, data="closed", extra=""),)
    for message in itertools.chain(cheap_trades, more_expensive_trades, closed):
        yield message


@pytest.mark.asyncio
async def test_client_calculates_on_long_feeds() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    client._send_averages = MagicMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = massive_fake_feed()
        await client.run()
        assert client._averages["BTC-USD"] == 100000.0
