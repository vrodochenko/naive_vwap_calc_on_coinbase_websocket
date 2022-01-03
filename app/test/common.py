import itertools
import json
from typing import AsyncIterator

from aiohttp import WSMessage, WSMsgType


async def fake_feed() -> AsyncIterator[WSMessage]:
    messages = (
        WSMessage(type=WSMsgType.TEXT, data="closed", extra=""),
        WSMessage(
            type=WSMsgType.TEXT,
            data=json.dumps({"type": "subscription", "data": "channels"}),
            extra="",
        ),
        WSMessage(
            type=WSMsgType.TEXT,
            data=json.dumps(
                {
                    "type": "match",
                    "product_id": "BTC-USD",
                    "size": "1.0",
                    "price": "1.0",
                }
            ),
            extra="",
        ),
        WSMessage(
            type=WSMsgType.TEXT,
            data=json.dumps(
                {
                    "type": "match",
                    "product_id": "BTC-USD",
                    "size": "1.0",
                    "price": "2.0",
                }
            ),
            extra="",
        ),
        WSMessage(type=WSMsgType.CLOSED, data="closed", extra=""),
    )
    for message in messages:
        yield message


async def long_fake_feed() -> AsyncIterator[WSMessage]:
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
