"""Stop the client on receiving a given number of messages."""
from app.errors import Stopped
from app.plugins.plugin import Plugin


class StopOnLimit(Plugin):
    def __init__(self, max_messages: int) -> None:
        """Initialize.

        :param max_messages: a number of messages to stop after."""

        self.messages_count = 0
        self.max_messages = max_messages

    def process(self, payload: dict[str, str]) -> None:
        """Increase the counter and stop the client by throwing Stopped.

        :param payload: a payload dict
        :return: None

        :raises Stopped: when the number of messages exceeds the limit.
        """

        if self.messages_count >= self.max_messages:
            raise Stopped

        self.messages_count += 1
