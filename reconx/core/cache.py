import json
import os
import time
from pathlib import Path
from reconx.core.logging import setup_logger
log = setup_logger("engine")

CACHE_FILE = Path.cwd() / "cache.json"


def _load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def _save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_cache(key: str):
    """Restituisce il valore in cache se esiste ed è valido."""
    data = _load_cache()
    entry = data.get(key)
    if not entry:
        return None

    if time.time() > entry["expires"]:
        # entry scaduta
        del data[key]
        _save_cache(data)
        return None

    log.info(f"[cache] Hit per {key}")
    return entry["value"]


def set_cache(key: str, value, ttl: int = 86400):
    """Salva un valore in cache con un TTL (secondi)."""
    data = _load_cache()
    data[key] = {"value": value, "expires": time.time() + ttl}
    _save_cache(data)
    log.info(f"[cache] Salvato {key} (TTL {ttl}s)")
