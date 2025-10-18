import asyncio
from plugins.crtsh_lookup import plugin

def test_crtsh_lookup_returns_certificates():
    """Verifica che il plugin crt.sh produca certificati validi."""
    results = asyncio.run(plugin.run("example.com"))
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("certificate" in r["type"] for r in results)
