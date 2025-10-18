from pathlib import Path
import textwrap

BASE_DIR = Path.cwd()

print(f"📁 Generazione struttura in: {BASE_DIR}")

# === CARTELLE DA CREARE ===
DIRS = [
    "reconx/core",
    "reconx/data",
    "reconx/api",
    "reconx/ui",
    "plugins/dns_basic/tests",
    "plugins/crtsh_lookup/tests",
    "plugins/whois_parser/tests",
    "plugins/__template__",
    "tests",
    "docs",
    ".github/workflows",
    "scripts",
]

# === FILES BASE ===
FILES = {
    "README.md": "# ReconX\n\nFramework di reconnaissance modulare.",
    "LICENSE": "MIT License",
    "CONTRIBUTING.md": "## Linee guida per contribuire\n\n1. Fork\n2. Branch\n3. PR",
    ".gitignore": "\n".join(["__pycache__/", "*.pyc", ".venv/", "venv/", "*.db", ".env"]),
    ".env.example": "# Inserisci qui le API keys (es. SHODAN_API_KEY=...)",
    "pyproject.toml": textwrap.dedent("""
        [tool.poetry]
        name = "reconx"
        version = "0.1.0"
        description = "Modular reconnaissance framework"
        authors = ["Tuo Nome <tu@domain.com>"]
        license = "MIT"

        [tool.poetry.dependencies]
        python = "^3.11"
        click = "^8.1.3"
        aiohttp = "^3.9.5"
        dnspython = "^2.6.1"
        requests = "^2.32.3"
        python-whois = "^0.9.4"
        sqlalchemy = "^2.0.36"
        jsonschema = "^4.23.0"

        [tool.poetry.group.dev.dependencies]
        pytest = "^8.3.0"
        black = "^24.8.0"
        isort = "^5.13.2"

        [tool.poetry.scripts]
        reconx = "reconx.cli:main"
    """).strip(),
}

# === FILES CODICE ===
CODE_FILES = {
    "reconx/__init__.py": "",
    "reconx/cli.py": textwrap.dedent("""
        import click

        @click.group()
        def main():
            \"\"\"CLI principale di ReconX\"\"\"
            pass

        @main.command()
        @click.argument("target")
        def scan(target):
            click.echo(f"Scanning {target}...")

        if __name__ == "__main__":
            main()
    """).strip(),
    "reconx/core/__init__.py": "",
    "reconx/core/plugin_base.py": textwrap.dedent("""
        from typing import List, Dict, Any, Protocol

        class Plugin(Protocol):
            name: str
            version: str
            inputs_supported: set

            async def run(self, target: str, ctx) -> List[Dict[str, Any]]:
                ...
    """).strip(),
    "reconx/core/engine.py": "# Motore principale ReconX\n",
    "reconx/core/schema.py": "# Validatore schema JSON per risultati\n",
    "reconx/core/storage.py": "# Gestione SQLite\n",
    "reconx/core/cache.py": "# Cache TTL\n",
    "reconx/core/logging.py": "# Logging centralizzato\n",
    "plugins/__init__.py": "",
    "plugins/dns_basic/plugin.py": "# Plugin DNS placeholder\n",
    "plugins/crtsh_lookup/plugin.py": "# Plugin crt.sh placeholder\n",
    "plugins/whois_parser/plugin.py": "# Plugin WHOIS placeholder\n",
    "tests/__init__.py": "",
    "tests/test_cli.py": "def test_scan_runs():\n    assert True\n",
    "docs/index.md": "# Documentazione ReconX",
    ".github/workflows/tests.yml": textwrap.dedent("""
        name: Tests
        on: [push, pull_request]
        jobs:
          build:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - name: Set up Python
                uses: actions/setup-python@v5
                with:
                  python-version: '3.11'
              - name: Install dependencies
                run: pip install poetry && poetry install
              - name: Run tests
                run: poetry run pytest -v
    """).strip(),
    "scripts/run_demo.sh": "#!/bin/bash\npython -m reconx.cli example.com\n"
}

# === CREAZIONE CARTELLE ===
for d in DIRS:
    path = BASE_DIR / d
    path.mkdir(parents=True, exist_ok=True)
    print(f"📂 Cartella creata: {path}")

# === CREAZIONE FILES ===
for name, content in FILES.items():
    path = BASE_DIR / name
    if not path.exists():
        path.write_text(content.strip() + "\n")
        print(f"📝 File creato: {path}")

for name, content in CODE_FILES.items():
    path = BASE_DIR / name
    if not path.exists():
        path.write_text(content.strip() + "\n")
        print(f"🧩 File creato: {path}")

print("\n✅ Struttura ReconX generata con successo!")
print("Ora puoi aprire 'reconx/cli.py' e lanciare:")
print("    python -m reconx.cli example.com")
