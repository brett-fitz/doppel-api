"""Webhook parsing utilities for Doppel events.

Provides a lightweight ``parse_webhook`` function that validates and
deserialises inbound JSON payloads into typed Pydantic models.  No
framework dependency — bring your own server (FastAPI, Flask, etc.).

Usage::

    from doppel.webhooks import parse_webhook

    event = parse_webhook(request.json())
    # event is one of the WebhookEvent union members
"""

from __future__ import annotations

from typing import Any

from doppel.models.webhooks import (
    AlertUpdatedEvent,
    IOCUpdatedEvent,
    IOCUpdatedPayload,
    ReportSurfacedEvent,
    SMSResponseEvent,
    UrlSurfacedEvent,
    WebhookEvent,
)


__all__ = ["parse_webhook"]

_EVENT_TYPE_MAP: dict[
    str,
    type[AlertUpdatedEvent | ReportSurfacedEvent | SMSResponseEvent | UrlSurfacedEvent],
] = {
    "alert_updated": AlertUpdatedEvent,
    "report_surfaced": ReportSurfacedEvent,
    "sms_response": SMSResponseEvent,
    "url_surfaced": UrlSurfacedEvent,
}


def parse_webhook(payload: dict[str, Any]) -> WebhookEvent:
    """Parse a raw webhook payload into a typed event model.

    The function inspects the ``event_type`` field to determine which
    model to use.  For ``ioc_updated`` events, which lack the standard
    ``{event_type, payload}`` wrapper, the payload is detected by the
    presence of an ``indicator`` field and absence of ``event_type``.

    Args:
        payload: Raw JSON payload (already deserialised to a dict).

    Returns:
        A validated webhook event model.

    Raises:
        ValueError: If the event type is unrecognised.
    """
    event_type = payload.get("event_type")

    if event_type and event_type in _EVENT_TYPE_MAP:
        return _EVENT_TYPE_MAP[event_type].model_validate(payload)

    if event_type is None and "indicator" in payload:
        ioc_payload = IOCUpdatedPayload.model_validate(payload)
        return IOCUpdatedEvent(payload=ioc_payload)

    raise ValueError(
        f"Unrecognised webhook event type: {event_type!r}. "
        f"Supported types: {sorted(_EVENT_TYPE_MAP)}"
    )
