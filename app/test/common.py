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
