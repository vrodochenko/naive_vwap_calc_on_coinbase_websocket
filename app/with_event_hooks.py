import logging
from typing import Any

logger = logging.getLogger(__name__)


class WithEventHooksMixin:
    """Allows to attach hooks to some events.

    Can be used for testing/debugging or doing meaningful things."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize and leave all the heavy lifting to the superclass.

        :param args: args
        :param kwargs: kwargs"""

        super().__init__(*args, **kwargs)

    def _on_open(self) -> None:
        """Run on_open hooks, if any."""
        logger.debug("on_open called")

    def _on_close(self) -> None:
        """Run on_close hooks, if any."""
        logger.debug("on_close called")

    def _on_message(self, msg: Any) -> None:
        """Run on_message hooks, if any.

        :param msg: a message received by the subclass
        """
        logger.debug("on_message called")

    def _on_subscribe(self) -> None:
        """Run on_subscribe hooks, if any."""
        logger.debug("on_subscribe called")

    def _on_error(self, e: Exception) -> None:
        """Run on_error hooks, if any."""
        logger.error(e)
