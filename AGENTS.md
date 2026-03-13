# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

`doppel-api` is a modern, type-safe Python client for the Doppel API, built on [HTTPX](https://www.python-httpx.org/) for first-class sync and async support.

**API Reference:** <https://doppel.readme.io/reference/>

**Technology Stack:**
- Python 3.11+ with UV for dependency management
- [Taskfile](https://taskfile.dev/) (go-task) for task running (`Taskfile.yml`)
- Ruff for linting and formatting
- pytest for testing with pytest-cov for coverage
- HTTPX for HTTP transport (sync + async)
- Pydantic for data models and validation

## Common Development Commands

### Setup and Installation
```bash
task setup # uv sync --all-groups
uv run python -c "import doppel; print('OK')"
```

### Testing
```bash
task test # uv run pytest tests/unit
task test:cov # uv run pytest --cov=doppel tests/unit
uv run pytest tests/unit/test_specific.py # single file
task test:integration # requires live Doppel API access
```

### Code Quality
```bash
task format # uv run ruff format .
task lint # uv run ruff check .
task lint:fix # uv run ruff check . --fix
task typecheck # uv run ty check doppel
task check # lint + format check + typecheck + tests
task lock:check # verify lockfile is up-to-date
```

### Building
```bash
task build # uv build
```

## Architecture and Code Organization

```
doppel/                     # Python package (the library)
├── __init__.py             # Public API: Doppel, AsyncDoppel, exceptions, __version__
├── client.py               # Doppel (sync) + AsyncDoppel with @cached_property resources
├── _base_client.py         # _BaseClient, SyncAPIClient, AsyncAPIClient
│                           #   - Dual API key auth via _DoppelAuth(httpx.Auth)
│                           #   - _check_response, _build_params
├── _resource.py            # SyncAPIResource / AsyncAPIResource base classes
├── _types.py               # Type aliases (JSON, Params, T)
├── exceptions.py           # DoppelError hierarchy
├── models/
│   ├── __init__.py         # Re-exports all models
│   ├── alerts.py           # AlertResponse, AlertCreatedResponse, AuditLog, enums
│   ├── reports.py          # ReportResponse (deprecated endpoints)
│   ├── brands.py           # BrandResponse, BrandsListResponse
│   ├── protected_assets.py # ProtectedAssetResponse, Platform enum (~40 values)
│   └── webhooks.py         # Webhook payloads: AlertUpdated, ReportSurfaced, SMS, IOC
├── alerts.py               # Alerts + AsyncAlerts resource (5 methods each)
├── reports.py              # Reports + AsyncReports resource (4 methods, deprecated)
├── brands.py               # Brands + AsyncBrands resource (1 method)
├── protected_assets.py     # ProtectedAssets + AsyncProtectedAssets resource (2 methods)
├── webhooks.py             # parse_webhook() utility function
└── py.typed                # PEP 561 marker

tests/                      # Test suites
├── unit/                   # Unit tests (pytest default)
│   ├── conftest.py         # Shared fixtures (sync_client, async_client, mock_api)
│   ├── test_alerts.py      # Alert resource tests (mocked with respx)
│   ├── test_base_client.py # Auth, response checking, param building
│   ├── test_brands.py      # Brand resource tests
│   ├── test_client.py      # Client wiring, cached_property behaviour
│   ├── test_exceptions.py  # Exception hierarchy, exception_for_status
│   ├── test_init.py        # Package exports, version
│   ├── test_models.py      # Model validation, enums, extra-field tolerance
│   ├── test_protected_assets.py # Protected asset resource tests
│   ├── test_reports.py     # Report resource tests (deprecation warnings)
│   └── test_webhooks.py    # Webhook payload parsing
└── integration/            # Integration tests (live API)
```

### Authentication

The Doppel API requires two API keys:
- `x-api-key` (gateway key) — set via `api_key` parameter
- `x-user-api-key` (user key) — set via `user_api_key` parameter
- `x-organization-code` (optional) — set via `organization_code` parameter

### Resource Pattern

Resources follow the same composition pattern as jirapi:
- Each resource group is a flat module (e.g. `doppel/alerts.py`)
- Resources inherit from `SyncAPIResource` / `AsyncAPIResource`
- Client wires resources via `@cached_property`
- All HTTP calls delegate to `_client._request()`

### Models

- All models use `ConfigDict(extra="allow")` for forward compatibility
- Tag fields normalise `[{"name": "..."}]` to `["..."]` via `@field_validator`
- Response wrappers match the exact API shape (e.g. `AlertsListResponse` with nested `data.alerts` + `metadata`)

## Code Style and Standards

### Python Style

**Imports:**
- Use absolute imports over relative imports
- Order imports alphabetically (isort via ruff)

**Type Hints:**
- Use type hints for all function parameters and returns
- Prefer built-in generics (`list[str]`, `dict[str, int]`) over `typing` equivalents
- Use union syntax (`str | None`) instead of `Optional[str]`
- Do not import deprecated typing names (`Dict`, `List`, `Set`, `Tuple`, `Optional`)

**Naming Conventions:**
- snake_case for functions and variables
- PascalCase for classes
- UPPER_CASE for constants
- Maximum line length: 100 characters

**Docstrings:**
- Use Google-style docstrings (configured in ruff)
- Document all public APIs
- Focus on why, not what
- Every module must have a module-level docstring

**Other Rules:**
- `__init__.py` files must define `__all__` to declare the public API
- Always specify exception types — never use bare `except:` or `except Exception:` without good reason
- Prefer `async def` for all I/O-bound operations
- Constants over magic numbers
- Single responsibility per function

### Testing Requirements

- Write tests before fixing bugs
- Test edge cases and error scenarios
- Use pytest for all testing
- Use proper mocking with pytest-mock and respx (for HTTPX)
- Use fixtures for test setup
- Mark integration tests with `@pytest.mark.integration`
- **MUST run `task format && task lint` before completion**

### Security

- Never commit credentials or sensitive information
- Never hardcode API tokens — accept them as parameters
- Sanitize all user inputs

### Version Control

- Feature branches: `feature/<description>`
- Bugfix branches: `fix/<description>`
- Small, focused commits with clear messages
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- **MUST run `task format && task lint` before considering work complete**

### Changelog

- **MUST update `CHANGELOG.md`** when making user-facing changes
- Add a new version section (e.g. `## [0.2.0] - YYYY-MM-DD`) or append to the latest unreleased section at the top
- Use the appropriate subsection: `Added`, `Changed`, `Fixed`, `Removed`
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Do not modify entries for already-released versions

### Development Workflow

1. Create feature branch
2. Make changes following coding standards
3. Run quality checks: `task format && task lint`
4. Run tests: `task test:cov`
5. Verify lockfile: `task lock:check`
6. Update `CHANGELOG.md`
7. Submit PR using the PR template
