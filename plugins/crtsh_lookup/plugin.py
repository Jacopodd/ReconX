import aiohttp
from datetime import datetime
from reconx.core.cache import get_cache, set_cache
from reconx.core.logging import setup_logger
log = setup_logger("engine")

name = "crtsh_lookup"
version = "1.1.0"
inputs_supported = {"domain"}


async def run(target, ctx=None):
    cache_key = f"crtsh:{target}"
    cached = get_cache(cache_key)
    if cached:
        return cached  # Restituisci il risultato da cache

    log.info(f"[crtsh_lookup] Avvio ricerca certificati per {target}")
    base_url = f"https://crt.sh/?q={target}&output=json"
    findings = []

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, timeout=10) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status} da crt.sh")
                data = await resp.json(content_type=None)
        except Exception as e:
            log.error(f"[crtsh_lookup] Errore durante la richiesta: {e}")
            return [{
                "target": target,
                "scanned_at": datetime.utcnow().isoformat() + "Z",
                "module": name,
                "type": "certificate",
                "confidence": 0.0,
                "priority": 2,
                "evidence": [{"label": "error", "value": str(e)}],
                "meta": {"source": "crtsh_lookup", "ttl_seconds": 86400},
            }]

    seen = set()
    for entry in data:
        cn = entry.get("common_name")
        if not cn or cn in seen:
            continue
        seen.add(cn)
        findings.append({
            "target": target,
            "scanned_at": datetime.utcnow().isoformat() + "Z",
            "module": name,
            "type": "certificate",
            "confidence": 0.8,
            "priority": 6,
            "evidence": [
                {"label": "common_name", "value": cn},
                {"label": "issuer_name", "value": entry.get("issuer_name")},
                {"label": "not_after", "value": entry.get("not_after")},
            ],
            "meta": {"source": "crt.sh", "ttl_seconds": 86400},
        })

    # ✅ Salva il risultato in cache
    set_cache(cache_key, findings, ttl=86400)
    log.info(f"[crtsh_lookup] Trovati {len(findings)} certificati per {target}")
    return findings
