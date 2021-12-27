from collections import deque
from statistics import mean

from pydantic import ValidationError

from app.models import MatchModel
from app.plugins.plugin import Plugin


class MessageProcessor(Plugin):
    """A superclass for the message processors for the client.

    They are meant to make some meaningful actions on the data
    parsed from the messages.
    """

    def process(self, payload: dict[str, str]) -> None:
        raise NotImplementedError()


class VWAPCalculator(MessageProcessor):
    """A calculator of volume-weighted averages of a given length.

    Send the result to stdout."""

    def __init__(self, products: list[str], max_length: int = 200) -> None:
        """Initialize."""
        self._averages: dict[str, float] = {product: 0 for product in products}
        self._prices: dict[str, deque] = {
            product: deque(maxlen=max_length) for product in products
        }
        self.max_length = max_length

    def process(self, payload: dict[str, str]) -> None:
        """Process messages depending on their content.

        :param payload: a message string
        """

        try:
            match = MatchModel(**payload)
        except ValidationError:
            pass

        if match:
            pair, volume, price = match.product_id, match.size, match.price
            weighted_price = volume * price
            self._update_averages(pair, weighted_price)
            self._send_averages()

    def _update_averages(self, pair: str, weighted_price: float) -> None:
        """Recalculate volume-weighted averages.

        We store all data we use in deques to stop bothering about max sizes:
        the old data will be pushed out by the new one.

        To speed the calculations up we use the fact that the newest value adds
        just its value to the average, and the oldest is removed: so you just
        need those two to update the average right.

        :param msg: a message with the required data
        """
        if len(self._prices[pair]) < self.max_length:  # accumulating
            self._prices[pair].append(weighted_price)
            self._averages[pair] = mean(self._prices[pair])
        else:  # taking the excluded values into account
            self._averages[pair] += (
                weighted_price - self._prices[pair][0]
            ) / self.max_length

    def _send_averages(self) -> None:
        """Send averages to stdout."""
        print(self._averages)
