import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    result = []

    with ThreadPoolExecutor(max_workers=threads) as exec:
        futures = [
            exec.submit(scan_tcp_port, target_ip, port, timeout) for port in ports
        ]

        try:
            for future in as_completed(futures):
                try:
                    scan_result = future.result()
                    proc = process_result(scan_result)

                    if proc:
                        result.append(proc)

                except Exception:
                    pass

        except KeyboardInterrupt:
            for future in futures:
                future.cancel()

            exec.shutdown(wait=False)
            raise

        return result
