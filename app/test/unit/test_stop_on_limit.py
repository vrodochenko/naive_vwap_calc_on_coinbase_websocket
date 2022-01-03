import pytest

from app.errors import Stopped
from app.plugins.stop_on_limit import StopOnLimit


def test_stop_on_limit_works() -> None:
    stopper = StopOnLimit(max_messages=1)
    assert stopper.messages_count == 0
    stopper.process({"process": "me"})
    assert stopper.messages_count == 1
    with pytest.raises(Stopped):
        stopper.process({"I shall not": "pass"})
    assert stopper.messages_count == 1
