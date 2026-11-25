"""A small JSON API over NOAA tide predictions: GET /stations and GET /stations/<id>/tides."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def stations() -> list[dict]:
    return json.loads((DATA / "stations.json").read_text())


def tides(station_id: str) -> list[dict] | None:
    path = DATA / f"hilo-{station_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())["predictions"]


def route(path: str) -> tuple[int, object]:
    parts = [p for p in path.split("?")[0].split("/") if p]
    if parts == ["stations"]:
        return 200, stations()
    if len(parts) == 3 and parts[0] == "stations" and parts[2] == "tides":
        found = tides(parts[1])
        return (200, found) if found is not None else (404, {"error": f"no station {parts[1]}"})
    return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = route(self.path)
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def serve(port: int = 8740) -> None:
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
