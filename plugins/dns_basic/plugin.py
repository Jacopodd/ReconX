import dns.resolver
from datetime import datetime
from reconx.core.logging import setup_logger
log = setup_logger("engine")

# === Metadati del plugin ===
name = "dns_basic"
version = "1.0.0"
inputs_supported = {"domain"}

# === Funzione principale ===
async def run(target, ctx=None):
    """
    Raccoglie i record DNS principali (A, AAAA, MX, NS, TXT)
    per il dominio specificato.
    """
    resolver = dns.resolver.Resolver()
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    findings = []

    log.info(f"[dns_basic] Avvio risoluzione DNS per {target}")

    for record_type in record_types:
        try:
            answers = resolver.resolve(target, record_type, lifetime=3)
            values = [str(rdata) for rdata in answers]
        except Exception as e:
            values = []
            # logging di errore minimo per debug
            log.error(f"[dns_basic] Nessun record {record_type} trovato ({e})")

        # Crea un singolo risultato per tipo di record
        finding = {
            "target": target,
            "scanned_at": datetime.utcnow().isoformat() + "Z",
            "module": name,
            "type": f"dns_{record_type.lower()}",
            "confidence": 0.9 if values else 0.5,
            "priority": 5,
            "evidence": [{"label": record_type, "value": values}],
            "meta": {"source": "dns_basic", "ttl_seconds": 86400},
        }

        findings.append(finding)

    log.info(f"[dns_basic] Completata risoluzione per {target}")
    return findings
