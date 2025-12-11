import socket


def grab_banner(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

            read_timeout = 2.0 if timeout > 2.0 else timeout
            sock.settimeout(read_timeout)

            try:
                banner = sock.recv(1024)

                if banner:
                    return banner.decode(errors="ignore").strip()

            except socket.timeout:
                pass

            sock.settimeout(timeout)

            try:
                probe = b"HEAD / HTTP/1.0\r\n\r\n"
                sock.sendall(probe)
                
                banner = sock.recv(1024)

                if banner:
                    return banner.decode(errors="ignore").strip()

            except Exception:
                pass

            return None

    except Exception:
        return None
