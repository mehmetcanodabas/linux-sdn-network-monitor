from unittest.mock import patch, Mock
from onos_sdn.client import ONOSClient


def test_get_topology():
    # Fake topology data returned by the ONOS API
    fake_topology = {
        "devices": 2,
        "links": 1,
        "hosts": 3
    }

    # Create a fake HTTP response object
    mock_response = Mock()
    mock_response.json.return_value = fake_topology
    mock_response.raise_for_status.return_value = None

    # Replace requests.get with our fake response
    with patch("onos_sdn.client.requests.get", return_value=mock_response):
        client = ONOSClient()
        result = client.get_topology()

    # Verify that the client returns the expected JSON data
    assert result == fake_topology

def test_get_devices():
    # Fake device data returned by the ONOS API
    fake_devices = {
        "devices": [
            {"id": "of:0000000000000001", "available": True},
            {"id": "of:0000000000000002", "available": True}
        ]
    }

    # Create a fake HTTP response
    mock_response = Mock()
    mock_response.json.return_value = fake_devices
    mock_response.raise_for_status.return_value = None

    # Simulate the ONOS API response
    with patch("onos_sdn.client.requests.get", return_value=mock_response):
        client = ONOSClient()
        result = client.get_devices()

    # Verify that both devices are returned correctly
    assert len(result) == 2
    assert result[0]["id"] == "of:0000000000000001"
    assert result[1]["id"] == "of:0000000000000002"   

def test_get_hosts():
    # Fake host data returned by the ONOS API
    fake_hosts = {
        "hosts": [
            {"id": "host-1", "ipAddresses": ["10.0.0.1"]},
            {"id": "host-2", "ipAddresses": ["10.0.0.2"]}
        ]
    }

    # Create a fake HTTP response
    mock_response = Mock()
    mock_response.json.return_value = fake_hosts
    mock_response.raise_for_status.return_value = None

    # Simulate the ONOS API response
    with patch("onos_sdn.client.requests.get", return_value=mock_response):
        client = ONOSClient()
        result = client.get_hosts()

    # Verify the returned hosts
    assert len(result) == 2
    assert result[0]["ipAddresses"] == ["10.0.0.1"]
    assert result[1]["ipAddresses"] == ["10.0.0.2"]     

def test_get_links():
    # Fake network links returned by the ONOS API
    fake_links = {
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
            }
        ]
    }

    # Create a fake HTTP response
    mock_response = Mock()
    mock_response.json.return_value = fake_links
    mock_response.raise_for_status.return_value = None

    # Simulate the ONOS API response
    with patch("onos_sdn.client.requests.get", return_value=mock_response):
        client = ONOSClient()
        result = client.get_links()

    # Verify the network connection information
    assert len(result) == 1
    assert result[0]["src"]["device"] == "of:0000000000000001"
    assert result[0]["dst"]["device"] == "of:0000000000000002"
    assert result[0]["state"] == "ACTIVE"    

def test_get_flows():
    # Simulated flow rules returned by the ONOS API
    device_id = "of:0000000000000001"

    fake_flows = {
        "flows": [
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
    }

    # Create a mock HTTP response
    mock_response = Mock()
    mock_response.json.return_value = fake_flows
    mock_response.raise_for_status.return_value = None

    # Replace the real HTTP request with a simulated response
    with patch("onos_sdn.client.requests.get", return_value=mock_response) as mock_get:
        client = ONOSClient()
        result = client.get_flows(device_id)

    # Verify that the correct device was requested
    mock_get.assert_called_once_with(
        f"http://localhost:8181/onos/v1/flows/{device_id}",
        auth=client.auth,
        timeout=10
    )

    # Verify the returned flow information
    assert len(result) == 2
    assert result[0]["packets"] == 150
    assert result[1]["bytes"] == 6000

import pytest
import requests


def test_get_topology_http_error():
    # Simulate an HTTP 404 response from ONOS
    mock_response = Mock()
    mock_response.status_code = 404

    # Raise an HTTPError when the status is checked
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error",
        response=mock_response
    )

    # Replace the real request with a simulated error response
    with patch("onos_sdn.client.requests.get", return_value=mock_response):
        client = ONOSClient()

        # Verify that the HTTP error is propagated
        with pytest.raises(requests.exceptions.HTTPError) as error:
            client.get_topology()

    assert error.value.response.status_code == 404        


def test_add_flow_rule():
    # Define a sample flow configuration
    device_id = "of:0000000000000001"
    dst_ip = "10.0.0.2"
    out_port = 2

    # Simulate a successful HTTP POST response
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.raise_for_status.return_value = None

    with patch("onos_sdn.client.requests.post", return_value=mock_response) as mock_post:
        client = ONOSClient()

        status = client.add_flow_rule(
            device_id=device_id,
            dst_ip=dst_ip,
            out_port=out_port
        )

    # Verify the HTTP response status
    assert status == 201

    # Verify the POST request and its JSON payload
    mock_post.assert_called_once()

    args, kwargs = mock_post.call_args

    assert args[0] == (
        "http://localhost:8181/onos/v1/flows/"
        "of:0000000000000001"
    )

    assert kwargs["json"]["deviceId"] == device_id
    assert kwargs["json"]["selector"]["criteria"][1]["ip"] == "10.0.0.2/32"
    assert kwargs["json"]["treatment"]["instructions"][0]["port"] == "2"
    assert kwargs["timeout"] == 10
