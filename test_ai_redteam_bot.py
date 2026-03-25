import pytest
from ai_redteam_bot import validate_target, DEFAULT_TARGET_PORTS, DEFAULT_PORT_SERVICE_MAP

# Test validate_target
@pytest.mark.parametrize("target", [
    "192.168.1.1",
    "10.0.0.5",
    "example.com",
    "sub.domain.org"
])
def test_validate_target_valid(target):
    assert validate_target(target) == target

@pytest.mark.parametrize("target", [
    "",
    "192.168.1.1; rm -rf /",
    "example.com && shutdown",
    "bad|input"
])
def test_validate_target_invalid(target):
    with pytest.raises(ValueError):
        validate_target(target)

# Test default config

def test_default_ports():
    assert 22 in DEFAULT_TARGET_PORTS
    assert 443 in DEFAULT_TARGET_PORTS
    assert isinstance(DEFAULT_TARGET_PORTS, list)

def test_default_port_service_map():
    assert DEFAULT_PORT_SERVICE_MAP[22] == "ssh"
    assert DEFAULT_PORT_SERVICE_MAP[443] == "https"
    assert isinstance(DEFAULT_PORT_SERVICE_MAP, dict)
