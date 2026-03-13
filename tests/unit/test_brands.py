import httpx
import respx

from doppel.client import Doppel
from doppel.models.brands import BrandsListResponse

from .conftest import BASE_URL


class TestBrandsResource:
    @respx.mock(base_url=BASE_URL)
    def test_list(self, respx_mock: respx.MockRouter, sync_client: Doppel):
        respx_mock.get("/brands").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"id": "b-1", "name": "Acme", "brand_type": "corporate"}],
                    "count": 1,
                },
            )
        )
        result = sync_client.brands.list()
        assert isinstance(result, BrandsListResponse)
        assert result.count == 1
        assert result.data[0].name == "Acme"

    @respx.mock(base_url=BASE_URL)
    def test_list_with_filters(self, respx_mock: respx.MockRouter, sync_client: Doppel):
        route = respx_mock.get("/brands").mock(
            return_value=httpx.Response(200, json={"data": [], "count": 0})
        )
        sync_client.brands.list(brand_type="corporate", limit=10)
        assert route.called
        assert "brand_type" in str(route.calls.last.request.url)
