import click
import asyncio
from reconx.core.engine import run_scan
from reconx.core.storage import export_results  # <-- nuovo import

@click.group()
def main():
    """CLI principale di ReconX"""
    pass

@main.command()
@click.argument("target")
def scan(target):
    """Esegue una scansione ReconX"""
    result = asyncio.run(run_scan(target))
    click.echo(f"Risultato: {result}")

@main.command()
@click.option("--format", default="json", type=click.Choice(["json", "csv"]),
              help="Formato di esportazione (json o csv).")
@click.option("--out", required=True, type=click.Path(),
              help="Percorso file di output.")
def export(format, out):
    """Esporta i risultati salvati dal database in JSON o CSV."""
    export_results(out, format)
    click.echo(f"[CLI] Esportati i risultati in {out}")

@main.command()
def list_plugins():
    """Elenca i plugin disponibili nel sistema."""
    import importlib
    from pathlib import Path

    plugins_dir = Path.cwd() / "plugins"
    found = 0

    for plugin_path in plugins_dir.iterdir():
        if plugin_path.is_dir() and (plugin_path / "plugin.py").exists():
            module_name = f"plugins.{plugin_path.name}.plugin"
            try:
                plugin = importlib.import_module(module_name)
                click.echo(f"- {plugin.name} (v{plugin.version})")
                found += 1
            except Exception as e:
                click.echo(f"[!] Errore caricando {plugin_path.name}: {e}")

    if not found:
        click.echo("Nessun plugin trovato.")


if __name__ == "__main__":
    main()
