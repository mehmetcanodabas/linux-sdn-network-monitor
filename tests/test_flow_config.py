import pytest

from onos_sdn.flow_config import validate_ip, validate_port, build_flow_rule


def test_valid_ip():
    # Accept a valid IPv4 address
    assert validate_ip("10.0.0.2") == "10.0.0.2"


def test_invalid_ip():
    # Reject an invalid IPv4 address
    with pytest.raises(ValueError):
        validate_ip("999.10.0.2")


def test_ipv6_not_supported():
    # Reject IPv6 addresses
    with pytest.raises(ValueError):
        validate_ip("2001:db8::1")


def test_valid_port():
    # Accept a valid switch output port
    assert validate_port(2) == 2


def test_invalid_port():
    # Reject a negative port number
    with pytest.raises(ValueError):
        validate_port(-5)


def test_non_numeric_port():
    # Reject non-numeric port values
    with pytest.raises(ValueError):
        validate_port("abc")


def test_build_flow_rule():
    # Create a forwarding rule for a specific device
    rule = build_flow_rule(
        device_id="of:0000000000000001",
        dst_ip="10.0.0.2",
        out_port=2
    )

    # Verify the target device and rule properties
    assert rule["deviceId"] == "of:0000000000000001"
    assert rule["priority"] == 40000
    assert rule["isPermanent"] is True

    # Verify the destination IP matching criteria
    criteria = rule["selector"]["criteria"]

    assert {"type": "ETH_TYPE", "ethType": "0x0800"} in criteria
    assert {"type": "IPV4_DST", "ip": "10.0.0.2/32"} in criteria

    # Verify the output port
    instructions = rule["treatment"]["instructions"]

    assert instructions[0]["type"] == "OUTPUT"
    assert instructions[0]["port"] == "2"        