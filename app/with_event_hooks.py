import logging

logger = logging.getLogger(__name__)


class WithEventHooksMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_open(self):
        logger.debug("subscribed")

    def on_close(self):
        logger.debug("closed")

    def on_message(self, msg):
        logger.debug("message received")
        logger.debug(msg)

    def on_error(self, e):
        logger.exception(e)
