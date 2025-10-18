import whois
from datetime import datetime
from reconx.core.cache import get_cache, set_cache
from reconx.core.logging import setup_logger
log = setup_logger("engine")

name = "whois_parser"
version = "1.0.1"
inputs_supported = {"domain"}


async def run(target, ctx=None):
    cache_key = f"whois:{target}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    log.info(f"[whois_parser] Avvio query WHOIS per {target}")
    try:
        data = whois.whois(target)
    except Exception as e:
        log.error(f"[whois_parser] Errore WHOIS: {e}")
        result = [{
            "target": target,
            "scanned_at": datetime.utcnow().isoformat() + "Z",
            "module": name,
            "type": "whois_record",
            "confidence": 0.0,
            "priority": 1,
            "evidence": [{"label": "error", "value": str(e)}],
            "meta": {"source": "whois_parser", "ttl_seconds": 86400},
        }]
        set_cache(cache_key, result, ttl=3600)
        return result

    registrant = data.get("org") or data.get("name") or "Unknown"
    creation = str(data.get("creation_date")) if data.get("creation_date") else "N/A"
    expiration = str(data.get("expiration_date")) if data.get("expiration_date") else "N/A"

    result = [{
        "target": target,
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "module": name,
        "type": "whois_record",
        "confidence": 0.8,
        "priority": 6,
        "evidence": [
            {"label": "registrant", "value": registrant},
            {"label": "creation_date", "value": creation},
            {"label": "expiration_date", "value": expiration}
        ],
        "meta": {"source": "whois_parser", "ttl_seconds": 86400},
    }]

    # ✅ Salva il risultato in cache per 24h
    set_cache(cache_key, result, ttl=86400)
    log.info(f"[whois_parser] Completata query WHOIS per {target}")
    return result
