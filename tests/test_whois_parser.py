import asyncio
from plugins.whois_parser import plugin

def test_whois_parser_returns_data():
    """Verifica che il plugin WHOIS produca risultati coerenti."""
    results = asyncio.run(plugin.run("example.com"))
    assert isinstance(results, list)
    assert len(results) > 0
    first = results[0]
    assert "whois_record" in first["type"]
    assert "evidence" in first
