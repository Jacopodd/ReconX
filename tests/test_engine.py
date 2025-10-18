import asyncio
from reconx.core.engine import run_scan

def test_engine_returns_results():
    """Verifica che il motore ritorni risultati validi."""
    results = asyncio.run(run_scan("example.com"))
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("module" in r for r in results)
    assert all("target" in r for r in results)
