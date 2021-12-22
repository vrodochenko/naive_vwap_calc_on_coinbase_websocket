import json
import time
from threading import Thread

from websocket import create_connection, WebSocketConnectionClosedException

from app.with_event_hooks import WithEventHooksMixin


class WebsocketClient(WithEventHooksMixin):
    def __init__(self, url):
        self.url = url
        self._ws = create_connection(self.url)
        self._active = True
        self._thread = Thread(target=self._run)
        self._keepalive = Thread(target=self._keepalive)

    def open(self):
        self.on_open()
        self._thread.start()

    def close(self):
        self.on_close()
        self._active = False
        self._disconnect()
        self._thread.join()

    def _connect(self):
        raise NotImplementedError()

    def _run(self):
        self._connect()
        self._listen()
        self._disconnect()

    def _keepalive(self, interval=30):
        while self._ws.connected:
            self._ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self._keepalive.start()
        while self._active:
            try:
                data = self._ws.recv()
                msg = json.loads(data)
                self.on_message(msg)
            except Exception as e:
                self.on_error(e)
                self._active = False

    def _disconnect(self):
        try:
            if self._ws:
                self._ws.close()
        except WebSocketConnectionClosedException:
            pass
        finally:
            self._thread.join()
            self._keepalive.join()

        self.on_close()
