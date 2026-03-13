from datetime import datetime

from doppel.models.alerts import (
    AlertCreatedResponse,
    AlertResponse,
    AlertsListResponse,
    AuditLog,
    EntityState,
    FileActionType,
    FileInput,
    FileResult,
    PaginationMetadata,
    Product,
    QueueState,
    Severity,
    SortOrder,
    SortType,
    Tag,
    TagActionType,
)
from doppel.models.brands import BrandResponse, BrandsListResponse
from doppel.models.protected_assets import (
    Platform,
    ProtectedAssetCreateResponse,
    ProtectedAssetResponse,
    ProtectedAssetsListResponse,
)
from doppel.models.reports import (
    ReportClassification,
    ReportResponse,
    ReportStatus,
    RootDomain,
)


class TestAlertEnums:
    def test_queue_state_values(self):
        assert QueueState.DOPPEL_REVIEW == "doppel_review"
        assert QueueState.TAKEN_DOWN == "taken_down"
        assert len(QueueState) == 6

    def test_entity_state_values(self):
        assert EntityState.ACTIVE == "active"
        assert len(EntityState) == 3

    def test_severity_values(self):
        assert Severity.HIGH == "high"
        assert len(Severity) == 3

    def test_product_values(self):
        assert Product.DOMAINS == "domains"
        assert len(Product) == 9

    def test_tag_action_type(self):
        assert TagActionType.ADD == "add"
        assert TagActionType.REMOVE == "remove"

    def test_file_action_type(self):
        assert FileActionType.UPLOAD == "upload"
        assert FileActionType.DELETE == "delete"

    def test_sort_type(self):
        assert SortType.DATE_SOURCED == "date_sourced"

    def test_sort_order(self):
        assert SortOrder.ASC == "asc"
        assert SortOrder.DESC == "desc"


class TestAlertModels:
    def test_alert_response_minimal(self):
        alert = AlertResponse(id="TST-1234")
        assert alert.id == "TST-1234"
        assert alert.tags == []
        assert alert.audit_logs == []

    def test_alert_response_tag_normalization(self):
        alert = AlertResponse.model_validate(
            {
                "id": "TST-1",
                "tags": [{"name": "phishing"}, {"name": "urgent"}],
            }
        )
        assert alert.tags == ["phishing", "urgent"]

    def test_alert_response_string_tags(self):
        alert = AlertResponse.model_validate({"id": "TST-2", "tags": ["a", "b"]})
        assert alert.tags == ["a", "b"]

    def test_alert_response_extra_fields(self):
        alert = AlertResponse.model_validate({"id": "TST-3", "new_field": "value"})
        assert alert.id == "TST-3"

    def test_alert_created_response(self):
        resp = AlertCreatedResponse.model_validate(
            {
                "id": "TST-100",
                "entity": "https://phish.com",
                "doppel_link": "https://app.doppel.com/domains/TST-100",
                "message": "Alert already exists",
            }
        )
        assert resp.id == "TST-100"
        assert resp.message == "Alert already exists"

    def test_alerts_list_response(self):
        data = {
            "data": {"alerts": [{"id": "A-1"}, {"id": "A-2"}]},
            "metadata": {"count": 2, "page": 0, "pages": 1, "page_size": 30},
        }
        resp = AlertsListResponse.model_validate(data)
        assert len(resp.data.alerts) == 2
        assert resp.metadata.count == 2
        assert resp.metadata.page_size == 30

    def test_file_input(self):
        f = FileInput(file_name="evidence.png", file_to_upload="base64data")
        assert f.file_name == "evidence.png"

    def test_file_result(self):
        f = FileResult(file_name="x.png", success=True)
        assert f.success is True

    def test_tag_model(self):
        t = Tag(name="phishing")
        assert t.name == "phishing"

    def test_audit_log(self):
        log = AuditLog.model_validate(
            {
                "changed_by": "user@test.com",
                "value": "monitoring",
                "timestamp": "2025-01-15T10:00:00Z",
                "type": "queue_state",
            }
        )
        assert log.changed_by == "user@test.com"
        assert isinstance(log.timestamp, datetime)

    def test_pagination_metadata_defaults(self):
        p = PaginationMetadata()
        assert p.count == 0
        assert p.page == 0


class TestReportModels:
    def test_report_status_values(self):
        assert ReportStatus.DOPPEL_REVIEW == "doppel_review"
        assert len(ReportStatus) == 6

    def test_report_classification_values(self):
        assert ReportClassification.SUSPICIOUS == "suspicious"
        assert len(ReportClassification) == 4

    def test_report_response(self):
        r = ReportResponse.model_validate(
            {
                "id": "r-1",
                "display_id": "TST-100",
                "submitted_url": "https://evil.com",
                "tags": [{"name": "phishing"}],
            }
        )
        assert r.display_id == "TST-100"
        assert r.tags == ["phishing"]

    def test_root_domain(self):
        rd = RootDomain(domain="evil.com", registrar="GoDaddy")
        assert rd.domain == "evil.com"


class TestBrandModels:
    def test_brand_response(self):
        b = BrandResponse.model_validate(
            {
                "id": "b-1",
                "name": "Acme Corp",
                "brand_type": "corporate",
            }
        )
        assert b.name == "Acme Corp"

    def test_brands_list_response(self):
        r = BrandsListResponse.model_validate(
            {
                "data": [{"id": "b-1", "name": "Acme"}],
                "count": 1,
            }
        )
        assert r.count == 1
        assert len(r.data) == 1


class TestProtectedAssetModels:
    def test_platform_enum(self):
        assert Platform.LINKEDIN == "linkedin"
        assert len(Platform) == 40

    def test_protected_asset_response(self):
        pa = ProtectedAssetResponse.model_validate(
            {
                "id": "pa-1",
                "brand_ids": ["b-1"],
                "platform": "linkedin",
                "asset_value": "https://linkedin.com/company/acme",
            }
        )
        assert pa.platform == "linkedin"

    def test_protected_assets_list_response(self):
        r = ProtectedAssetsListResponse.model_validate(
            {
                "data": [{"id": "pa-1", "brand_ids": ["b-1"], "asset_value": "x"}],
                "count": 1,
            }
        )
        assert r.count == 1

    def test_create_response(self):
        r = ProtectedAssetCreateResponse.model_validate(
            {
                "data": {"id": "pa-2", "brand_ids": ["b-1"], "asset_value": "y"},
                "message": "Created successfully",
            }
        )
        assert r.message == "Created successfully"
        assert r.data.id == "pa-2"
