from unittest.mock import patch

import pytest

from app.websocket_client import WebsocketClient


@pytest.fixture
def ws_client() -> WebsocketClient:
    return WebsocketClient("https://route66")


@pytest.mark.asyncio()
async def test_ws_client_connects(ws_client: WebsocketClient) -> None:
    assert hasattr(ws_client, "_session")
    with patch.object(ws_client._session, "ws_connect") as connect_mock:
        async with ws_client.websocket() as _:
            assert connect_mock.called is True
