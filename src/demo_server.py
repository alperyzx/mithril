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

from src.alarm_core import analyze, load_scenario


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(__file__).resolve().parent / "demo_assets"
DATA_DIR = ROOT / "docs" / "project" / "senaryo"


class DemoState:
    """Keeps deterministic correlation results and raw-data evidence in memory."""

    def __init__(self) -> None:
        self.report = analyze(DATA_DIR)
        self.alarms, _, self.dependencies = load_scenario(DATA_DIR)

    def dashboard(self) -> dict[str, Any]:
        cards = []
        for card in self.report["incident_cards"]:
            rendered = dict(card)
            cards.append(rendered)
        return {
            "input_alarm_count": self.report["input_alarm_count"],
            "incident_card_count": len(cards),
            "max_incident_cards": 15,
            "incident_cards": cards,
            "noise_summary": self.report["noise_summary"],
            "noise_total": sum(self.report["noise_summary"].values()),
        }

    def evidence(self, incident_id: str) -> dict[str, Any]:
        card = next((item for item in self.report["incident_cards"] if item["incident_id"] == incident_id), None)
        if card is None:
            raise KeyError(incident_id)
        rows = [
            alarm for alarm in self.alarms
            if card["start_at"] <= alarm["timestamp"] <= card["end_at"]
            and alarm["service"] in card["affected_services"]
        ]
        rows.sort(key=lambda alarm: alarm["timestamp"])
        type_counts: dict[str, int] = {}
        service_counts: dict[str, int] = {}
        source_counts: dict[str, int] = {}
        for alarm in rows:
            type_counts[alarm["alarm_type"]] = type_counts.get(alarm["alarm_type"], 0) + 1
            service_counts[alarm["service"]] = service_counts.get(alarm["service"], 0) + 1
            source_counts[alarm["source_system"]] = source_counts.get(alarm["source_system"], 0) + 1
        return {
            "incident_id": incident_id,
            "window": {"start_at": card["start_at"], "end_at": card["end_at"]},
            "raw_alarm_count": len(rows),
            "alarm_type_counts": dict(sorted(type_counts.items(), key=lambda item: (-item[1], item[0]))),
            "service_counts": dict(sorted(service_counts.items(), key=lambda item: (-item[1], item[0]))),
            "source_system_counts": dict(sorted(source_counts.items(), key=lambda item: (-item[1], item[0]))),
            "sample_alarms": [
                {
                    "timestamp": alarm["timestamp"],
                    "service": alarm["service"],
                    "host": alarm["host"],
                    "severity": alarm["severity"],
                    "alarm_type": alarm["alarm_type"],
                }
                for alarm in rows[:12]
            ],
        }


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
            if path.startswith("/api/evidence/"):
                incident_id = path.removeprefix("/api/evidence/")
                try:
                    self._send_json(state.evidence(incident_id))
                except KeyError:
                    self._send_json({"error": "Olay kartı bulunamadı."}, HTTPStatus.NOT_FOUND)
                return
            if path == "/":
                path = "/index.html"
            if path not in {"/index.html", "/dashboard.css", "/dashboard.js"}:
                self._send_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)
                return
            asset = ASSET_ROOT / path.lstrip("/")
            content_type = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
            self._send(asset.read_bytes(), f"{content_type}; charset=utf-8")

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