import argparse
import json
import requests

from onos_sdn.client import ONOSClient


def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Linux-based SDN Network Monitor"
    )

    parser.add_argument(
        "command",
        choices=[
            "topology", "devices", "hosts",
            "links", "flows", "add-flow"
        ],
        help="Select a monitoring or configuration operation"
    )

    parser.add_argument(
        "--device",
        help="OpenFlow device ID"
    )

    parser.add_argument(
        "--dst-ip",
        help="Destination IPv4 address for a flow rule"
    )

    parser.add_argument(
        "--out-port",
        help="Switch output port for a flow rule"
    )

    args = parser.parse_args()

    # Validate required command arguments
    if args.command in ("flows", "add-flow") and not args.device:
        parser.error("--device is required")

    if args.command == "add-flow":
        if not args.dst_ip or not args.out_port:
            parser.error("--dst-ip and --out-port are required")

    client = ONOSClient()

    # Execute the selected operation
    try:
        if args.command == "topology":
            result = client.get_topology()

        elif args.command == "devices":
            result = client.get_devices()

        elif args.command == "hosts":
            result = client.get_hosts()

        elif args.command == "links":
            result = client.get_links()

        elif args.command == "flows":
            result = client.get_flows(args.device)

        elif args.command == "add-flow":
            result = {
                "status_code": client.add_flow_rule(
                    args.device,
                    args.dst_ip,
                    args.out_port
                ),
                "message": "Flow configuration request accepted"
            }

        # Display formatted JSON
        print(json.dumps(result, indent=4))

    except requests.exceptions.Timeout:
        print("ERROR: Controller request timed out")
        raise SystemExit(1)

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to controller at localhost:8181")
        raise SystemExit(1)

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        print(f"ERROR: API returned HTTP status {status}")
        raise SystemExit(1)

    except ValueError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
