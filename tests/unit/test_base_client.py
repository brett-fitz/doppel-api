import httpx
import pytest

from doppel._base_client import (
    AsyncAPIClient,
    SyncAPIClient,
    _BaseClient,
    _DoppelAuth,
)
from doppel.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestDoppelAuth:
    def test_auth_sets_headers(self):
        auth = _DoppelAuth(
            api_key="gw-key",
            user_api_key="user-key",
            organization_code="my-org",
        )
        request = httpx.Request("GET", "https://example.com")
        flow = auth.auth_flow(request)
        modified = next(flow)
        assert modified.headers["x-api-key"] == "gw-key"
        assert modified.headers["x-user-api-key"] == "user-key"
        assert modified.headers["x-organization-code"] == "my-org"

    def test_auth_without_org_code(self):
        auth = _DoppelAuth(api_key="gw-key", user_api_key="user-key")
        request = httpx.Request("GET", "https://example.com")
        flow = auth.auth_flow(request)
        modified = next(flow)
        assert modified.headers["x-api-key"] == "gw-key"
        assert modified.headers["x-user-api-key"] == "user-key"
        assert "x-organization-code" not in modified.headers


class TestBaseClientBuildParams:
    def test_filters_none_values(self):
        result = _BaseClient._build_params(a="1", b=None, c=3)
        assert result == {"a": "1", "c": 3}

    def test_empty_when_all_none(self):
        result = _BaseClient._build_params(x=None, y=None)
        assert result == {}


class TestCheckResponse:
    def _make_client(self) -> SyncAPIClient:
        return SyncAPIClient(api_key="k", user_api_key="u")

    def test_success_passes(self):
        client = self._make_client()
        resp = httpx.Response(200, json={"ok": True})
        client._check_response(resp)

    def test_400_raises_validation_error(self):
        client = self._make_client()
        resp = httpx.Response(400, json={"message": "bad input"})
        with pytest.raises(ValidationError) as exc_info:
            client._check_response(resp)
        assert exc_info.value.status_code == 400
        assert "bad input" in str(exc_info.value)

    def test_401_raises_authentication_error(self):
        client = self._make_client()
        resp = httpx.Response(401, json={"message": "invalid key"})
        with pytest.raises(AuthenticationError):
            client._check_response(resp)

    def test_404_raises_not_found(self):
        client = self._make_client()
        resp = httpx.Response(404, json={"message": "not found"})
        with pytest.raises(NotFoundError):
            client._check_response(resp)

    def test_429_includes_retry_after(self):
        client = self._make_client()
        resp = httpx.Response(
            429,
            json={"message": "rate limited"},
            headers={"Retry-After": "30"},
        )
        with pytest.raises(RateLimitError) as exc_info:
            client._check_response(resp)
        assert exc_info.value.retry_after == 30.0

    def test_500_raises_server_error(self):
        client = self._make_client()
        resp = httpx.Response(500, json={"message": "internal error"})
        with pytest.raises(ServerError):
            client._check_response(resp)

    def test_detail_list_format(self):
        client = self._make_client()
        resp = httpx.Response(
            422,
            json={"detail": [{"msg": "field required", "loc": ["body", "entity"]}]},
        )
        with pytest.raises(Exception) as exc_info:
            client._check_response(resp)
        assert "field required" in str(exc_info.value)

    def test_non_json_body(self):
        client = self._make_client()
        resp = httpx.Response(500, text="Server Error")
        with pytest.raises(ServerError) as exc_info:
            client._check_response(resp)
        assert exc_info.value.response_body == "Server Error"


class TestSyncClientContextManager:
    def test_context_manager(self):
        with SyncAPIClient(api_key="k", user_api_key="u") as client:
            assert client is not None


class TestAsyncClientInit:
    def test_creates_instance(self):
        client = AsyncAPIClient(api_key="k", user_api_key="u")
        assert client._base_url == "https://api.doppel.com/v1"
