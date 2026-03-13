import httpx
import pytest
import respx

from doppel.client import AsyncDoppel
from doppel.models.protected_assets import (
    ProtectedAssetCreateResponse,
    ProtectedAssetsListResponse,
)

from .conftest import BASE_URL


class TestAsyncProtectedAssetsResource:
    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_list(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.get("/protected-assets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "pa-1",
                            "brand_ids": ["b-1"],
                            "platform": "linkedin",
                            "asset_value": "https://linkedin.com/company/acme",
                        }
                    ],
                    "count": 1,
                },
            )
        )
        result = await async_client.protected_assets.list()
        assert isinstance(result, ProtectedAssetsListResponse)
        assert result.count == 1
        assert result.data[0].platform == "linkedin"

    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_create(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.post("/protected-asset").mock(
            return_value=httpx.Response(
                201,
                json={
                    "data": {
                        "id": "pa-2",
                        "brand_ids": ["b-1"],
                        "asset_value": "https://example.com",
                    },
                    "message": "Created",
                },
            )
        )
        result = await async_client.protected_assets.create(
            brand_ids=["b-1"],
            asset_value="https://example.com",
        )
        assert isinstance(result, ProtectedAssetCreateResponse)
        assert result.data.id == "pa-2"
        assert result.message == "Created"
