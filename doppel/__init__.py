"""doppel — Modern Python Doppel client with sync and async support."""

from importlib.metadata import version

from doppel.client import AsyncDoppel, Doppel
from doppel.exceptions import (
    AuthenticationError,
    ConflictError,
    DoppelError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


__version__ = version("doppel-api")

__all__ = [
    "AsyncDoppel",
    "AuthenticationError",
    "ConflictError",
    "Doppel",
    "DoppelError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "__version__",
]
