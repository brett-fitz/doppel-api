import warnings

import httpx
import respx

from doppel.client import Doppel
from doppel.models.reports import ReportResponse

from .conftest import BASE_URL


class TestReportsResource:
    @respx.mock(base_url=BASE_URL)
    def test_submit_emits_deprecation_warning(
        self, respx_mock: respx.MockRouter, sync_client: Doppel
    ):
        respx_mock.post("/report").mock(
            return_value=httpx.Response(
                200,
                json={"id": "r-1", "display_id": "TST-100", "tags": []},
            )
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = sync_client.reports.submit(url="https://evil.com")
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()
        assert isinstance(result, ReportResponse)
        assert result.id == "r-1"

    @respx.mock(base_url=BASE_URL)
    def test_get(self, respx_mock: respx.MockRouter, sync_client: Doppel):
        respx_mock.get("/report").mock(
            return_value=httpx.Response(
                200,
                json={"id": "r-2", "display_id": "TST-200", "tags": []},
            )
        )
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = sync_client.reports.get(id="r-2")
        assert isinstance(result, ReportResponse)
        assert result.display_id == "TST-200"

    @respx.mock(base_url=BASE_URL)
    def test_update(self, respx_mock: respx.MockRouter, sync_client: Doppel):
        respx_mock.put("/report").mock(
            return_value=httpx.Response(
                200,
                json={"id": "r-3", "display_id": "TST-300", "tags": []},
            )
        )
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = sync_client.reports.update(id="r-3", report_status="monitoring")
        assert isinstance(result, ReportResponse)

    @respx.mock(base_url=BASE_URL)
    def test_list(self, respx_mock: respx.MockRouter, sync_client: Doppel):
        respx_mock.get("/reports").mock(
            return_value=httpx.Response(
                200,
                json={"data": [{"id": "r-1", "tags": []}], "count": 1},
            )
        )
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = sync_client.reports.list(page=0, page_size=10)
        assert isinstance(result, dict)
        assert result["count"] == 1
