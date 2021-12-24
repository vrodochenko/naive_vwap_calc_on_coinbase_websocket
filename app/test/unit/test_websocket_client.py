from unittest.mock import patch

import pytest

from app.websocket_client import WebsocketClient


@pytest.fixture
def ws_client() -> WebsocketClient:
    return WebsocketClient("https://route66")


@pytest.mark.asyncio()
async def test_ws_client_call_session(ws_client: WebsocketClient) -> None:
    assert hasattr(ws_client, "url")
    with patch("app.websocket_client.ClientSession") as session_mock:
        async with ws_client.websocket() as _:
            assert session_mock.called is True
