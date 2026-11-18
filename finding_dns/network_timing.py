import ssl
import socket
import sys
import time
from urllib.parse import urlparse
import http.client
import json


def measure_request(url):
    timings = {}

    # Parse the url
    parsed = urlparse(url)

    hostname = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    use_tls = parsed.scheme == "https"

    if not hostname or parsed.scheme not in ("http", "https"):
        raise ValueError("Please provide a valid HTTP or HTTPS URL")

    total_start = time.perf_counter()

    # Measure DNS resolution time
    start = time.perf_counter()
    addresses = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    timings["dns_ms"] = round((time.perf_counter() - start) * 1000, 2)

    family, socktype, proto, _, sockaddr = addresses[0]

    sock = socket.socket(family, socktype, proto)
    sock.settimeout(15)

    try:
        # Measure TCP timing
        start = time.perf_counter()
        sock.connect(sockaddr)
        timings["tcp_ms"] = round((time.perf_counter() - start) * 1000, 2)

        # Measure TLS timing
        if use_tls:
            context = ssl.create_default_context()
            start = time.perf_counter()
            sock = context.wrap_socket(sock, server_hostname=hostname)
            timings["tls_ms"] = round((time.perf_counter() - start) * 1000, 2)
        else:
            timings["tls_ms"] = 0

        # Measure HTTP timing
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        host = hostname
        if parsed.port:
            host += f":{parsed.port}"

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"
            "User-Agent: NetworkMonitor/1.0\r\n"
            "\r\n"
        )

        start = time.perf_counter()
        sock.sendall(request.encode())

        response = http.client.HTTPResponse(sock)
        response.begin()

        timings["ttfb_ms"] = round((time.perf_counter() - start) * 1000, 2)

        # Measure download timing
        start = time.perf_counter()
        body = response.read()
        timings["download_ms"] = round((time.perf_counter() - start) * 1000, 2)

        timings["total_ms"] = round((time.perf_counter() - total_start) * 1000, 2)

        return {
            "url": url,
            "status_code": response.status,
            "response_size_bytes": len(body),
            "timings": timings,
        }
    finally:
        sock.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python network_timing.py <url>")
        sys.exit(1)

    try:
        result = measure_request(sys.argv[1])
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
