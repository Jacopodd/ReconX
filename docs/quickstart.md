# ReconX — Quickstart Guide

**ReconX** is a modular framework for **passive reconnaissance** of domains and IP addresses.
It automatically collects DNS, WHOIS, and Certificate Transparency data using independent and extensible plugins.

---

## Installation

### Requirements
- Python 3.11 or higher
- `git` and `poetry` (or `pip` if preferred)

### Install with Poetry
```bash
git clone https://github.com/<your-username>/ReconX.git
cd ReconX
poetry install
```

### Manual install (pip)
```bash
pip install -r requirements.txt
```

## Basic Usage

### Scan a single target
```bash
python -m reconx.cli scan example.com
```

### Export results
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

## Project Structure
```text
ReconX/
├── reconx/core/         → core modules (engine, schema, logging, cache)
├── plugins/             → dynamic plugin modules
├── tests/               → automated test suite
└── docs/                → technical documentation
```

## Legal & Ethical Notice
ReconX is designed for **authorized and passive reconnaissance activities only**.
Unauthorized use on third-party systems or domains without consent is **strictly prohibited**.
Use responsibly and for research, security testing, or educational purposes only.
