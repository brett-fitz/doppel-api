import httpx
import pytest
import respx

from doppel.client import AsyncDoppel
from doppel.models.alerts import AlertCreatedResponse, AlertResponse, AlertsListResponse

from .conftest import BASE_URL


class TestAsyncAlertsResource:
    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_create(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.post("/alert").mock(
            return_value=httpx.Response(
                201,
                json={"id": "TST-1", "entity": "https://evil.com", "doppel_link": "..."},
            )
        )
        result = await async_client.alerts.create(entity="https://evil.com")
        assert isinstance(result, AlertCreatedResponse)
        assert result.id == "TST-1"

    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_get_by_id(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.get("/alert").mock(
            return_value=httpx.Response(
                200,
                json={"id": "TST-2", "entity": "https://evil.com", "tags": []},
            )
        )
        result = await async_client.alerts.get(id="TST-2")
        assert isinstance(result, AlertResponse)
        assert result.id == "TST-2"

    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_update(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.put("/alert").mock(
            return_value=httpx.Response(
                200,
                json={"id": "TST-3", "queue_state": "monitoring", "tags": []},
            )
        )
        result = await async_client.alerts.update(id="TST-3", queue_state="monitoring")
        assert isinstance(result, AlertResponse)
        assert result.queue_state == "monitoring"

    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_list(self, respx_mock: respx.MockRouter, async_client: AsyncDoppel):
        respx_mock.get("/alerts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {"alerts": [{"id": "A-1", "tags": []}]},
                    "metadata": {"count": 1, "page": 0, "pages": 1, "page_size": 30},
                },
            )
        )
        result = await async_client.alerts.list(queue_state="monitoring")
        assert isinstance(result, AlertsListResponse)
        assert len(result.data.alerts) == 1

    @pytest.mark.asyncio
    @respx.mock(base_url=BASE_URL)
    async def test_submit_referrer_logs(
        self, respx_mock: respx.MockRouter, async_client: AsyncDoppel
    ):
        respx_mock.post("/alert/referrer").mock(return_value=httpx.Response(202, json={}))
        await async_client.alerts.submit_referrer_logs(
            referrer_url="https://google.com",
            destination_url="https://evil.com",
        )
