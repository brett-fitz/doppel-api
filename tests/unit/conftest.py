"""Shared test fixtures for doppel unit tests."""

import pytest
import respx

from doppel.client import AsyncDoppel, Doppel


BASE_URL = "https://api.doppel.com/v1"


@pytest.fixture
def sync_client() -> Doppel:
    """Return a synchronous Doppel client for testing."""
    return Doppel(api_key="test-gw-key", user_api_key="test-user-key")


@pytest.fixture
def async_client() -> AsyncDoppel:
    """Return an async Doppel client for testing."""
    return AsyncDoppel(api_key="test-gw-key", user_api_key="test-user-key")


@pytest.fixture
def mock_api() -> respx.MockRouter:
    """Return a respx mock router scoped to the base URL."""
    with respx.mock(base_url=BASE_URL) as router:
        yield router
