class ServerSentCloseMessage(Exception):
    """Server sent a close message."""


class ServerSentErrorMessage(Exception):
    """Server sent an error message."""


class ServerSentMalformedMessage(Exception):
    """Server sent a malformed message."""
