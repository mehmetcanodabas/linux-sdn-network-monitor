from ipaddress import ip_address


def validate_ip(ip):
    # Validate an IPv4 address
    try:
        address = ip_address(ip)

        if address.version != 4:
            raise ValueError("Only IPv4 addresses are supported")

        return str(address)

    except ValueError:
        raise ValueError(f"Invalid IPv4 address: {ip}")


def validate_port(port):
    # Validate the switch output port
    try:
        port = int(port)
    except (ValueError, TypeError):
        raise ValueError("Port must be a valid integer")

    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")

    return port


def build_flow_rule(device_id, dst_ip, out_port):
    # Validate configuration parameters
    dst_ip = validate_ip(dst_ip)
    out_port = validate_port(out_port)

    if not device_id.startswith("of:"):
        raise ValueError("Device ID must start with 'of:'")

    # Build an ONOS-style forwarding rule
    flow_rule = {
        "deviceId": device_id,
        "priority": 40000,
        "timeout": 0,
        "isPermanent": True,
        "selector": {
            "criteria": [
                {"type": "ETH_TYPE", "ethType": "0x0800"},
                {"type": "IPV4_DST", "ip": f"{dst_ip}/32"}
            ]
        },
        "treatment": {
            "instructions": [
                {"type": "OUTPUT", "port": str(out_port)}
            ]
        }
    }

    return flow_rule
