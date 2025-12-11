import json
import os


def load_servicesJson():
    servicesJson_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "services.json"
    )

    try:
        with open(servicesJson_path, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_service_name(port, services=None):
    if services is None:
        services = load_servicesJson()

    return services.get(str(port), "Unknown")


def print_tcp_results(results, scan_type="TCP", show_banner=False):
    services = load_servicesJson()

    open_ports = [res for res in results if res.get("status") == "open"]

    if not open_ports:
        print(f"\n[*] No open {scan_type} ports found.\n")
        return

    open_ports.sort(key=lambda x: x["port"])

    print(f"\n[+] Found {len(open_ports)} open {scan_type} port(s):\n")

    if show_banner:
        print(f"{'PORT':<10} {'STATE':<12} {'SERVICE':<20} {'BANNER'}")
    else:
        print(f"{'PORT':<10} {'STATE':<12} {'SERVICE':<20}")

    # Print each result
    for result in open_ports:
        port = result["port"]
        status = result.get("status", "unknown")
        service = get_service_name(port, services)
        banner = result.get("banner", "") or ""

        if show_banner:
            # remove newlines and extra spaces
            banner = banner.replace("\n", " ").replace("\r", " ").strip()

            # Truncate banner if too long
            if len(banner) > 40:
                banner = banner[:37] + "..."
            print(f"{port:<10} {status:<12} {service:<20} {banner}")
        else:
            print(f"{port:<10} {status:<12} {service:<20}")

    print()


"""
def print_udp_results(results):
    # ...
"""

"""
if __name__ == "__main__":
    test -> print(get_service_name(443)) // Returns HTTPS
"""
