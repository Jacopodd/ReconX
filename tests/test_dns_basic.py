import asyncio
from plugins.dns_basic import plugin

def test_dns_basic_returns_records():
    """Verifica che il plugin DNS produca record validi."""
    results = asyncio.run(plugin.run("example.com"))
    assert isinstance(results, list)
    assert len(results) > 0
    assert any(r["type"].startswith("dns_") for r in results)
    assert all("target" in r for r in results)
