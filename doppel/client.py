"""Public Doppel client classes.

``Doppel`` provides synchronous access and ``AsyncDoppel`` provides
asynchronous access to the Doppel API.  Resource groups are exposed as
``@cached_property`` attributes (e.g. ``client.alerts``, ``client.brands``).
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

from doppel._base_client import _DEFAULT_BASE_URL, _DEFAULT_TIMEOUT, AsyncAPIClient, SyncAPIClient


if TYPE_CHECKING:
    from doppel.alerts import Alerts, AsyncAlerts
    from doppel.brands import AsyncBrands, Brands
    from doppel.protected_assets import AsyncProtectedAssets, ProtectedAssets
    from doppel.reports import AsyncReports, Reports

__all__ = ["AsyncDoppel", "Doppel"]


class Doppel(SyncAPIClient):
    """Synchronous Doppel API client.

    Authentication requires both an API key and a user API key, provided
    via the ``api_key`` and ``user_api_key`` parameters.  An optional
    ``organization_code`` can be supplied for multi-org accounts.

    Usage::

        from doppel import Doppel

        client = Doppel(api_key="gw-key", user_api_key="user-key")
        alert = client.alerts.get(id="TST-1234")
        client.close()

    Or as a context manager::

        with Doppel(api_key="gw-key", user_api_key="user-key") as client:
            brands = client.brands.list()
    """

    def __init__(  # noqa: D107
        self,
        *,
        api_key: str,
        user_api_key: str,
        organization_code: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        **httpx_client_kwargs: Any,
    ) -> None:
        super().__init__(
            api_key=api_key,
            user_api_key=user_api_key,
            organization_code=organization_code,
            base_url=base_url,
            timeout=timeout,
            **httpx_client_kwargs,
        )

    @cached_property
    def alerts(self) -> Alerts:
        """Alert operations (create, get, update, list, referrer logs)."""
        from doppel.alerts import Alerts

        return Alerts(self)

    @cached_property
    def brands(self) -> Brands:
        """Brand listing operations."""
        from doppel.brands import Brands

        return Brands(self)

    @cached_property
    def protected_assets(self) -> ProtectedAssets:
        """Protected asset operations (list, create)."""
        from doppel.protected_assets import ProtectedAssets

        return ProtectedAssets(self)

    @cached_property
    def reports(self) -> Reports:
        """Report operations (deprecated -- use alerts instead)."""
        from doppel.reports import Reports

        return Reports(self)


class AsyncDoppel(AsyncAPIClient):
    """Asynchronous Doppel API client.

    Usage::

        from doppel import AsyncDoppel

        async with AsyncDoppel(api_key="gw-key", user_api_key="user-key") as client:
            alert = await client.alerts.get(id="TST-1234")
    """

    def __init__(  # noqa: D107
        self,
        *,
        api_key: str,
        user_api_key: str,
        organization_code: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        **httpx_client_kwargs: Any,
    ) -> None:
        super().__init__(
            api_key=api_key,
            user_api_key=user_api_key,
            organization_code=organization_code,
            base_url=base_url,
            timeout=timeout,
            **httpx_client_kwargs,
        )

    @cached_property
    def alerts(self) -> AsyncAlerts:
        """Alert operations (create, get, update, list, referrer logs)."""
        from doppel.alerts import AsyncAlerts

        return AsyncAlerts(self)

    @cached_property
    def brands(self) -> AsyncBrands:
        """Brand listing operations."""
        from doppel.brands import AsyncBrands

        return AsyncBrands(self)

    @cached_property
    def protected_assets(self) -> AsyncProtectedAssets:
        """Protected asset operations (list, create)."""
        from doppel.protected_assets import AsyncProtectedAssets

        return AsyncProtectedAssets(self)

    @cached_property
    def reports(self) -> AsyncReports:
        """Report operations (deprecated -- use alerts instead)."""
        from doppel.reports import AsyncReports

        return AsyncReports(self)
