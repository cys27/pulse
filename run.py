#!/usr/bin/env python3
import sys

from pulse.cli.dispatcher import dispatch
from pulse.core.utils import Colors


def main():
    try:
        exit_code = dispatch()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] Interrupted by user.{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.FAIL}[!] Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
