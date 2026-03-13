"""Brand models for the Doppel API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


__all__ = [
    "BrandResponse",
    "BrandsListResponse",
]


class BrandResponse(BaseModel):
    """A brand returned by the Doppel API."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    brand_type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BrandsListResponse(BaseModel):
    """Response from GET /brands."""

    model_config = ConfigDict(extra="allow")

    data: list[BrandResponse] = Field(default_factory=list)
    count: int = 0
