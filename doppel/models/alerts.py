"""Alert models and enums for the Doppel API."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


__all__ = [
    "AlertCreatedResponse",
    "AlertResponse",
    "AlertsListResponse",
    "AuditLog",
    "AuditLogMetadata",
    "EntityState",
    "FileActionType",
    "FileInput",
    "FileResult",
    "PaginationMetadata",
    "Product",
    "QueueState",
    "Severity",
    "SortOrder",
    "SortType",
    "Tag",
    "TagActionType",
]


class QueueState(StrEnum):
    """Status of which queue the alert is in.

    Note: ``taken_down`` is equivalent to "Resolved" in the Doppel Vision app.
    """

    DOPPEL_REVIEW = "doppel_review"
    NEEDS_CONFIRMATION = "needs_confirmation"
    ACTIONED = "actioned"
    TAKEN_DOWN = "taken_down"
    MONITORING = "monitoring"
    ARCHIVED = "archived"


class EntityState(StrEnum):
    """State of the entity identified by the alert."""

    ACTIVE = "active"
    DOWN = "down"
    PARKED = "parked"


class Severity(StrEnum):
    """Severity level of the alert."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Product(StrEnum):
    """Product category the alert belongs to."""

    DOMAINS = "domains"
    SOCIAL_MEDIA = "social_media"
    MOBILE_APPS = "mobile_apps"
    ECOMMERCE = "ecommerce"
    CRYPTO = "crypto"
    EMAIL = "email"
    PAID_ADS = "paid_ads"
    TELCO = "telco"
    DARKWEB = "darkweb"


class TagActionType(StrEnum):
    """Action to perform on a tag during alert update."""

    ADD = "add"
    REMOVE = "remove"


class FileActionType(StrEnum):
    """Action to perform on files during alert update."""

    UPLOAD = "upload"
    DELETE = "delete"


class SortType(StrEnum):
    """Field to sort alerts by."""

    DATE_SOURCED = "date_sourced"
    DATE_LAST_ACTIONED = "date_last_actioned"


class SortOrder(StrEnum):
    """Sort direction."""

    ASC = "asc"
    DESC = "desc"


# --------------------------------------------------------------------- #
# Supporting models
# --------------------------------------------------------------------- #


class Tag(BaseModel):
    """A tag associated with an alert."""

    model_config = ConfigDict(extra="allow")

    name: str


class FileInput(BaseModel):
    """A file to upload with an alert.

    Attributes:
        file_name: Name of the file (e.g. ``"evidence.png"``).
        file_to_upload: Base64-encoded file content.
    """

    model_config = ConfigDict(extra="allow")

    file_name: str
    file_to_upload: str | None = None


class FileResult(BaseModel):
    """Result of an individual file operation."""

    model_config = ConfigDict(extra="allow")

    file_name: str | None = None
    success: bool | None = None
    error: str | None = None


class AuditLogMetadata(BaseModel):
    """Metadata attached to an audit log entry."""

    model_config = ConfigDict(extra="allow")

    enforcement_request: dict[str, str] | None = None
    match: dict[str, dict[str, str]] | None = None


class AuditLog(BaseModel):
    """A log entry recording a change to an alert."""

    model_config = ConfigDict(extra="allow")

    changed_by: str | None = None
    value: str | None = None
    timestamp: datetime | None = None
    type: str | None = None
    metadata: AuditLogMetadata | None = None


class PaginationMetadata(BaseModel):
    """Pagination metadata returned by list endpoints."""

    model_config = ConfigDict(extra="allow")

    count: int = 0
    page: int = 0
    pages: int = 0
    page_size: int = 0


# --------------------------------------------------------------------- #
# Response models
# --------------------------------------------------------------------- #


class AlertResponse(BaseModel):
    """Full alert returned by GET /alert and within GET /alerts listings."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    entity: str | None = None
    brand: str | None = None
    doppel_link: str | None = None
    queue_state: str | None = None
    entity_state: str | None = None
    severity: str | None = None
    source: str | None = None
    product: str | None = None
    platform: str | None = None
    notes: str | None = None
    uploaded_by: str | None = None
    assignee: str | None = None
    created_at: datetime | None = None
    last_activity_timestamp: datetime | None = None
    screenshot_url: str | None = None
    score: float | None = None
    tags: list[str] = Field(default_factory=list)
    audit_logs: list[AuditLog] = Field(default_factory=list)
    entity_content: dict[str, object] | None = None
    file_results: list[FileResult] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def _normalize_tags(cls, v: list[str | dict[str, str]]) -> list[str]:
        """Handle tags as strings or objects (``{"name": "..."}``).

        The API returns tags as objects with a ``name`` key, but for
        convenience the model normalises them to plain strings.
        """
        return [t["name"] if isinstance(t, dict) else t for t in v]


class AlertCreatedResponse(BaseModel):
    """Lighter response returned by POST /alert."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    entity: str | None = None
    doppel_link: str | None = None
    last_activity_timestamp: datetime | None = None
    message: str | None = None
    file_results: list[FileResult] = Field(default_factory=list)


class _AlertsData(BaseModel):
    """Inner ``data`` wrapper for the alerts list response."""

    model_config = ConfigDict(extra="allow")

    alerts: list[AlertResponse] = Field(default_factory=list)


class AlertsListResponse(BaseModel):
    """Paginated response from GET /alerts."""

    model_config = ConfigDict(extra="allow")

    data: _AlertsData = Field(default_factory=_AlertsData)
    metadata: PaginationMetadata = Field(default_factory=PaginationMetadata)
