import subprocess
import sys

def test_cli_scan_runs():
    """Verifica che il comando 'scan' esegua senza errori."""
    result = subprocess.run(
        [sys.executable, "-m", "reconx.cli", "scan", "example.com"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "example.com" in result.stdout or "Scansione completata" in result.stdout


def test_cli_list_plugins():
    """Verifica che 'list-plugins' elenchi i plugin disponibili."""
    result = subprocess.run(
        [sys.executable, "-m", "reconx.cli", "list-plugins"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "dns_basic" in result.stdout or "crtsh_lookup" in result.stdout
