"""Protected asset models and enums for the Doppel API."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


__all__ = [
    "Platform",
    "ProtectedAssetCreateResponse",
    "ProtectedAssetResponse",
    "ProtectedAssetsListResponse",
]


class Platform(StrEnum):
    """Platform types for protected assets."""

    AMAZON = "amazon"
    ANDROID = "android"
    APP_STORE = "app_store"
    BLUESKY = "bluesky"
    DISCORD = "discord"
    DOMAIN = "domain"
    EMAIL = "email"
    ETSY = "etsy"
    FACEBOOK = "facebook"
    GITHUB = "github"
    GLASSDOOR = "glassdoor"
    GOOGLE_ADS = "google_ads"
    GOOGLE_MAPS = "google_maps"
    GOOGLE_PLAY = "google_play"
    INDEED = "indeed"
    INSTAGRAM = "instagram"
    KAKAO_TALK = "kakao_talk"
    LINE = "line"
    LINKEDIN = "linkedin"
    META_ADS = "meta_ads"
    NAVER = "naver"
    OKX = "okx"
    OTHER = "other"
    PINTEREST = "pinterest"
    REDDIT = "reddit"
    SHOPEE = "shopee"
    SHOPIFY = "shopify"
    SIGNAL = "signal"
    SNAPCHAT = "snapchat"
    TELEGRAM = "telegram"
    THREADS = "threads"
    TIKTOK = "tiktok"
    TOKOPEDIA = "tokopedia"
    TRUSTPILOT = "trustpilot"
    TWITTER = "twitter"
    VIBER = "viber"
    WECHAT = "wechat"
    WHATSAPP = "whatsapp"
    YOUTUBE = "youtube"
    ZALO = "zalo"


class ProtectedAssetResponse(BaseModel):
    """A protected asset returned by the Doppel API."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    brand_ids: list[str] = Field(default_factory=list)
    platform: str | None = None
    asset_value: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProtectedAssetsListResponse(BaseModel):
    """Response from GET /protected-assets."""

    model_config = ConfigDict(extra="allow")

    data: list[ProtectedAssetResponse] = Field(default_factory=list)
    count: int = 0


class ProtectedAssetCreateResponse(BaseModel):
    """Response from POST /protected-asset."""

    model_config = ConfigDict(extra="allow")

    data: ProtectedAssetResponse | None = None
    message: str | None = None
