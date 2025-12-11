import socket

from pulse.core.threading_pool import threaded_scan
from pulse.core.utils import parse_ports


def scan_tcp_port(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((host, port))

            if result == 0:
                return port, True

        except socket.error:
            pass

    return port, False


def process_result(scan_result):
    port, is_open = scan_result

    if not is_open:
        return None

    return {"port": port, "status": "open"}


def tcp_scan(args):
    target_ip = args.target
    timeout = args.timeout
    threads = args.threads
    ports = parse_ports(args.ports)

    return threaded_scan(
        scan_func=scan_tcp_port,
        target_ip=target_ip,
        threads=threads,
        timeout=timeout,
        ports=ports,
        proc_func=process_result,
    )
