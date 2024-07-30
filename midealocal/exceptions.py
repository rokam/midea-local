"""Midea Local library exceptions."""

from __future__ import annotations


class MideaLocalError(Exception):
    """Base class for mideal_local errors."""


class CannotAuthenticate(MideaLocalError):
    """Exception raised when credentials are incorrect."""


class CannotConnect(MideaLocalError):
    """Exception raised when connection fails."""


class DataUnexpectedLength(MideaLocalError):
    """Exception raised when data length is less or more than expected."""


class DataSignDoesntMatch(MideaLocalError):
    """Exception raised when data sign is not matching."""


class DataSignWrongType(MideaLocalError):
    """Exception raised when data is the wrong type to sign."""


class ElementMissing(MideaLocalError):
    """Exception raised when a element is missing."""


class MessageWrongFormat(MideaLocalError):
    """Exception raised when message format is wrong."""


class SocketException(MideaLocalError):
    """Exception raise by socket error."""


class ValueWrongType(MideaLocalError):
    """Exception raised when the value has a wrong data type."""
