# Threading pool utilities for concurrent port scanning

from concurrent.futures import ThreadPoolExecutor, as_completed


def threaded_scan(scan_func, target_ip, ports, timeout, threads, proc_func=None):
    result = []

    with ThreadPoolExecutor(max_workers=threads) as exec:
        futures = [exec.submit(scan_func, target_ip, port, timeout) for port in ports]

        try:
            for future in as_completed(futures):
                try:
                    scan_result = future.result()

                    if proc_func:
                        proc = proc_func(scan_result)

                        if proc is not None:
                            result.append(proc)

                    else:
                        result.append(scan_result)

                except Exception:
                    pass

        except KeyboardInterrupt:
            # Cancel
            for future in futures:
                future.cancel()

            exec.shutdown(wait=False)
            raise

        exec.shutdown(wait=True)

    return result
