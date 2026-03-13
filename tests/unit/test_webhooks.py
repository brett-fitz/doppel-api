import pytest

from doppel.models.webhooks import (
    AlertUpdatedEvent,
    IOCUpdatedEvent,
    ReportSurfacedEvent,
    SMSResponseEvent,
    UrlSurfacedEvent,
)
from doppel.webhooks import parse_webhook


class TestParseWebhook:
    def test_report_surfaced(self):
        payload = {
            "event_type": "report_surfaced",
            "payload": {
                "report_id": "abc-123",
                "display_id": "TST-100",
                "doppel_url": "https://app.doppel.com/domains/TST-100",
                "timestamp": "2025-01-15T10:00:00Z",
                "urls": ["https://evil.com"],
            },
        }
        event = parse_webhook(payload)
        assert isinstance(event, ReportSurfacedEvent)
        assert event.payload.report_id == "abc-123"
        assert event.payload.urls == ["https://evil.com"]

    def test_alert_updated(self):
        payload = {
            "event_type": "alert_updated",
            "timestamp": "2025-01-15T10:00:00Z",
            "updated_values": {"queue_state": "monitoring"},
            "initial_values": {"queue_state": "doppel_review"},
            "alert": {
                "id": "TST-200",
                "doppel_link": "https://app.doppel.com/domains/TST-200",
                "created_at": "2025-01-10T08:00:00Z",
                "entity": "https://phish.com",
                "entity_state": "active",
                "queue_state": "monitoring",
                "severity": "high",
                "product": "domains",
                "source": "API Upload",
                "notes": "",
                "uploaded_by": "user@test.com",
                "tags": [{"name": "phishing"}],
            },
        }
        event = parse_webhook(payload)
        assert isinstance(event, AlertUpdatedEvent)
        assert event.alert.id == "TST-200"
        assert event.updated_values.queue_state == "monitoring"
        assert event.initial_values.queue_state == "doppel_review"

    def test_sms_response(self):
        payload = {
            "event_type": "sms_response",
            "payload": {
                "message_sid": "SM12345",
                "from_number": "+1234567890",
                "to_number": "+1987654321",
                "body": "Yes I got the phishing email",
                "timestamp": "2025-01-15T10:00:00Z",
                "campaign_id": "campaign_q1",
            },
        }
        event = parse_webhook(payload)
        assert isinstance(event, SMSResponseEvent)
        assert event.payload.message_sid == "SM12345"
        assert event.payload.campaign_id == "campaign_q1"

    def test_url_surfaced(self):
        payload = {
            "event_type": "url_surfaced",
            "payload": {
                "url": "https://evil.com/login",
                "report_id": "rpt-42",
                "doppel_url": "https://app.doppel.com/domains/rpt-42",
                "timestamp": "2025-02-20T14:30:00Z",
            },
        }
        event = parse_webhook(payload)
        assert isinstance(event, UrlSurfacedEvent)
        assert event.payload.url == "https://evil.com/login"
        assert event.payload.report_id == "rpt-42"

    def test_ioc_updated_unwrapped(self):
        payload = {
            "id": "ioc-1",
            "created_at": "2025-01-15T10:00:00Z",
            "type": "LINK",
            "indicator": "evil.com",
            "status": "MALICIOUS",
        }
        event = parse_webhook(payload)
        assert isinstance(event, IOCUpdatedEvent)
        assert event.event_type == "ioc_updated"
        assert event.payload.indicator == "evil.com"
        assert event.payload.status == "MALICIOUS"

    def test_unknown_event_type_raises(self):
        with pytest.raises(ValueError, match="Unrecognised webhook event type"):
            parse_webhook({"event_type": "unknown_event"})

    def test_no_event_type_no_indicator_raises(self):
        with pytest.raises(ValueError, match="Unrecognised webhook event type"):
            parse_webhook({"some_field": "value"})

    def test_alert_updated_with_credential_data(self):
        payload = {
            "event_type": "alert_updated",
            "timestamp": "2025-01-15T10:00:00Z",
            "updated_values": {},
            "initial_values": {},
            "alert": {
                "id": "TST-300",
                "doppel_link": "https://app.doppel.com/domains/TST-300",
                "created_at": "2025-01-10T08:00:00Z",
                "entity": "https://darkweb.com",
                "entity_state": "active",
                "queue_state": "doppel_review",
                "severity": "high",
                "product": "darkweb",
                "source": "Dark Web Feed",
                "notes": "",
                "uploaded_by": "Doppel",
                "tags": [],
                "credential_data": {
                    "credential_url": "http://onion.example",
                    "network": "ONION.V2",
                    "email": "victim@test.com",
                    "password": "leaked123",
                },
                "has_credit_card_data": True,
            },
        }
        event = parse_webhook(payload)
        assert isinstance(event, AlertUpdatedEvent)
        assert event.alert.credential_data is not None
        assert event.alert.credential_data.email == "victim@test.com"
        assert event.alert.has_credit_card_data is True
