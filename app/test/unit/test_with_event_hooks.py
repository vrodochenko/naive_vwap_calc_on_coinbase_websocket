"""Tests for underlying structures."""
import logging
from typing import Iterator

import pytest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from app.with_event_hooks import WithEventHooksMixin


@pytest.fixture
def with_event_hooks() -> WithEventHooksMixin:
    return WithEventHooksMixin()


@pytest.fixture()
def with_debug_logging(monkeypatch: MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("APP_LOG_LEVEL", "DEBUG")
    yield


@pytest.mark.parametrize("method", ["open", "close", "subscribe"])
def test_event_hooks_do_debug_logging(
    caplog: LogCaptureFixture,
    with_event_hooks: WithEventHooksMixin,
    with_debug_logging: None,
    method: str,
) -> None:

    with caplog.at_level(logging.DEBUG):
        getattr(with_event_hooks, f"_on_{method}")()
        assert caplog.records[0].message == f"on_{method} called"


def test_on_message_does_debug_logging(
    caplog: LogCaptureFixture,
    with_event_hooks: WithEventHooksMixin,
    with_debug_logging: None,
) -> None:

    with caplog.at_level(logging.DEBUG):
        with_event_hooks._on_message("here we are")
        assert caplog.records[0].message == "on_message called"
