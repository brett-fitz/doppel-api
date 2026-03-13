"""Alerts resource — sync and async access to Doppel alert endpoints."""

from __future__ import annotations

from typing import Any

from doppel._resource import AsyncAPIResource, SyncAPIResource
from doppel.models.alerts import (
    AlertCreatedResponse,
    AlertResponse,
    AlertsListResponse,
    FileInput,
)


__all__ = ["Alerts", "AsyncAlerts"]


class Alerts(SyncAPIResource):
    """Synchronous resource for alert operations."""

    def create(
        self,
        *,
        entity: str,
        brand: str | None = None,
        tags: list[str] | None = None,
        source: str | None = None,
        files: list[FileInput] | None = None,
    ) -> AlertCreatedResponse:
        """Create an alert for a URL or phone number.

        Args:
            entity: URL or phone number to alert on.
            brand: Brand name to associate with the alert.
            tags: Tag names to associate (must already exist).
            source: Custom API source identifier.
            files: Files to upload with the alert (max 10).

        Returns:
            The created (or existing) alert summary.
        """
        body: dict[str, Any] = {"entity": entity}
        if brand is not None:
            body["brand"] = brand
        if tags is not None:
            body["tags"] = tags
        if source is not None:
            body["source"] = source
        if files is not None:
            body["files"] = [f.model_dump(exclude_none=True) for f in files]
        resp = self._client._request("POST", "/alert", json=body)
        return AlertCreatedResponse.model_validate(resp.json())

    def get(
        self,
        *,
        id: str | None = None,
        entity: str | None = None,
    ) -> AlertResponse:
        """Retrieve an alert by ID or entity.

        Exactly one of ``id`` or ``entity`` must be provided.

        Args:
            id: Alert identifier (e.g. ``"TST-1234"``).
            entity: URL or phone number of the alert.

        Returns:
            Full alert details.
        """
        params = self._client._build_params(id=id, entity=entity)
        resp = self._client._request("GET", "/alert", params=params)
        return AlertResponse.model_validate(resp.json())

    def update(
        self,
        *,
        id: str | None = None,
        entity: str | None = None,
        queue_state: str | None = None,
        entity_state: str | None = None,
        comment: str | None = None,
        tag_action: str | None = None,
        tag_name: str | None = None,
        file_action: str | None = None,
        files: list[FileInput] | None = None,
        screenshot: str | None = None,
    ) -> AlertResponse:
        """Update an alert identified by ID or entity.

        Args:
            id: Alert identifier.
            entity: URL or phone number of the alert.
            queue_state: New queue state.
            entity_state: New entity state.
            comment: Comment to add.
            tag_action: ``"add"`` or ``"remove"``.
            tag_name: Tag name to add or remove.
            file_action: ``"upload"`` or ``"delete"``.
            files: Files for the file action (max 10).
            screenshot: Base64-encoded screenshot (PNG/JPEG).

        Returns:
            Updated alert details.
        """
        params = self._client._build_params(id=id, entity=entity)
        body: dict[str, Any] = {}
        if queue_state is not None:
            body["queue_state"] = queue_state
        if entity_state is not None:
            body["entity_state"] = entity_state
        if comment is not None:
            body["comment"] = comment
        if tag_action is not None:
            body["tag_action"] = tag_action
        if tag_name is not None:
            body["tag_name"] = tag_name
        if file_action is not None:
            body["file_action"] = file_action
        if files is not None:
            body["files"] = [f.model_dump(exclude_none=True) for f in files]
        if screenshot is not None:
            body["screenshot"] = screenshot
        resp = self._client._request("PUT", "/alert", params=params, json=body)
        return AlertResponse.model_validate(resp.json())

    def list(
        self,
        *,
        search_key: str | None = None,
        queue_state: str | None = None,
        product: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        last_activity_timestamp: str | None = None,
        sort_type: str | None = None,
        sort_order: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        tags: list[str] | None = None,
    ) -> AlertsListResponse:
        """List alerts with optional filtering, sorting, and pagination.

        Args:
            search_key: Search by URL.
            queue_state: Filter by queue state.
            product: Filter by product category.
            created_before: Alerts created before this datetime.
            created_after: Alerts created after this datetime.
            last_activity_timestamp: Alerts with activity on or after this datetime.
            sort_type: Field to sort by (``date_sourced`` or ``date_last_actioned``).
            sort_order: ``asc`` or ``desc``.
            page: Page number (default 0).
            page_size: Results per page (default 30, max 200).
            tags: Filter by tag names.

        Returns:
            Paginated list of alerts.
        """
        params = self._client._build_params(
            search_key=search_key,
            queue_state=queue_state,
            product=product,
            created_before=created_before,
            created_after=created_after,
            last_activity_timestamp=last_activity_timestamp,
            sort_type=sort_type,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
            tags=tags,
        )
        resp = self._client._request("GET", "/alerts", params=params)
        return AlertsListResponse.model_validate(resp.json())

    def submit_referrer_logs(
        self,
        *,
        referrer_url: str,
        destination_url: str,
    ) -> None:
        """Submit referrer logs for an alert.

        Args:
            referrer_url: The referring URL.
            destination_url: The destination URL.
        """
        body = {"referrer_url": referrer_url, "destination_url": destination_url}
        self._client._request("POST", "/alert/referrer", json=body)


