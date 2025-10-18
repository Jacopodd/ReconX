# ReconX — Plugin Development Guide

This guide explains how to create plugins compatible with ReconX. Plugins extend the framework by gathering new types of data (e.g. Shodan, VirusTotal, additional DNS logic).

---

## Plugin location and structure

Place your plugin in `plugins/<plugin_name>/`:

```
plugins/
  my_plugin/
    __init__.py
    plugin.py
```

`plugin.py` must define the plugin metadata and an `async run()` function.

---

## Minimal plugin template

```python
# plugins/my_plugin/plugin.py

name = "my_plugin"
version = "1.0.0"
inputs_supported = {"domain"}  # or {"ip"}, or both

async def run(target, ctx=None):
    '''
    Implement the plugin logic here. Return a list of findings (dictionaries).
    '''
    # Example static result
    return [{
        "target": target,
        "scanned_at": "2025-10-18T12:00:00Z",
        "module": name,
        "type": "custom_data",
        "confidence": 0.9,
        "priority": 5,
        "evidence": [{"label": "example", "value": "value"}],
        "meta": {"source": name, "ttl_seconds": 86400}
    }]
```

---

## Required plugin interface

Every plugin must provide:
- `name` (string)
- `version` (string)
- `inputs_supported` (set of strings, e.g. `{"domain"}`)
- `async def run(target, ctx=None)` which returns `List[Dict]`

Plugins are imported dynamically by `reconx.core.engine` as `plugins.<plugin_name>.plugin`.

---

## Output schema requirements

Each finding returned by `run()` must conform to ReconX canonical schema (see `docs/schema_reference.md`). In particular:
- Returns a **list** of dictionaries (even if single finding)
- Required keys include: `target`, `module`, `type`, `confidence`, `priority`, `evidence`, `meta`
- `evidence` must be a list of objects with `label` and `value`

---

## Recommended practices

- Use `reconx.core.logging.setup_logger()` for logging instead of `print()`.
- Use `reconx.core.cache.get_cache()` and `set_cache()` for expensive network calls.
- Handle exceptions internally and return error-style findings with low confidence rather than raising.
- Respect `meta.ttl_seconds` to indicate how long findings should be cached.
- Prefer asynchronous I/O (aiohttp, asyncio) to avoid blocking the engine.

---

## Testing a plugin

Create a unit test under `tests/`:

```python
import asyncio
from plugins.my_plugin import plugin

def test_my_plugin():
    results = asyncio.run(plugin.run("example.com"))
    assert isinstance(results, list)
    assert results[0]["module"] == "my_plugin"
```

Run `pytest -v` to execute tests.

---

## Example: using cache and logger (recommended)

```python
from reconx.core.logging import setup_logger
from reconx.core.cache import get_cache, set_cache
from datetime import datetime
import aiohttp

log = setup_logger("my_plugin")
name = "my_plugin"
version = "1.0.0"
inputs_supported = {"domain"}

async def run(target, ctx=None):
    cache_key = f"my_plugin:{target}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    # Example network call
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://example.com/.well-known/info") as resp:
            data = await resp.text()

    finding = {
        "target": target,
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "module": name,
        "type": "external_info",
        "confidence": 0.8,
        "priority": 5,
        "evidence": [{"label": "payload", "value": data}],
        "meta": {"source": name, "ttl_seconds": 86400},
    }

    set_cache(cache_key, [finding], ttl=86400)
    return [finding]
```

---

## Troubleshooting

- If the engine reports `ModuleNotFoundError: plugins.<name>.plugin`, ensure file is named `plugin.py` and package directory contains `__init__.py`.
- If findings are rejected by validation, check `reconx/core/schema.py` to ensure your output satisfies required fields.
- Use `python -m reconx.cli list-plugins` to verify plugin discovery.
