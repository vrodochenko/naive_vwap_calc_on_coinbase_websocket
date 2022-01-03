class Stopped(Exception):
    """The client was stopped for some reason."""


class ServerSentCloseMessage(Stopped):
    """Server sent a close message."""


class ServerSentErrorMessage(Exception):
    """Server sent an error message."""


class ServerSentMalformedMessage(Exception):
    """Server sent a malformed message."""
