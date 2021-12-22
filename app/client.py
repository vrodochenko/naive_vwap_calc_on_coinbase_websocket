import json

from app.websocket_client import WebsocketClient
from collections import deque

MAX_AVERAGE_LENGTH = 200


class CoinbaseClient(WebsocketClient):
    def __init__(
        self,
        url="wss://ws-feed.pro.coinbase.com",
        products=["BTC-USD", "ETH-USD", "ETH-BTC"],
    ):
        super().__init__(url=url)
        self.products = products
        self.averages = {product: 0 for product in products}
        self._prices = {
            product: deque(maxlen=MAX_AVERAGE_LENGTH) for product in products
        }

    def connect(self):
        self.url = self.url.strip("/")
        self.channels = [{"name": "matches", "product_ids": self.products}]
        params = {
            "type": "subscribe",
            "product_ids": self.products,
            "channels": self.channels,
        }
        self._ws.send(json.dumps(params))

    def on_message(self, msg):
        super().on_message(msg)
        self._update_averages(msg)
        self.send_averages()

    def _update_averages(self, msg):
        if msg["type"] in ("match", "last_match"):
            pair = msg["product_id"]
            volume = float(msg["size"])
            price = float(msg["price"])
            weighted_price = volume * price
            if len(self._prices[pair]) == 0:  # let's get the first piece of data
                self.averages[pair] = weighted_price
            elif len(self._prices[pair]) < MAX_AVERAGE_LENGTH:  # accumulating
                self.averages[pair] += weighted_price / len(self._prices[pair])
            else:  # taking the excluded values into account
                self.averages[pair] += (
                    weighted_price - self._prices[pair][0]
                ) / MAX_AVERAGE_LENGTH
            self._prices[pair].append(weighted_price)

    def send_averages(self):
        print(self.averages)
