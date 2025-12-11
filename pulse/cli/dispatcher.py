import datetime
import socket
import time

from pulse.cli import BANNER
from pulse.cli.arguments import get_args
from pulse.core.banner import grab_banner
from pulse.core.tcp_scan import tcp_scan
from pulse.output.json_writer import print_asJson, save_asJson
from pulse.output.printer import print_tcp_results


def get_full_time():
    now = datetime.datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M")

    return formatted


def resolve_hostname(target):
    try:
        ip = socket.gethostbyname(target)
        return ip

    except socket.gaierror:
        return None


def add_banners(result, target, timeout):
    for res in result:
        if res.get("status") == "open":
            banner = grab_banner(target, res["port"], timeout)
            res["banner"] = banner

    return result


def run_tcp_scan(args, target):
    print(f"[*] Starting TCP scan on {target}")
    print(f"[*] Started at {get_full_time()}")

    tcp_results = tcp_scan(args)

    if args.banner and tcp_results:
        print("[*] Grabbing banners from open ports.")
        tcp_results = add_banners(tcp_results, target, args.timeout)

    return tcp_results


"""
def run_udp_scan(args, target):
    # ...
"""


def dispatch():
    print(BANNER)

    args = get_args()

    target_ip = resolve_hostname(args.target)

    if target_ip is None:
        print(f"[!] Error: Could not resolve hostname '{args.target}'")
        return 1

    _target_temp = args.target
    args.target = target_ip

    scan_types = []

    if args.tcp:
        scan_types.append("TCP")

    # scan_type_as_str = (" + ").join(scan_types)

    # print header
    if not args.json:
        # print
        print("")

    # record start time
    start_time = time.time()

    # results
    tcp_results = None
    # udp_results = None

    try:
        if args.tcp:
            tcp_results = run_tcp_scan(args, target_ip)

        """
        if args.udp:
            udp_results = run_udp_scan(args, target_ip)
        """

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        return 130

    except Exception as err:
        print(f"[!] Error during scan: {err}")
        return 1

    elapsed_time = time.time() - start_time

    # Output results
    if args.output:
        save_asJson(
            args.output,
            f"{_target_temp} ({target_ip})" if _target_temp != target_ip else target_ip,
            args,
            elapsed_time,
            tcp_results,
        )
        print(f"[*] Results saved to {args.output}")

    if args.json:
        print_asJson(target_ip, args, elapsed_time, tcp_results)

    else:
        if tcp_results is not None:
            print_tcp_results(tcp_results, scan_type="TCP", show_banner=args.banner)

        print(f"[*] Scan completed in {elapsed_time:.2f} seconds.")

    return 0
