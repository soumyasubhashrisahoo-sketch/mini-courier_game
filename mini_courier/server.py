"""Serve the browser game (docs/index.html) from a tiny local web server."""

import functools
import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def serve_game(port: int = 8000, open_browser: bool = True) -> None:
    if not (DOCS_DIR / "index.html").exists():
        raise SystemExit(f"Game file not found: {DOCS_DIR / 'index.html'}")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS_DIR))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://localhost:{port}/"
        print(f"Courier Dash is running at {url}")
        print("Press Ctrl+C to stop.")
        if open_browser:
            threading.Timer(0.5, webbrowser.open, args=(url,)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
