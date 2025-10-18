from reconx.core.cache import set_cache, get_cache

def test_cache_set_and_get():
    """Verifica che il sistema di cache salvi e recuperi correttamente i dati."""
    set_cache("unit_test", {"ok": True}, ttl=5)
    value = get_cache("unit_test")
    assert value == {"ok": True}
