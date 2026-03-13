"""Webhook payload models for events pushed by Doppel."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


__all__ = [
    "AlertDarkWebCredentialData",
    "AlertUpdatedEvent",
    "AlertUpdatedPayload",
    "IOCUpdatedEvent",
    "IOCUpdatedPayload",
    "ReportSurfacedEvent",
    "ReportSurfacedPayload",
    "SMSResponseEvent",
    "SMSResponseMetadata",
    "SMSResponsePayload",
    "UrlSurfacedEvent",
    "UrlSurfacedPayload",
    "WebhookEvent",
]


# --------------------------------------------------------------------- #
# Report surfaced
# --------------------------------------------------------------------- #


class UrlSurfacedPayload(BaseModel):
    """A single URL surfaced within a report."""

    model_config = ConfigDict(extra="allow")

    url: str
    report_id: str
    doppel_url: str
    timestamp: datetime


class UrlSurfacedEvent(BaseModel):
    """Top-level envelope for a ``url_surfaced`` webhook."""

    model_config = ConfigDict(extra="allow")

    event_type: str
    payload: UrlSurfacedPayload


class ReportSurfacedPayload(BaseModel):
    """Payload for the ``report_surfaced`` webhook event."""

    model_config = ConfigDict(extra="allow")

    report_id: str
    display_id: str
    doppel_url: str
    timestamp: datetime
    urls: list[str] = Field(default_factory=list)


class ReportSurfacedEvent(BaseModel):
    """Top-level envelope for a ``report_surfaced`` webhook."""

    model_config = ConfigDict(extra="allow")

    event_type: str
    payload: ReportSurfacedPayload


# --------------------------------------------------------------------- #
# Alert updated
# --------------------------------------------------------------------- #


class AlertDarkWebCredentialData(BaseModel):
    """Credential data attached to a dark web alert."""

    model_config = ConfigDict(extra="allow")

    credential_url: str | None = None
    network: str | None = None
    email: str | None = None
    password: str | None = None


class AlertUpdatedPayload(BaseModel):
    """Payload describing the alert that was updated."""

    model_config = ConfigDict(extra="allow")

    id: str
    doppel_link: str
    created_at: datetime
    entity: str
    entity_state: str
    queue_state: str
    severity: str
    product: str
    source: str
    notes: str
    uploaded_by: str
    tags: list[dict[str, str]] = Field(default_factory=list)
    brand: str | None = None
    credential_data: AlertDarkWebCredentialData | None = None
    has_credit_card_data: bool | None = None


class _AlertUpdateValues(BaseModel):
    """Key-value pairs of fields that changed on an alert update."""

    model_config = ConfigDict(extra="allow")

    queue_state: str | None = None
    entity_state: str | None = None
    notes: str | None = None
    tag_add: str | None = None
    tag_remove: str | None = None
    file_action: str | None = None
    severity: str | None = None


class AlertUpdatedEvent(BaseModel):
    """Top-level envelope for an ``alert_updated`` webhook."""

    model_config = ConfigDict(extra="allow")

    event_type: str
    timestamp: datetime
    updated_values: _AlertUpdateValues
    initial_values: _AlertUpdateValues
    alert: AlertUpdatedPayload


# --------------------------------------------------------------------- #
# SMS response
# --------------------------------------------------------------------- #


class SMSResponseMetadata(BaseModel):
    """Metadata about an SMS response."""

    model_config = ConfigDict(extra="allow")

    message_type: str | None = None
    num_media: int | None = None
    media_urls: list[str] = Field(default_factory=list)


class SMSResponsePayload(BaseModel):
    """Payload for the ``sms_response`` webhook event."""

    model_config = ConfigDict(extra="allow")

    message_sid: str
    from_number: str
    to_number: str
    body: str
    timestamp: datetime
    campaign_id: str
    user_id: str | None = None
    metadata: SMSResponseMetadata | None = None


class SMSResponseEvent(BaseModel):
    """Top-level envelope for an ``sms_response`` webhook."""

    model_config = ConfigDict(extra="allow")

    event_type: str
    payload: SMSResponsePayload


# --------------------------------------------------------------------- #
# IOC updated
# --------------------------------------------------------------------- #


class IOCUpdatedPayload(BaseModel):
    """Payload for the ``ioc_updated`` webhook event.

    Note: This webhook requires contacting Doppel to subscribe.
    """

    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime
    type: str
    indicator: str
    status: str


class IOCUpdatedEvent(BaseModel):
    """Top-level envelope for an ``ioc_updated`` webhook.

    Unlike other webhooks, the ``ioc_updated`` event sends the payload
    directly without the standard ``{event_type, payload}`` wrapper.
    This model wraps it for consistency with the other event types.
    """

    model_config = ConfigDict(extra="allow")

    event_type: str = "ioc_updated"
    payload: IOCUpdatedPayload


# --------------------------------------------------------------------- #
# Union type
# --------------------------------------------------------------------- #

WebhookEvent = (
    AlertUpdatedEvent | IOCUpdatedEvent | ReportSurfacedEvent | SMSResponseEvent | UrlSurfacedEvent
)
"""Union of all supported Doppel webhook event types."""
