"""Brands resource — sync and async access to Doppel brand endpoints."""

from __future__ import annotations

from doppel._resource import AsyncAPIResource, SyncAPIResource
from doppel.models.brands import BrandsListResponse


__all__ = ["AsyncBrands", "Brands"]


class Brands(SyncAPIResource):
    """Synchronous resource for brand operations."""

    def list(
        self,
        *,
        brand_type: str | None = None,
        brand_name: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BrandsListResponse:
        """List active brands.

        Args:
            brand_type: Filter by brand type.
            brand_name: Filter by brand name.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            List of brands with count.
        """
        params = self._client._build_params(
            brand_type=brand_type,
            brand_name=brand_name,
            limit=limit,
            offset=offset,
        )
        resp = self._client._request("GET", "/brands", params=params)
        return BrandsListResponse.model_validate(resp.json())


class AsyncBrands(AsyncAPIResource):
    """Asynchronous resource for brand operations."""

    async def list(
        self,
        *,
        brand_type: str | None = None,
        brand_name: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BrandsListResponse:
        """List active brands."""
        params = self._client._build_params(
            brand_type=brand_type,
            brand_name=brand_name,
            limit=limit,
            offset=offset,
        )
        resp = await self._client._request("GET", "/brands", params=params)
        return BrandsListResponse.model_validate(resp.json())
