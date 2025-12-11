import socket


def grab_banner(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

            try:
                banner = sock.recv(1024)

                if banner:
                    return banner.decode(errors="ignore").strip()

            except socket.timeout:
                pass

            try:
                sock.sendall(b"Hey!")
                banner = sock.recv(1024)

                if banner:
                    return banner.decode(errors="ignore").strip()

            except Exception:
                pass

            return None

    except Exception:
        return None
