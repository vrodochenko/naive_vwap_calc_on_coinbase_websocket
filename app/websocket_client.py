import contextlib
from typing import AsyncIterator

from aiohttp import ClientSession, ClientWebSocketResponse


class WebsocketClient:
    """A websocket client which instantiates and holds the connection.

    Contains the aiohttp's session management.
    """

    def __init__(self, url: str) -> None:
        """Initialize.

        :param url: url"""
        self.url = url

    @contextlib.asynccontextmanager
    async def websocket(
        self,
    ) -> AsyncIterator[ClientWebSocketResponse]:
        session = ClientSession()
        async with session.ws_connect(url=self.url) as _ws:
            yield _ws
        session.close()
