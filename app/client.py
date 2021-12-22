import json

from app.websocket_client import WebsocketClient


class CoinbaseClient(WebsocketClient):
    def __init__(
        self,
        url="wss://ws-feed.pro.coinbase.com",
        products=["BTC-USD", "ETH-USD", "ETH-BTC"],
    ):
        super().__init__(url=url)
        self.products = products

    def _connect(self):
        self.url = self.url.strip("/")
        self.channels = [{"name": "ticker", "product_ids": self.products}]
        params = {
            "type": "subscribe",
            "product_ids": self.products,
            "channels": self.channels,
        }
        self._ws.send(json.dumps(params))
