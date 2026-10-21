## linux-sdn-network-monitor

Implementation of a Linux-Based Software-Defined Network Monitoring and Flow Configuration Tool Using Python and REST APIs

The project provides a Python command-line application for monitoring network topology, OpenFlow devices, hosts, links, and flow statistics through an ONOS-style REST API.

A Flask-based network simulator supports HTTP GET and POST operations, enabling IPv4 forwarding rule configuration, parameter validation, and retrieval of configured flow entries.

The application was developed and tested in an Ubuntu 24.04 (WSL2) environment.

### Key Results

- Successfully implemented 5 REST API monitoring operations for network topology, devices, hosts, links, and flow statistics.
- Simulated an SDN topology consisting of 3 OpenFlow switches, 2 network links, and 2 hosts.
- Implemented HTTP POST-based flow configuration using destination IPv4 addresses and switch output ports.
- Successfully submitted forwarding rules and retrieved the stored configurations using HTTP GET.
- Implemented input validation and HTTP error handling.
- Passed 14 automated unit tests using pytest.

### Result Snapshots

[Network Monitoring](docs/results/network%20monitoring.png): Successful retrieval of simulated OpenFlow network devices and their availability status.

[Flow Configuration](docs/results/flow%20configuration.png): Configured forwarding rule retrieved through the REST API, demonstrating destination IP matching and switch output port selection.

**Keywords:** Python, Linux, Software-Defined Networking (SDN), ONOS REST API, OpenFlow, Network Monitoring, Flow Configuration, HTTP GET/POST, JSON, Flask, pytest.

**Development Environment:** Ubuntu 24.04 (WSL2), Python 3.

**Testing Environment:** Local Flask-Based ONOS-Style REST API Simulator.
