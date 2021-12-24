import json
import logging
from collections import deque
from statistics import mean
from typing import Union

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType
from pydantic import ValidationError

from app.errors import (
    ServerSentCloseMessage,
    ServerSentErrorMessage,
    ServerSentMalformedMessage,
)
from app.models import MatchModel
from app.websocket_client import WebsocketClient
from app.with_event_hooks import WithEventHooksMixin

MAX_AVERAGE_LENGTH = 200

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

        self._averages: dict[str, float] = {product: 0 for product in products}
        self._prices: dict[str, deque] = {
            product: deque(maxlen=MAX_AVERAGE_LENGTH) for product in products
        }
        self._channels: list[dict[str, Union[str, list[str]]]] = [
            {"name": channel, "product_ids": self.products}
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
        try:
            payload = json.loads(msg.data)
        except Exception as e:
            # no need to bother about malformed packages for now
            self._on_error(e)
            raise ServerSentMalformedMessage

        if msg.type == WSMsgType.CLOSED:
            raise ServerSentCloseMessage
        elif msg.type == WSMsgType.ERROR:
            logger.error(msg.data)
            raise ServerSentErrorMessage

        self._process(payload)

    def _process(self, payload: dict[str, str]) -> None:
        """Process messages depending on their content.

        :param payload: a message string
        """
        if payload["type"] == "subscription":
            self._on_subscribe()
        try:
            match = MatchModel(**payload)
            pair, volume, price = match.product_id, match.size, match.price
            weighted_price = volume * price
            self._update_averages(pair, weighted_price)
            self._send_averages()
        except ValidationError:
            pass

    def _update_averages(self, pair: str, weighted_price: float) -> None:
        """Recalculate volume-weighted averages.

        We store all data we use in deques to stop bothering about max sizes:
        the old data will be pushed out by the new one.

        To speed the calculations up we use the fact that the newest value adds
        just its value to the average, and the oldest is removed: so you just
        need those two to update the average right.

        :param msg: a message with the required data
        """
        if len(self._prices[pair]) < MAX_AVERAGE_LENGTH:  # accumulating
            self._prices[pair].append(weighted_price)
            self._averages[pair] = mean(self._prices[pair])
        else:  # taking the excluded values into account
            self._averages[pair] += (
                weighted_price - self._prices[pair][0]
            ) / MAX_AVERAGE_LENGTH

    def _send_averages(self) -> None:
        """Send averages to stdout."""
        print(self._averages)
