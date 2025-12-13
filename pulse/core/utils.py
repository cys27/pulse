# Utility functions for Pulse port scanner


def parse_ports(ports_input):
    ports = set()

    # Split by commas and handle ranges
    for port_spec in ports_input.split(","):
        port_spec = port_spec.strip()

        if "-" in port_spec:
            left, right = map(int, port_spec.split("-"))
            ports.update(range(left, right + 1))

        else:
            ports.add(int(port_spec))

    return sorted(ports)


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
