import importlib
import asyncio
import json
from pathlib import Path
from urllib.parse import urlparse

from reconx.core.storage import init_db, save_findings
from reconx.core.logging import setup_logger
from reconx.core.schema import validate_finding

log = setup_logger("engine")


async def run_scan(target: str):
    """
    Carica ed esegue tutti i plugin su un singolo target.
    Aggrega i risultati, li valida, li stampa e li salva in SQLite.
    """
    # Normalizzazione input (gestisce URL completi come https://example.com)
    if "://" in target:
        parsed = urlparse(target)
        target = parsed.hostname or target
        log.info(f"[engine] Input normalizzato a dominio: {target}")

    log.info(f"[engine] Avvio scansione per target: {target}")

    plugins_dir = Path(__file__).resolve().parent.parent / "plugins"
    results = []

    # Inizializza database
    init_db()

    # Scansiona la cartella plugins/
    for plugin_path in (Path.cwd() / "plugins").iterdir():
        if plugin_path.is_dir() and (plugin_path / "plugin.py").exists():
            module_name = f"plugins.{plugin_path.name}.plugin"
            try:
                plugin = importlib.import_module(module_name)
            except Exception as e:
                log.error(f"[engine] Errore caricando {module_name}: {e}")
                continue

            # Esegue il plugin
            log.info(f"[+] Eseguo plugin: {plugin.name}")
            if hasattr(plugin, "run"):
                try:
                    plugin_results = await plugin.run(target, ctx=None)

                    # Validazione schema JSON per ogni risultato
                    for r in plugin_results:
                        try:
                            validate_finding(r)
                        except Exception as ve:
                            log.warning(f"[engine] Risultato non valido da {plugin.name}: {ve}")
                            continue
                        results.append(r)

                except Exception as e:
                    log.error(f"[engine] Errore eseguendo {plugin.name}: {e}")

    # Salva i risultati nel database SQLite
    if results:
        save_findings(results)
        log.info(f"[engine] {len(results)} risultati salvati nel database.")
    else:
        log.info("[engine] Nessun risultato da salvare.")

    # Stampa JSON per la CLI
    print(json.dumps(results, indent=2))
    return results
