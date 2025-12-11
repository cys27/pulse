import datetime
import json
import os


def generate_json_output(
    target, args=None, elapsed_time=None, tcp_results=None, udp_results=None
):
    output = {
        "scan_info": {
            "target": target,
            "timestamp": datetime.datetime.now().isoformat(),
            "scan_duration_seconds": elapsed_time,
        },
        "scan_options": {},
        "results": {},
    }

    if args:
        output["scan_options"] = {
            "ports": args.ports,
            "tcp_scan": args.tcp,
            "udp_scan": args.udp,
            "banner_grab": args.banner,
            "threads": args.threads,
            "timeout": args.timeout,
        }

    if tcp_results is not None:
        open_tcp = [r for r in tcp_results if r.get("status") == "open"]
        output["results"]["tcp"] = {
            "total_scanned": len(tcp_results) if tcp_results else 0,
            "open_ports_count": len(open_tcp),
            "open_ports": sorted(open_tcp, key=lambda x: x["port"]),
        }

    return output


def print_asJson(
    target, args=None, elapsed_time=None, tcp_results=None, udp_results=None
):
    output = generate_json_output(target, args, elapsed_time, tcp_results, udp_results)

    print(json.dumps(output, indent=4))


def save_asJson(
    filename, target, args=None, elapsed_time=None, tcp_results=None, udp_results=None
):
    output = generate_json_output(target, args, elapsed_time, tcp_results, udp_results)

    directory = os.path.dirname(filename)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, "w") as file:
        json.dump(output, file, indent=4)

    return filename
