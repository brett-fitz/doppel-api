"""Reports resource — sync and async access to deprecated Doppel report endpoints."""

from __future__ import annotations

from typing import Any
import warnings

from doppel._resource import AsyncAPIResource, SyncAPIResource
from doppel.models.reports import ReportResponse


__all__ = ["AsyncReports", "Reports"]

_DEPRECATION_MSG = (
    "The Doppel Reports API is deprecated. Use the Alerts API instead. "
    "See https://doppel.readme.io/reference/ for details."
)


class Reports(SyncAPIResource):
    """Synchronous resource for report operations (deprecated)."""

    def submit(
        self,
        *,
        url: str,
        **kwargs: Any,
    ) -> ReportResponse:
        """Submit a new report (deprecated).

        .. deprecated::
            Use :meth:`Alerts.create` instead.

        Args:
            url: URL to report.
            **kwargs: Additional fields for the request body.

        Returns:
            The created report.
        """
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        body: dict[str, Any] = {"url": url, **kwargs}
        resp = self._client._request("POST", "/report", json=body)
        return ReportResponse.model_validate(resp.json())

    def get(
        self,
        *,
        url: str | None = None,
        id: str | None = None,
        display_id: str | None = None,
    ) -> ReportResponse:
        """Retrieve a report by URL, ID, or display ID (deprecated).

        .. deprecated::
            Use :meth:`Alerts.get` instead.

        Args:
            url: The reported URL.
            id: The report ID.
            display_id: The report's display ID.

        Returns:
            Full report details.
        """
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(url=url, id=id, display_id=display_id)
        resp = self._client._request("GET", "/report", params=params)
        return ReportResponse.model_validate(resp.json())

    def update(
        self,
        *,
        url: str | None = None,
        id: str | None = None,
        display_id: str | None = None,
        **kwargs: Any,
    ) -> ReportResponse:
        """Update a report (deprecated).

        .. deprecated::
            Use :meth:`Alerts.update` instead.

        Args:
            url: The reported URL.
            id: The report ID.
            display_id: The report's display ID.
            **kwargs: Fields to update in the request body.

        Returns:
            Updated report details.
        """
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(url=url, id=id, display_id=display_id)
        resp = self._client._request("PUT", "/report", params=params, json=kwargs)
        return ReportResponse.model_validate(resp.json())

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """List reports (deprecated).

        .. deprecated::
            Use :meth:`Alerts.list` instead.

        Args:
            page: Page number.
            page_size: Results per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated list of reports.
        """
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(page=page, page_size=page_size, **kwargs)
        resp = self._client._request("GET", "/reports", params=params)
        return resp.json()


class AsyncReports(AsyncAPIResource):
    """Asynchronous resource for report operations (deprecated)."""

    async def submit(
        self,
        *,
        url: str,
        **kwargs: Any,
    ) -> ReportResponse:
        """Submit a new report (deprecated)."""
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        body: dict[str, Any] = {"url": url, **kwargs}
        resp = await self._client._request("POST", "/report", json=body)
        return ReportResponse.model_validate(resp.json())

    async def get(
        self,
        *,
        url: str | None = None,
        id: str | None = None,
        display_id: str | None = None,
    ) -> ReportResponse:
        """Retrieve a report by URL, ID, or display ID (deprecated)."""
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(url=url, id=id, display_id=display_id)
        resp = await self._client._request("GET", "/report", params=params)
        return ReportResponse.model_validate(resp.json())

    async def update(
        self,
        *,
        url: str | None = None,
        id: str | None = None,
        display_id: str | None = None,
        **kwargs: Any,
    ) -> ReportResponse:
        """Update a report (deprecated)."""
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(url=url, id=id, display_id=display_id)
        resp = await self._client._request("PUT", "/report", params=params, json=kwargs)
        return ReportResponse.model_validate(resp.json())

    async def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """List reports (deprecated)."""
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        params = self._client._build_params(page=page, page_size=page_size, **kwargs)
        resp = await self._client._request("GET", "/reports", params=params)
        return resp.json()
