# ReconX — JSON Schema Reference

This document describes the canonical JSON schema used by ReconX for plugin findings.
All plugins must emit findings that conform to this schema.

---

## Example finding

```json
{
  "target": "example.com",
  "scanned_at": "2025-10-18T12:34:56Z",
  "module": "dns_basic",
  "type": "dns_record",
  "confidence": 0.9,
  "priority": 5,
  "evidence": [
    {"label": "A", "value": ["93.184.216.34"]}
  ],
  "meta": {
    "source": "dns_basic",
    "ttl_seconds": 86400
  }
}
```

---

## Field reference

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | Domain or IP the finding is about |
| `scanned_at` | string (ISO8601) | UTC timestamp when the finding was generated |
| `module` | string | Plugin name that produced the finding |
| `type` | string | Short descriptor of the finding (e.g. `dns_a`, `certificate`, `whois_record`) |
| `confidence` | number | Confidence score between 0.0 and 1.0 |
| `priority` | integer | Priority score (suggested 0–10) |
| `evidence` | array | Array of evidence objects: `[{ "label": "...", "value": ... }]` |
| `meta` | object | Module-specific metadata (e.g. `source`, `ttl_seconds`) |

---

## Evidence object

Each item in `evidence` should be an object with:
- `label` (string): a short name for the evidence (e.g. `"A"`, `"CN"`, `"registrant"`)
- `value` (string | number | array | object): the evidence content

Examples:
```json
{"label": "A", "value": ["93.184.216.34"]}
{"label": "CN", "value": "*.example.com"}
{"label": "registrant", "value": "Example Corp"}
```

---

## Validation

ReconX includes `reconx/core/schema.py` that validates each finding with `jsonschema`.
If a finding does not conform, the engine logs a warning and skips the invalid finding.

Typical validation errors:
- Missing required fields (`module`, `confidence`, etc.)
- Wrong data type (e.g. `evidence` not an array)
- Non-ISO timestamps in `scanned_at`

---

## Versioning and backwards compatibility

- The canonical schema can evolve. When changing the schema, bump the framework version and document the change in `docs/CHANGELOG.md`.
- Plugins should declare a `version` string; when upgrading schema expectations, document migration steps for plugin authors.
