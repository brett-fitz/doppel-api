"""Report models and enums for the Doppel API (deprecated endpoints)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from doppel.models.alerts import AuditLog


__all__ = [
    "DomainMatch",
    "ReportClassification",
    "ReportResponse",
    "ReportStatus",
    "RootDomain",
]


class ReportStatus(StrEnum):
    """Status of which queue the report is in.

    Note: ``taken_down`` is equivalent to "Resolved" in the Doppel Vision app.
    """

    DOPPEL_REVIEW = "doppel_review"
    NEEDS_CONFIRMATION = "needs_confirmation"
    ACTIONED = "actioned"
    TAKEN_DOWN = "taken_down"
    MONITORING = "monitoring"
    ARCHIVED = "archived"


class ReportClassification(StrEnum):
    """Classification of a reported entity."""

    SUSPICIOUS = "suspicious"
    DOWN = "down"
    PARKED = "parked"
    ACTIVE = "active"


class RootDomain(BaseModel):
    """Root domain information associated with a report."""

    model_config = ConfigDict(extra="allow")

    domain: str | None = None
    registrar: str | None = None
    ip_address: str | None = None
    country_code: str | None = None
    hosting_provider: str | None = None


class DomainMatch(BaseModel):
    """A domain match found for a report."""

    model_config = ConfigDict(extra="allow")

    domain: dict[str, str] | None = None


class ReportResponse(BaseModel):
    """Report returned by the deprecated report endpoints."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    display_id: str | None = None
    submitted_url: str | None = None
    doppel_url: str | None = None
    report_status: str | None = None
    classification: str | None = None
    product: str | None = None
    source: str | None = None
    notes: str | None = None
    uploaded_by: str | None = None
    created_at: datetime | None = None
    matches: list[DomainMatch] = Field(default_factory=list)
    root_domain: RootDomain | None = None
    audit_logs: list[AuditLog] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def _normalize_tags(cls, v: list[str | dict[str, str]]) -> list[str]:
        """Normalise tag objects to plain strings."""
        return [t["name"] if isinstance(t, dict) else t for t in v]