class AsyncAlerts(AsyncAPIResource):
    """Asynchronous resource for alert operations."""

    async def create(
        self,
        *,
        entity: str,
        brand: str | None = None,
        tags: list[str] | None = None,
        source: str | None = None,
        files: list[FileInput] | None = None,
    ) -> AlertCreatedResponse:
        """Create an alert for a URL or phone number."""
        body: dict[str, Any] = {"entity": entity}
        if brand is not None:
            body["brand"] = brand
        if tags is not None:
            body["tags"] = tags
        if source is not None:
            body["source"] = source
        if files is not None:
            body["files"] = [f.model_dump(exclude_none=True) for f in files]
        resp = await self._client._request("POST", "/alert", json=body)
        return AlertCreatedResponse.model_validate(resp.json())

    async def get(
        self,
        *,
        id: str | None = None,
        entity: str | None = None,
    ) -> AlertResponse:
        """Retrieve an alert by ID or entity."""
        params = self._client._build_params(id=id, entity=entity)
        resp = await self._client._request("GET", "/alert", params=params)
        return AlertResponse.model_validate(resp.json())

    async def update(
        self,
        *,
        id: str | None = None,
        entity: str | None = None,
        queue_state: str | None = None,
        entity_state: str | None = None,
        comment: str | None = None,
        tag_action: str | None = None,
        tag_name: str | None = None,
        file_action: str | None = None,
        files: list[FileInput] | None = None,
        screenshot: str | None = None,
    ) -> AlertResponse:
        """Update an alert identified by ID or entity."""
        params = self._client._build_params(id=id, entity=entity)
        body: dict[str, Any] = {}
        if queue_state is not None:
            body["queue_state"] = queue_state
        if entity_state is not None:
            body["entity_state"] = entity_state
        if comment is not None:
            body["comment"] = comment
        if tag_action is not None:
            body["tag_action"] = tag_action
        if tag_name is not None:
            body["tag_name"] = tag_name
        if file_action is not None:
            body["file_action"] = file_action
        if files is not None:
            body["files"] = [f.model_dump(exclude_none=True) for f in files]
        if screenshot is not None:
            body["screenshot"] = screenshot
        resp = await self._client._request("PUT", "/alert", params=params, json=body)
        return AlertResponse.model_validate(resp.json())

    async def list(
        self,
        *,
        search_key: str | None = None,
        queue_state: str | None = None,
        product: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        last_activity_timestamp: str | None = None,
        sort_type: str | None = None,
        sort_order: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        tags: list[str] | None = None,
    ) -> AlertsListResponse:
        """List alerts with optional filtering, sorting, and pagination."""
        params = self._client._build_params(
            search_key=search_key,
            queue_state=queue_state,
            product=product,
            created_before=created_before,
            created_after=created_after,
            last_activity_timestamp=last_activity_timestamp,
            sort_type=sort_type,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
            tags=tags,
        )
        resp = await self._client._request("GET", "/alerts", params=params)
        return AlertsListResponse.model_validate(resp.json())

    async def submit_referrer_logs(
        self,
        *,
        referrer_url: str,
        destination_url: str,
    ) -> None:
        """Submit referrer logs for an alert."""
        body = {"referrer_url": referrer_url, "destination_url": destination_url}
        await self._client._request("POST", "/alert/referrer", json=body)
