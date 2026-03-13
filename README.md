# doppel-api

[![CI](https://github.com/brett-fitz/doppel-api/actions/workflows/ci.yml/badge.svg)](https://github.com/brett-fitz/doppel-api/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/doppel-api)](https://pypi.org/project/doppel-api/)
[![Python](https://img.shields.io/pypi/pyversions/doppel-api)](https://pypi.org/project/doppel-api/)
[![License](https://img.shields.io/pypi/l/doppel-api)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/doppel-api)](https://pypistats.org/packages/doppel-api)
[![Checked with ty](https://img.shields.io/badge/type--checked-ty-blue)](https://github.com/astral-sh/ty)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Modern, type-safe Python client for the **Doppel API** — built on [HTTPX](https://www.python-httpx.org/) for first-class sync and async support.

> **API Reference:** <https://doppel.readme.io/reference/>

## Features

- **Sync and async** — identical API surface via `Doppel` (sync) and `AsyncDoppel` (async)
- **Type-safe** — Pydantic v2 models for every request and response payload
- **Semantic exceptions** — typed error hierarchy for clean error handling
- **Webhook parsing** — lightweight `parse_webhook()` utility for inbound events
- **Modern Python** — 3.11+, built-in generics, union types, no legacy `typing` imports
- **Minimal dependencies** — just `httpx` and `pydantic`

## Installation

```bash
pip install doppel-api
# or
uv add doppel-api
```

## Quick Start

```python
from doppel import Doppel

client = Doppel(api_key="your-gw-key", user_api_key="your-user-key")

# Create an alert
alert = client.alerts.create(entity="https://suspicious-site.com")

# Get an alert by ID
alert = client.alerts.get(id="TST-1234")

# List alerts with filters
alerts = client.alerts.list(queue_state="monitoring", page_size=50)

# List brands
brands = client.brands.list()

# List and create protected assets
assets = client.protected_assets.list(platform_name="linkedin")
new_asset = client.protected_assets.create(
    brand_ids=["brand-id"],
    asset_value="https://linkedin.com/company/acme",
)

client.close()
```

### Context Manager

```python
from doppel import Doppel

with Doppel(api_key="your-gw-key", user_api_key="your-user-key") as client:
    alert = client.alerts.get(id="TST-1234")
```

### Asynchronous

```python
import asyncio
from doppel import AsyncDoppel

async def main():
    async with AsyncDoppel(api_key="your-gw-key", user_api_key="your-user-key") as client:
        alert = await client.alerts.get(id="TST-1234")
        brands = await client.brands.list()

asyncio.run(main())
```

### Multi-Organization Support

```python
client = Doppel(
    api_key="your-gw-key",
    user_api_key="your-user-key",
    organization_code="my-org",
)
```

### Webhook Parsing

Parse inbound webhook payloads from Doppel — no framework dependency required:

```python
from doppel.webhooks import parse_webhook

event = parse_webhook(request_body)
# Returns AlertUpdatedEvent | ReportSurfacedEvent | UrlSurfacedEvent | SMSResponseEvent | IOCUpdatedEvent
```

### Error Handling

```python
from doppel import Doppel, NotFoundError, RateLimitError

client = Doppel(api_key="gw-key", user_api_key="user-key")

try:
    alert = client.alerts.get(id="NONEXISTENT")
except NotFoundError:
    print("Alert not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```

## API Coverage

| Resource | Methods |
|---|---|
| **Alerts** | `create`, `get`, `update`, `list`, `submit_referrer_logs` |
| **Brands** | `list` |
| **Protected Assets** | `list`, `create` |
| **Reports** *(deprecated)* | `submit`, `get`, `update`, `list` |
| **Webhooks** | `parse_webhook()` utility |

## Development

```bash
# Install dependencies
task setup          # uv sync --all-groups

# Run quality checks
task check          # lint + format check + typecheck + tests

# Run tests with coverage
task test:cov       # uv run pytest --cov=doppel tests/unit
```

## Architecture

```
doppel/
├── __init__.py             # Public API: Doppel, AsyncDoppel, exceptions
├── client.py               # Doppel + AsyncDoppel with @cached_property resources
├── _base_client.py         # Shared HTTP logic, dual API key auth
├── _resource.py            # SyncAPIResource / AsyncAPIResource base classes
├── exceptions.py           # DoppelError hierarchy
├── models/
│   ├── __init__.py         # Re-exports all models
│   ├── alerts.py           # AlertResponse, enums, pagination
│   ├── reports.py          # ReportResponse (deprecated)
│   ├── brands.py           # BrandResponse
│   ├── protected_assets.py # ProtectedAssetResponse, Platform enum
│   └── webhooks.py         # Webhook event payloads
├── alerts.py               # Alerts + AsyncAlerts resource
├── reports.py              # Reports + AsyncReports resource (deprecated)
├── brands.py               # Brands + AsyncBrands resource
├── protected_assets.py     # ProtectedAssets + AsyncProtectedAssets resource
├── webhooks.py             # parse_webhook() utility
└── py.typed                # PEP 561 marker
```

## Contributing

Contributions are welcome! Please [open an issue](https://github.com/brett-fitz/doppel-api/issues) first to discuss proposed changes. See the [Development](#development) section for setup instructions.

## License

[MIT](LICENSE) | [Changelog](CHANGELOG.md) | [PyPI](https://pypi.org/project/doppel-api/)
