# Validatore schema JSON per risultati
from jsonschema import validate, ValidationError

FINDING_SCHEMA = {
    "type": "object",
    "required": ["target", "module", "type", "confidence", "priority", "evidence", "meta"],
    "properties": {
        "target": {"type": "string"},
        "module": {"type": "string"},
        "type": {"type": "string"},
        "confidence": {"type": "number"},
        "priority": {"type": "number"},
        "evidence": {"type": "array"},
        "meta": {"type": "object"},
    },
}

def validate_finding(finding):
    """Valida un singolo risultato secondo lo schema canonico."""
    try:
        validate(instance=finding, schema=FINDING_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Finding non conforme allo schema: {e.message}")
