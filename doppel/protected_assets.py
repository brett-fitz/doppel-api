"""Protected assets resource — sync and async access to Doppel protected asset endpoints."""

from __future__ import annotations

from doppel._resource import AsyncAPIResource, SyncAPIResource
from doppel.models.protected_assets import (
    ProtectedAssetCreateResponse,
    ProtectedAssetsListResponse,
)


__all__ = ["AsyncProtectedAssets", "ProtectedAssets"]


class ProtectedAssets(SyncAPIResource):
    """Synchronous resource for protected asset operations."""

    def list(
        self,
        *,
        platform_name: str | None = None,
        brand_ids: list[str] | None = None,
        brand_names: list[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ProtectedAssetsListResponse:
        """List protected assets.

        Args:
            platform_name: Filter by platform (e.g. ``"linkedin"``).
            brand_ids: Filter by brand IDs (max 100).
            brand_names: Filter by brand names (max 100).
            limit: Maximum results (default 100, max 1000).
            offset: Number of results to skip.

        Returns:
            List of protected assets with count.
        """
        params = self._client._build_params(
            platform_name=platform_name,
            brand_ids=brand_ids,
            brand_names=brand_names,
            limit=limit,
            offset=offset,
        )
        resp = self._client._request("GET", "/protected-assets", params=params)
        return ProtectedAssetsListResponse.model_validate(resp.json())

    def create(
        self,
        *,
        brand_ids: list[str],
        asset_value: str,
    ) -> ProtectedAssetCreateResponse:
        """Create a new protected asset.

        Args:
            brand_ids: Brand IDs to associate with the asset.
            asset_value: The URL, handle, or identifier to protect.

        Returns:
            The created asset with a confirmation message.
        """
        body = {"brand_ids": brand_ids, "asset_value": asset_value}
        resp = self._client._request("POST", "/protected-asset", json=body)
        return ProtectedAssetCreateResponse.model_validate(resp.json())


class AsyncProtectedAssets(AsyncAPIResource):
    """Asynchronous resource for protected asset operations."""

    async def list(
        self,
        *,
        platform_name: str | None = None,
        brand_ids: list[str] | None = None,
        brand_names: list[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ProtectedAssetsListResponse:
        """List protected assets."""
        params = self._client._build_params(
            platform_name=platform_name,
            brand_ids=brand_ids,
            brand_names=brand_names,
            limit=limit,
            offset=offset,
        )
        resp = await self._client._request("GET", "/protected-assets", params=params)
        return ProtectedAssetsListResponse.model_validate(resp.json())

    async def create(
        self,
        *,
        brand_ids: list[str],
        asset_value: str,
    ) -> ProtectedAssetCreateResponse:
        """Create a new protected asset."""
        body = {"brand_ids": brand_ids, "asset_value": asset_value}
        resp = await self._client._request("POST", "/protected-asset", json=body)
        return ProtectedAssetCreateResponse.model_validate(resp.json())
