import os

import requests
from requests.auth import HTTPBasicAuth

from onos_sdn.flow_config import build_flow_rule


class ONOSClient:
    def __init__(self, host=None, port=None):
        # Read controller settings from environment variables
        host = host or os.getenv("ONOS_HOST", "localhost")
        port = port if port is not None else os.getenv("ONOS_PORT", "8181")

        username = os.getenv("ONOS_USERNAME", "onos")
        password = os.getenv("ONOS_PASSWORD", "rocks")

        self.base_url = f"http://{host}:{port}/onos/v1"
        self.auth = HTTPBasicAuth(username, password)

    def get_topology(self):
        # Retrieve network topology information
        url = f"{self.base_url}/topology"

        response = requests.get(
            url,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    def get_devices(self):
        # Retrieve all network devices
        url = f"{self.base_url}/devices"

        response = requests.get(
            url,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.json()["devices"]

    def get_hosts(self):
        # Retrieve all network hosts
        url = f"{self.base_url}/hosts"

        response = requests.get(
            url,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.json()["hosts"]

    def get_links(self):
        # Retrieve connections between switches
        url = f"{self.base_url}/links"

        response = requests.get(
            url,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.json()["links"]

    def get_flows(self, device_id):
        # Retrieve flow rules for a specific device
        url = f"{self.base_url}/flows/{device_id}"

        response = requests.get(
            url,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.json()["flows"]

    def add_flow_rule(self, device_id, dst_ip, out_port):
        # Validate parameters and build a forwarding rule
        flow_rule = build_flow_rule(device_id, dst_ip, out_port)

        # Send the configuration to the API
        url = f"{self.base_url}/flows/{device_id}"

        response = requests.post(
            url,
            json=flow_rule,
            auth=self.auth,
            timeout=10
        )

        response.raise_for_status()
        return response.status_code
