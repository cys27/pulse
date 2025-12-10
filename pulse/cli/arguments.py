import argparse


def get_args():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Pulse is a lightweight TCP/UDP port scanner"
    )

    # Define command-line arguments

    ## Target specification
    parser.add_argument(
        "-t", "--target", required=True, help="IP address of the target to scan"
    )

    ## Port range specification
    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help='Port range to scan (e.g., "1-1024" or "80,443,8080")',
    )

    # Scan type options

    ## TCP scan option
    parser.add_argument("--tcp", action="store_true", help="Perform a TCP port scan")

    """

    ## UDP scan option
    parser.add_argument(
        '--udp',
        action='store_true',
        help='Perform a UDP port scan'
    )

    """

    # Additional options

    ## Banner grabbing option
    parser.add_argument(
        "--banner",
        "--withBanners",
        action="store_true",
        help="Attempt to retrieve service banners from open ports",
    )

    ## Number of threads option
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of concurrent threads to use for scanning",
    )

    ## Timeout option
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout in seconds for each port scan attempt",
    )

    ## Save the output as json
    parser.add_argument(
        "--json",
        "--saveAsJson",
        action="store_true",
        help="Save the results in JSON format",
    )

    # Parse the arguments
    args = parser.parse_args()

    """

    # Validate that at least one scan type is selected
    if not args.tcp and not args.udp:
        parser.error('At least one of --tcp or --udp must be specified.')

    """

    return args
