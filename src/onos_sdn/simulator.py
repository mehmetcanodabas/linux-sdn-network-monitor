from flask import Flask, jsonify, request

from onos_sdn.flow_config import validate_ip, validate_port

app = Flask(__name__)

# Store configured flow rules in memory
configured_flows = {}


@app.route("/onos/v1/topology", methods=["GET"])
def get_topology():
    # Return simulated network topology
    return jsonify({
        "devices": 3,
        "links": 2,
        "hosts": 2
    })


@app.route("/onos/v1/devices", methods=["GET"])
def get_devices():
    # Return simulated OpenFlow switches
    return jsonify({
        "devices": [
            {
                "id": "of:0000000000000001",
                "available": True
            },
            {
                "id": "of:0000000000000002",
                "available": True
            },
            {
                "id": "of:0000000000000003",
                "available": True
            }
        ]
    })


@app.route("/onos/v1/hosts", methods=["GET"])
def get_hosts():
    # Return simulated network hosts
    return jsonify({
        "hosts": [
            {
                "id": "host-1",
                "ipAddresses": ["10.0.0.1"]
            },
            {
                "id": "host-2",
                "ipAddresses": ["10.0.0.2"]
            }
        ]
    })


@app.route("/onos/v1/links", methods=["GET"])
def get_links():
    # Return simulated connections between switches
    return jsonify({
        "links": [
            {
                "src": {
                    "device": "of:0000000000000001",
                    "port": "1"
                },
                "dst": {
                    "device": "of:0000000000000002",
                    "port": "2"
                },
                "state": "ACTIVE"
            },
            {
                "src": {
                    "device": "of:0000000000000002",
                    "port": "3"
                },
                "dst": {
                    "device": "of:0000000000000003",
                    "port": "1"
                },
                "state": "ACTIVE"
            }
        ]
    })


@app.route("/onos/v1/flows/<device_id>", methods=["GET"])
def get_flows(device_id):
    # Return simulated flow statistics
    default_flows = [
        {
            "id": "1001",
            "deviceId": device_id,
            "state": "ADDED",
            "packets": 150,
            "bytes": 12000
        },
        {
            "id": "1002",
            "deviceId": device_id,
            "state": "ADDED",
            "packets": 75,
            "bytes": 6000
        }
    ]

    # Include flow rules created through POST requests
    new_flows = configured_flows.get(device_id, [])

    return jsonify({
        "flows": default_flows + new_flows
    })


@app.route("/onos/v1/flows/<device_id>", methods=["POST"])
def add_flow_rule(device_id):
    # Read the configuration request
    flow_rule = request.get_json(silent=True)

    if not isinstance(flow_rule, dict):
        return jsonify({
            "error": "Invalid JSON payload"
        }), 400

    # Verify that the rule targets the requested device
    if flow_rule.get("deviceId") != device_id:
        return jsonify({
            "error": "Device ID mismatch"
        }), 400

    # Validate the forwarding rule structure
    try:
        criteria = flow_rule["selector"]["criteria"]
        instructions = flow_rule["treatment"]["instructions"]

        dst_ip = next(
            item["ip"]
            for item in criteria
            if item["type"] == "IPV4_DST"
        )

        out_port = next(
            item["port"]
            for item in instructions
            if item["type"] == "OUTPUT"
        )

        if not dst_ip.endswith("/32"):
            raise ValueError("Invalid destination prefix")

        validate_ip(dst_ip[:-3])
        validate_port(out_port)

    except (KeyError, TypeError, ValueError, StopIteration, AttributeError):
        return jsonify({
            "error": "Invalid forwarding rule"
        }), 400

    # Store the validated rule in memory
    configured_flows.setdefault(device_id, []).append(flow_rule)

    return jsonify({
        "message": "Flow rule stored successfully",
        "deviceId": device_id,
        "rule": flow_rule
    }), 201


if __name__ == "__main__":
    # Start the local REST API simulator
    app.run(
        host="127.0.0.1",
        port=8181,
        debug=False
    )
