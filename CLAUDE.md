# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

DMP (DST Management Platform) Python SDK — a client library for the DMP game server management API (Don't Starve Together). Wraps REST endpoints behind chainable module objects (`client.room.list()`, `client.dashboard.startup()`).

**Dependencies:** Python >= 3.9, requests >= 2.28. No other runtime dependencies.

## Build & publish

```
python -m build          # build dist/*
python -m twine upload dist/*   # publish to PyPI
```

Version is set in `pyproject.toml` → `project.version`. Update it before building.

There are no tests in this project.

## Architecture

```
dmp_sdk_python/
├── __init__.py          # exports DMPClient, DMPError, PaginatedResult
├── client.py            # DMPClient — session, HTTP, module wiring
├── error.py             # DMPError exception (code + message)
├── paginated.py         # PaginatedResult (rows, page, pageSize, total)
└── modules/
    ├── user.py          # UserModule      (/v3/user/*)
    ├── dashboard.py     # DashboardModule (/v3/dashboard/*)
    ├── room.py          # RoomModule      (/v3/room/*)
    ├── mod.py           # ModModule       (/v3/mod/*)
    ├── player.py        # PlayerModule    (/v3/player/*)
    ├── tools.py         # ToolsModule     (/v3/tools/*)
    ├── logs.py          # LogsModule      (/v3/logs/*)
    └── platform.py      # PlatformModule  (/v3/platform/*)
```

### DMPClient (`client.py`)

Wraps a `requests.Session`. Constructor takes `base_url`, optional `token`, `timeout` (default 30), and `lang` (default "zh").

- Auth: JWT token sent as `X-DMP-TOKEN` header. Set via constructor or `set_token()`.
- Language: `X-I18n-Lang` header, toggled via `set_lang("zh"|"en")`.
- All API paths are under `/v3/` prefix.

Key methods:
- `_request(method, path, params, json_data, data, files, raw)` — sends HTTP request, parses JSON envelope `{"code": 200, "data": ...}`. Raises `DMPError` on non-200 code. With `raw=True`, returns the raw `requests.Response` (for binary downloads).
- `_paginated(data, method, path, params)` — single-page request returning a `PaginatedResult`.

Shortcut properties: `client.u` (user), `client.db` (dashboard), `client.rm` (room), `client.md` (mod), `client.pl` (player), `client.tl` (tools), `client.lg` (logs), `client.pt` (platform).

### Module pattern

Every module class follows the same pattern:
- Constructor receives the `DMPClient` instance, stores as `self._c`.
- Each method maps to one API endpoint, calling `self._c._request(HTTP_METHOD, "/path", ...)`.
- List endpoints use `self._c._paginated()` to get paginated results.
- File download methods accept an optional `save_path` to write to disk, otherwise return raw bytes.

### PaginatedResult (`paginated.py`)

Wraps `{"rows": [...], "page": int, "pageSize": int, "total": int}`. Supports `len()`, `__getitem__`, and `__iter__` over `rows`.

### Error handling (`error.py`)

`DMPError(code, message)` — raised when API returns `code != 200`. Both `code` and `message` are accessible as attributes.

### Password handling

Passwords are sent in plain text; the backend handles bcrypt hashing server-side.
