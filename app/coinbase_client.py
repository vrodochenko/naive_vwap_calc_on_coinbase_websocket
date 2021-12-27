import json
import logging
from typing import Union

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

from app.errors import (
    ServerSentCloseMessage,
    ServerSentErrorMessage,
    ServerSentMalformedMessage,
)
from app.plugins.plugin import Plugin
from app.plugins.vwap_calculator import VWAPCalculator
from app.websocket_client import WebsocketClient
from app.with_event_hooks import WithEventHooksMixin

logger = logging.getLogger(__name__)


class CoinbaseClient(WebsocketClient, WithEventHooksMixin):
    """A websocket client for coinbase feed.

    It is meant to subscribe to coinbase's channels of choice,
    see https://docs.cloud.coinbase.com/exchange/docs/ for details.

    By default, it subscribes to a "matches" channel, calculates
    moving volume-weighted averages using up to MAX_AVERAGE_LENGTH
    data entries and streams them to stdout.
    """

    def __init__(
        self,
        url: str = "wss://ws-feed.pro.coinbase.com",
        products: list[str] = ["BTC-USD", "ETH-USD", "ETH-BTC"],
        channel: str = "matches",
    ) -> None:
        """Initialize.

        :param url: a coinbase feed URL
        :param products: the products to watch
        :param channel: the channel to subscribe to
        """
        super().__init__(url=url)
        self.products: list[str] = products

        self._plugins: list[Plugin] = [
            VWAPCalculator(products=products, max_length=200)
        ]
        self._channels: list[dict[str, Union[str, list[str]]]] = [
            {"name": channel, "product_ids": products}
        ]

    async def run(self) -> None:
        """Subscribe and operate with the channels and products of interest."""
        async with self.websocket() as ws:
            self._on_open()  # events or side-effects can be placed here

            await self._subscribe(ws)
            async for msg in ws:
                try:
                    self._on_message(msg)
                except ServerSentMalformedMessage:
                    continue
                except (ServerSentErrorMessage, ServerSentCloseMessage):
                    break

            self._on_close()  # and there

    async def _subscribe(self, socket: ClientWebSocketResponse) -> None:
        """Send a subscription message to the server.

        :param socket: a socket to use
        """
        await socket.send_str(
            json.dumps(
                {
                    "type": "subscribe",
                    "product_ids": self.products,
                    "channels": self._channels,
                }
            )
        )

    def _on_message(self, msg: WSMessage) -> None:
        """React on error/close messages or continue processing.

        :raises ServerSentCloseMessage: when CLOSED is encountered
        :raises ServerSentErrorMessage: when ERROR is encountered
        :raises ServerSentMalformedMessage: when the payload cannot be parsed
        """
        super()._on_message(msg)

        if msg.type == WSMsgType.CLOSED:
            raise ServerSentCloseMessage
        elif msg.type == WSMsgType.ERROR:
            logger.error(msg.data)
            raise ServerSentErrorMessage

        try:
            payload = json.loads(msg.data)
        except Exception as e:
            # no need to bother about malformed packages for now
            self._on_error(e)
            raise ServerSentMalformedMessage

        if payload["type"] == "subscription":
            self._on_subscribe()
        else:
            for plugin in self._plugins:
                plugin.process(payload)
