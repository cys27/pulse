import sys

from pulse.cli.dispatcher import dispatch


def main():
    try:
        exit_code = dispatch()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
