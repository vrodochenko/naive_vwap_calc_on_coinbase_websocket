from unittest.mock import AsyncMock, patch

import pytest

from app.coinbase_client import CoinbaseClient
from app.test.common import fake_feed


@pytest.mark.asyncio
async def test_client_processes_messages() -> None:
    client = CoinbaseClient()
    client._subscribe = AsyncMock()  # type: ignore
    with patch.object(client, "websocket") as socket_mock:
        socket_mock.return_value.__aenter__.return_value = fake_feed()
        with patch.object(client, "_on_message") as on_message_mock:
            await client.run()
            assert on_message_mock.called
