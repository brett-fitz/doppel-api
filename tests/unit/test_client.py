from doppel.alerts import Alerts, AsyncAlerts
from doppel.brands import AsyncBrands, Brands
from doppel.client import AsyncDoppel, Doppel
from doppel.protected_assets import AsyncProtectedAssets, ProtectedAssets
from doppel.reports import AsyncReports, Reports


class TestDoppelClient:
    def test_has_alerts(self):
        client = Doppel(api_key="k", user_api_key="u")
        assert isinstance(client.alerts, Alerts)

    def test_has_brands(self):
        client = Doppel(api_key="k", user_api_key="u")
        assert isinstance(client.brands, Brands)

    def test_has_protected_assets(self):
        client = Doppel(api_key="k", user_api_key="u")
        assert isinstance(client.protected_assets, ProtectedAssets)

    def test_has_reports(self):
        client = Doppel(api_key="k", user_api_key="u")
        assert isinstance(client.reports, Reports)

    def test_cached_property_returns_same_instance(self):
        client = Doppel(api_key="k", user_api_key="u")
        assert client.alerts is client.alerts
        assert client.brands is client.brands

    def test_custom_base_url(self):
        client = Doppel(
            api_key="k",
            user_api_key="u",
            base_url="https://custom.api.com/v2",
        )
        assert client._base_url == "https://custom.api.com/v2"

    def test_organization_code(self):
        client = Doppel(
            api_key="k",
            user_api_key="u",
            organization_code="my-org",
        )
        assert client._auth._organization_code == "my-org"


class TestAsyncDoppelClient:
    def test_has_alerts(self):
        client = AsyncDoppel(api_key="k", user_api_key="u")
        assert isinstance(client.alerts, AsyncAlerts)

    def test_has_brands(self):
        client = AsyncDoppel(api_key="k", user_api_key="u")
        assert isinstance(client.brands, AsyncBrands)

    def test_has_protected_assets(self):
        client = AsyncDoppel(api_key="k", user_api_key="u")
        assert isinstance(client.protected_assets, AsyncProtectedAssets)

    def test_has_reports(self):
        client = AsyncDoppel(api_key="k", user_api_key="u")
        assert isinstance(client.reports, AsyncReports)
