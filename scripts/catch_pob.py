#!/usr/bin/env python3
"""Tiny one-shot receiver: browser POSTs the PoB code here, we write it to disk.

Avoids passing a long base64 blob through the model, which corrupts it.
"""
import http.server
import pathlib
import sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "builds" / "labcummer.pob"


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8").strip()
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(body)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")
        print(f"received {len(body)} chars -> {OUT}", flush=True)
        sys.exit(0)

    def log_message(self, *args: object) -> None:
        pass


if __name__ == "__main__":
    http.server.HTTPServer(("127.0.0.1", 8799), Handler).serve_forever()
