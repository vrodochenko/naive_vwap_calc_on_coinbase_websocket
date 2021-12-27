from abc import ABC


class Plugin(ABC):
    """A base class for plugins the client can use.

    Exists only for convenient naming.
    """

    def process(self, payload: dict[str, str]) -> None:
        """Process incoming messages here.

        :param payload: the message content loaded from json"""
        raise NotImplementedError()
