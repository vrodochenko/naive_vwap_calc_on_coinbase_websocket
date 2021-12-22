import json
from threading import Thread

from websocket import create_connection, WebSocketConnectionClosedException

import logging

logger = logging.getLogger(__name__)

class WebsocketClient:
    def __init__(
            self,
            url="wss://ws-feed.pro.coinbase.com",
            products=["BTC-USD", "ETH-USD", "ETH-BTC"],
            ):
        self.url = url
        self.products = products
        self.type = "subscribe"
        self.stopped = True
        self.error = None
        self.ws = None
        self.thread = None
        self.verbose = True

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stopped = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.keepalive = Thread(target=self._keepalive)
        self.thread.start()

    def _connect(self):
        self.url = self.url.strip('/')
        self.channels = [{"name": "ticker", "product_ids": self.products}]
        self.ws = create_connection(self.url)

        params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}
        self.ws.send(json.dumps(params))

    def _keepalive(self, interval=30):
        while self.ws.connected:
            self.ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self.keepalive.start()
        while not self.stopped:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(msg)

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
        except WebSocketConnectionClosedException:
            pass
        finally:
            self.keepalive.join()

        self.on_close()

    def close(self):
        self.stopped = True   # will only disconnect after next msg recv
        self._disconnect() # force disconnect so threads can join
        self.thread.join()

    def on_open(self):
        if self.verbose:
            print("-- Subscribed! --\n")

    def on_close(self):
        if self.verbose:
            print("\n-- Socket Closed --")

    def on_message(self, msg):
        if self.verbose:
            print(msg)

    def on_error(self, e, data=None):
        self.error = e
        self.stopped = True
        print('{} - data: {}'.format(e, data))


class MyWebsocketClient(WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USD", "ETH-USD"]
        self.message_count = 0
        print("Let's count the messages!")

    def on_message(self, msg):
        print(json.dumps(msg, indent=3, sort_keys=True))
        self.message_count += 0


