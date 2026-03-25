import pytest
import asyncio
from PhantomStrike_AI import validate_target, scan_port, scan_target, PluginManager

# Test input validation
@pytest.mark.parametrize("target,expected", [
    ("127.0.0.1", True),
    ("localhost", True),
    ("256.256.256.256", False),
    ("", False),
    ("example.com", True),
])
def test_validate_target(target, expected):
    result = validate_target(target)
    assert (result is not None) == expected

# Test async port scan (localhost, port 80 usually closed)
@pytest.mark.asyncio
async def test_scan_port_closed():
    res = await scan_port("127.0.0.1", 1)  # Porta 1 quasi sempre chiusa
    assert isinstance(res, dict)
    assert res["port"] == 1
    assert not res["open"]

# Test scan_target restituisce lista
@pytest.mark.asyncio
async def test_scan_target_returns_list():
    res = await scan_target("127.0.0.1")
    assert isinstance(res, list)
    for r in res:
        assert "port" in r and "open" in r

# Test caricamento plugin
def test_plugin_manager_load():
    pm = PluginManager()
    pm.load_plugins()
    assert isinstance(pm.plugins, list)
