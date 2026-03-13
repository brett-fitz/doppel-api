# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-03-12

### Added

- Initial project scaffolding (pyproject.toml, Taskfile, CI, Renovate, Claude workflows)
- `Doppel` (sync) and `AsyncDoppel` (async) client classes with dual API key auth (`x-api-key` + `x-user-api-key`) and optional `x-organization-code`
- Alerts resource: `create`, `get`, `update`, `list`, `submit_referrer_logs`
- Brands resource: `list`
- Protected assets resource: `list`, `create`
- Reports resource (deprecated): `submit`, `get`, `update`, `list`
- Pydantic v2 models for all API responses: `AlertResponse`, `AlertCreatedResponse`, `BrandResponse`, `ProtectedAssetResponse`, `ReportResponse`
- Enum types: `QueueState`, `EntityState`, `Severity`, `Product`, `Platform`, `SortType`, `SortOrder`, `TagActionType`, `FileActionType`
- Custom exception hierarchy: `DoppelError`, `ValidationError`, `AuthenticationError`, `ForbiddenError`, `NotFoundError`, `ConflictError`, `RateLimitError`, `ServerError`
- Webhook parsing via `parse_webhook()` for `alert_updated`, `report_surfaced`, `url_surfaced`, `sms_response`, and `ioc_updated` events
- Full unit test suite (97 tests) with sync and async coverage
