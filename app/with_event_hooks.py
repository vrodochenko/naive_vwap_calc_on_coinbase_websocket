import logging
from typing import Any

logger = logging.getLogger(__name__)


class WithEventHooksMixin:
    """A way to attach hooks to some events.

    Can be used for testing/debuggging or doing actual job"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize and all heavy lifting to the superclass.

        :param args: args
        :param kwargs: kwargs"""

        super().__init__(*args, **kwargs)

    def on_open(self) -> None:
        """Run on_open hooks, if any."""
        logger.debug("on_open called")

    def on_close(self) -> None:
        """Run on_close hooks, if any."""
        logger.debug("on_close called")

    def on_message(self, msg: str) -> None:
        """Run on_message hooks, if any.

        :param msg: a message received by the subclass
        """
        logger.debug(f"message {msg} received")

    def on_error(self, e: Exception) -> None:
        """Run on_error hooks, if any."""
        logger.error(e)
