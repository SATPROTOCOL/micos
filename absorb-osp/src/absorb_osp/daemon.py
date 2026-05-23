"""
absorb-osp — Daemon Mode

Runs in the background to:
1. Listen for webhooks on a configurable port
2. Watch a directory for URL files (drop *.url files to trigger)
3. Log all events for audit
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

from .lib.workflow import WorkflowEngine

logger = logging.getLogger("absorb-osp-daemon")


def start_daemon(port: int = 8765, watch_dir: Optional[str] = None):
    """Start the absorb-osp daemon.

    Args:
        port: Port for webhook listener (HTTP POST /absorb)
        watch_dir: Directory to watch for *.url files
    """
    _setup_logging()
    engine = WorkflowEngine()

    print(f"\n🚀 absorb-osp daemon starting...")
    print(f"   Webhook port: {port}")
    print(f"   Watch directory: {watch_dir or 'not set'}")
    print(f"   Working dir: {engine.absorbed_dir}")
    print(f"\n📋 Available endpoints:")
    print(f"   POST http://localhost:{port}/absorb  — Trigger absorption")
    print(f"   GET  http://localhost:{port}/status  — Daemon status")
    print(f"   GET  http://localhost:{port}/health  — Health check")
    print("")

    if watch_dir:
        _watch_directory(watch_dir, engine)

    # Start webhook server
    _start_webhook_server(port, engine)


def _setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def _start_webhook_server(port: int, engine: WorkflowEngine):
    """Start a minimal HTTP webhook server."""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler

        class AbsorbHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == "/absorb":
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length).decode()
                    try:
                        data = json.loads(body)
                        url = data.get("url", "")
                        logger.info(f"Received absorption request: {url}")
                        engine.run(url)
                        self._respond(200, {"status": "ok", "url": url})
                    except Exception as e:
                        logger.error(f"Workflow failed: {e}")
                        self._respond(500, {"status": "error", "message": str(e)})
                else:
                    self._respond(404, {"status": "not_found"})

            def do_GET(self):
                if self.path == "/health":
                    self._respond(200, {"status": "healthy"})
                elif self.path == "/status":
                    projects = engine.list_absorbed()
                    self._respond(200, {
                        "status": "running",
                        "absorbed_count": len(projects),
                        "projects": [p["name"] for p in projects],
                    })
                else:
                    self._respond(404, {"status": "not_found"})

            def _respond(self, code: int, data: dict):
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            def log_message(self, fmt, *args):
                logger.info(f"{self.address_string()} - {fmt % args}")

        server = HTTPServer(("0.0.0.0", port), AbsorbHandler)
        logger.info(f"Webhook server listening on port {port}")
        server.serve_forever()

    except ImportError:
        logger.error("HTTP server not available in this environment")
    except OSError as e:
        logger.error(f"Failed to start server on port {port}: {e}")
    except KeyboardInterrupt:
        logger.info("Daemon stopped by user")


def _watch_directory(watch_dir: str, engine: WorkflowEngine):
    """Watch a directory for new *.url files.

    Each .url file should contain a GitHub URL as its first line.
    """
    import threading

    def watcher():
        path = Path(watch_dir)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Watching directory: {watch_dir}")

        seen = set()
        while True:
            for f in path.glob("*.url"):
                if f.name in seen:
                    continue
                seen.add(f.name)
                try:
                    url = f.read_text().strip()
                    if url and ("github.com" in url or url.startswith("http")):
                        logger.info(f"Detected URL file: {f.name} → {url}")
                        engine.run(url)
                        # Rename to mark as processed
                        f.rename(f.with_suffix(".processed"))
                except Exception as e:
                    logger.error(f"Failed to process {f.name}: {e}")
            time.sleep(2)

    t = threading.Thread(target=watcher, daemon=True)
    t.start()
