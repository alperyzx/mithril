#!/usr/bin/env python3
"""Local, dependency-free demo server for the S-A1 alarm correlation flow."""

from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from src.alarm_core import analyze


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(__file__).resolve().parent / "demo_assets"
DATA_DIR = ROOT / "docs" / "project" / "senaryo"
VALID_ACTION_STATUSES = ("open", "in_progress", "blocked", "resolved")


class DemoState:
    """Keeps the deterministic report and demo-only action state in memory."""

    def __init__(self) -> None:
        self.report = analyze(DATA_DIR)
        self.action_statuses = {
            card["incident_id"]: card["action_status"]
            for card in self.report["incident_cards"]
        }

    def dashboard(self) -> dict[str, Any]:
        cards = []
        for card in self.report["incident_cards"]:
            rendered = dict(card)
            rendered["action_status"] = self.action_statuses[card["incident_id"]]
            cards.append(rendered)
        return {
            "input_alarm_count": self.report["input_alarm_count"],
            "incident_card_count": len(cards),
            "max_incident_cards": 15,
            "incident_cards": cards,
            "noise_summary": self.report["noise_summary"],
            "noise_total": sum(self.report["noise_summary"].values()),
        }

    def update_action(self, incident_id: str, status: str) -> dict[str, str]:
        if incident_id not in self.action_statuses:
            raise KeyError(incident_id)
        if status not in VALID_ACTION_STATUSES:
            raise ValueError(status)
        self.action_statuses[incident_id] = status
        return {"incident_id": incident_id, "action_status": status}


def make_handler(state: DemoState) -> type[BaseHTTPRequestHandler]:
    class DemoHandler(BaseHTTPRequestHandler):
        server_version = "MithrilDemo/1.0"

        def log_message(self, format: str, *args: object) -> None:
            print("[demo] " + format % args)

        def _send(self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, value: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
            self._send(
                json.dumps(value, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8",
                status,
            )

        def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            path = urlparse(self.path).path
            if path == "/api/dashboard":
                self._send_json(state.dashboard())
                return
            if path == "/":
                path = "/index.html"
            if path not in {"/index.html", "/dashboard.css", "/dashboard.js"}:
                self._send_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)
                return
            asset = ASSET_ROOT / path.lstrip("/")
            content_type = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
            self._send(asset.read_bytes(), f"{content_type}; charset=utf-8")

        def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            prefix = "/api/cards/"
            suffix = "/action"
            path = urlparse(self.path).path
            if not (path.startswith(prefix) and path.endswith(suffix)):
                self._send_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)
                return
            incident_id = path[len(prefix):-len(suffix)].strip("/")
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                result = state.update_action(incident_id, payload["status"])
            except (json.JSONDecodeError, KeyError, ValueError):
                self._send_json(
                    {"error": "Geçerli bir kart ve durum gönderin."},
                    HTTPStatus.BAD_REQUEST,
                )
                return
            self._send_json(result)

    return DemoHandler


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Mithril S-A1 demo dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", default=8000, type=int, help="Bind port (default: 8000)")
    args = parser.parse_args()

    state = DemoState()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(state))
    print(f"Mithril demo hazır: http://{args.host}:{args.port}")
    print("Durdurmak için Ctrl+C kullanın.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMithril demo durduruldu.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()