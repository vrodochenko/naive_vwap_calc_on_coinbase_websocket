from collections import deque

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
        """Initialize.

        :param products: a list of products handled by a plugin
        :param max_length: max number of samples the moving average can handle.
        """
        self.max_length = max_length

        self._averages: dict[str, float] = {product: 0.0 for product in products}

        self._prices: dict[str, deque[float]] = {
            product: deque(maxlen=max_length) for product in products
        }
        self._volumes: dict[str, deque[float]] = {
            product: deque(maxlen=max_length) for product in products
        }

        self._mean_prices: dict[str, float] = {product: 0.0 for product in products}
        self._total_volumes: dict[str, float] = {product: 0.0 for product in products}

    def process(self, payload: dict[str, str]) -> None:
        """Process messages depending on their content.

        :param payload: a message string
        """
        match = None
        try:
            match = MatchModel(**payload)
        except ValidationError:
            pass

        if match:
            pair, volume, price = match.product_id, match.size, match.price
            self._update_averages(pair, price, volume)
            self._send_averages()

    def _update_averages(self, pair: str, price: float, volume: float) -> None:
        """Recalculate volume-weighted averages.

        We store all data we use in deques to stop bothering about max sizes:
        the old data will be pushed out by the new one.

        To speed the calculations up we use the fact that the newest value adds
        just its value to the average, and the oldest is removed.

        :param pair: a pair to operate on
        :param price: a weighted price
        :param volume: a volume
        """
        weighted_price = price * volume
        if len(self._prices[pair]) < self.max_length:  # accumulating
            self._prices[pair].append(weighted_price)
            self._volumes[pair].append(volume)

            self._mean_prices[pair] = sum(self._prices[pair])
            self._total_volumes[pair] = sum(self._volumes[pair])

        else:  # taking the excluded values into account
            self._mean_prices[pair] += weighted_price - self._prices[pair][0]
            self._total_volumes[pair] += volume - self._volumes[pair][0]

            self._prices[pair].append(weighted_price)
            self._volumes[pair].append(volume)

        self._averages[pair] = self._mean_prices[pair] / self._total_volumes[pair]

    def _send_averages(self) -> None:
        """Send averages to stdout."""
        print(self._averages)
