# 🛰️ ReconX — Modular Reconnaissance Framework

**Author:** Jacopo De Dominicis  
**Version:** 0.1.0  
**License:** MIT  
**Release Date:** October 2025

---

## Overview

**ReconX** is a **modular passive reconnaissance framework** designed for cybersecurity professionals, threat analysts, and OSINT researchers.  
It automates the collection, normalization, and prioritization of reconnaissance data (DNS, WHOIS, certificates) through a clean **plugin-based architecture**.

ReconX is the first component of the **Sentinel Framework**, an ecosystem of intelligent and interoperable cybersecurity tools.

---

## Vision & Mission

**Vision:** Build a lightweight, reliable, and extensible ecosystem for automated reconnaissance and intelligence.  
**Mission:** Provide an open-source framework to:

- Collect technical information (DNS, certificates, IPs, WHOIS) consistently.  
- Normalize and enrich data through a standardized JSON schema.  
- Evaluate evidence using a configurable scoring and prioritization system.  
- Extend functionality easily through simple, well-documented plugins.

---

## Key Features (v0.1.0 – MVP)

- **CLI Core** with commands: `scan`, `export`, `list-plugins`
- **Dynamic plugin loader** (runtime discovery in `/plugins/`)
- **Three core modules**: `dns_basic`, `whois_parser`, `crtsh_lookup`
- **SQLite local storage** + export to `JSON` or `CSV`
- **Canonical JSON output schema**
- **Caching layer** with TTL
- **Automatic validation** of plugin output via `jsonschema`
- **Test suite** with Pytest (100% passing)
- **Logging & error handling** unified across all modules

---

##  Installation

### Requirements
- Python 3.11+
- `git`, `poetry` or `pip`

### Setup (Poetry)
```bash
git clone https://github.com/<your-username>/ReconX.git
cd ReconX
poetry install
```

### Manual setup (pip)
```bash
pip install -r requirements.txt
```

---

## Usage

### Run a scan
```bash
python -m reconx.cli scan example.com
```

### Export stored results
```bash
python -m reconx.cli export --format json --out results.json
```

### List available plugins
```bash
python -m reconx.cli list-plugins
```

---

## Example Output

```json
[
  {
    "target": "example.com",
    "module": "dns_basic",
    "type": "dns_a",
    "confidence": 0.9,
    "priority": 5,
    "evidence": [{"label": "A", "value": ["93.184.216.34"]}],
    "meta": {"source": "dns_basic", "ttl_seconds": 86400}
  }
]
```

---

## Project Structure

```
ReconX/
├── reconx/
│   ├── core/              → engine, storage, schema, cache, logging
│   └── cli.py             → CLI entrypoint
├── plugins/               → modular data collectors (DNS, WHOIS, CRTSH)
├── tests/                 → pytest suite (8 tests total)
├── docs/                  → technical documentation (quickstart, plugin guide, schema)
└── .github/workflows/     → CI pipeline with lint + tests
```

---

## Core Architecture

### Engine
- Loads plugins dynamically from `/plugins/`
- Executes them asynchronously with `asyncio`
- Validates all results via `reconx/core/schema.py`
- Saves data to SQLite via `reconx/core/storage.py`

### Plugin System
- Each plugin defines `name`, `version`, `inputs_supported`, and `async run()`.
- Must return data conforming to the canonical schema.

### Caching
- Implemented in `core/cache.py`
- TTL-based mechanism to avoid redundant requests.

### Logging
- Unified log format across modules.
- Levels: INFO, WARNING, ERROR.

---

## Example Plugins

| Plugin | Purpose | Output Type |
|--------|----------|--------------|
| `dns_basic` | DNS resolution (A, AAAA, MX, NS, TXT) | `dns_a`, `dns_ns`, etc. |
| `whois_parser` | WHOIS record extraction | `whois_record` |
| `crtsh_lookup` | Certificate Transparency search | `certificate` |

---

## Testing

All components are covered by Pytest unit tests:

```bash
pytest -v
```

Example output:

```
8 passed in 1.35s
```

---

## Export Formats

| Format | Command Example | Description |
|--------|-----------------|--------------|
| JSON | `--format json --out results.json` | Full raw data export |
| CSV | `--format csv --out results.csv` | Tabular export for reports |

---

## Documentation

| File | Description |
|------|--------------|
| `docs/quickstart.md` | Setup and usage guide |
| `docs/plugin_dev_guide.md` | How to build compatible plugins |
| `docs/schema_reference.md` | Canonical JSON schema reference |

---

## Legal & Ethical Notice

ReconX is designed **only** for authorized passive reconnaissance.  
Do not use it for intrusive or unauthorized scanning.  
Users are responsible for ensuring compliance with all applicable laws and regulations.

---

## Roadmap

### v1.0 — Robustness & API Integration
- API connectors: Shodan, Censys
- Configurable scoring engine
- Export to HTML reports
- Rate-limit + retry handling

### v2.0 — Scalability & Web UI
- Web dashboard (React / Vue)
- PostgreSQL / Elasticsearch backend
- Worker pool for concurrent jobs
- Plugin registry and REST API

---

## Sentinel Ecosystem

ReconX is part of the **Sentinel Framework**, a family of interoperable cybersecurity tools:

| Module | Purpose |
|---------|----------|
| **ReconX** | Passive reconnaissance and intelligence |
| **HoneypotX** | Threat deception and trap system |
| **CloudX** | Cloud asset monitoring |
| **DevSecX** | CI/CD pipeline security |
| **SIEMLiteX** | Lightweight monitoring and event correlation |

---

## Contributing

Pull requests are welcome!  
To contribute:
1. Fork the repository
2. Create a feature branch
3. Run tests (`pytest -v`)
4. Submit a PR

---

## License

Licensed under the **MIT License**.  
© 2025 Jacopo — All rights reserved.
