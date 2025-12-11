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
