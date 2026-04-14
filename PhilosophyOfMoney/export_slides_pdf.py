from __future__ import annotations

import contextlib
import shutil
import socket
import subprocess
import threading
import time
import urllib.parse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "money-philosophy-slides.html"
PDF_FILE = BASE_DIR / "money-philosophy-slides.pdf"


class QuerySafeHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        clean_path = urllib.parse.urlsplit(path).path
        return super().translate_path(clean_path)

    def log_message(self, format: str, *args) -> None:
        return


def find_free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def find_chrome() -> Path:
    candidates = [
        shutil.which("chrome.exe"),
        shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)

    raise FileNotFoundError("Could not find Chrome or Edge for PDF export.")


def wait_for_server(port: int, timeout_seconds: float = 5.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.1)
    raise TimeoutError(f"Local export server on port {port} did not start in time.")


def export_pdf() -> None:
    if not HTML_FILE.exists():
        raise FileNotFoundError(f"Missing slideshow HTML: {HTML_FILE}")

    port = find_free_port()
    handler = partial(QuerySafeHandler, directory=str(BASE_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)

    try:
        thread.start()
        wait_for_server(port)

        chrome = find_chrome()
        url = f"http://127.0.0.1:{port}/{HTML_FILE.name}?print-pdf"

        command = [
            str(chrome),
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=15000",
            f"--print-to-pdf={PDF_FILE}",
            "--print-to-pdf-no-header",
            url,
        ]

        subprocess.run(command, check=True, timeout=60)

    finally:
        server.shutdown()
        server.server_close()

    if not PDF_FILE.exists() or PDF_FILE.stat().st_size < 10_000:
        raise RuntimeError(f"PDF export failed or produced an unexpectedly small file: {PDF_FILE}")

    print(f"Saved PDF: {PDF_FILE}")
    print(f"Size: {PDF_FILE.stat().st_size} bytes")


if __name__ == "__main__":
    export_pdf()