"""Read Codex's local app-server API and send sanitized usage over USB serial."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


class Singleton:
    """OS file lock releases automatically if the process exits or is killed."""
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.file = path.open("a+b")
        self.file.seek(0)
        if os.fstat(self.file.fileno()).st_size == 0:
            self.file.write(b"0")
            self.file.flush()
        self.file.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.file.close()
            raise RuntimeError("Usage bridge is already running") from None

    def close(self):
        self.file.close()


class Status:
    """One small, overwritten file; never store raw API or serial content."""
    def __init__(self, path):
        self.path = path
        self.data = {"pid": os.getpid(), "running": True, "api_state": "connecting",
                     "last_api_sample": None, "com": None, "ack_received": None,
                     "ack_updated": None, "sd": None}

    def sample(self, packet):
        self.data["last_api_sample"] = packet
        self.data["api_state"] = "ok"

    def ack(self, line, now=None):
        try:
            value = json.loads(line)
        except (ValueError, UnicodeDecodeError):
            return
        if not isinstance(value, dict) or value.get("type") != "ack":
            return
        updated = value.get("updated")
        if not finite_number(updated) or updated < 0:
            return
        self.data["ack_received"] = int(time.time() if now is None else now)
        self.data["ack_updated"] = int(updated)
        self.data["sd"] = value.get("sd") if isinstance(value.get("sd"), bool) else None
        capacity = value.get("sd_mb")
        self.data["sd_mb"] = int(capacity) if finite_number(capacity) and capacity >= 0 else None

    def write(self):
        self.data["updated"] = int(time.time())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        try:
            temporary.write_text(json.dumps(self.data, separators=(",", ":")) + "\n", encoding="utf-8")
            temporary.replace(self.path)
        except OSError:
            # Antivirus/readers may briefly prevent replacement; retry next loop.
            pass


def usage_packet(response, now=None):
    """Never infer 0% from absent fields or infer a window from its position."""
    buckets = response.get("rateLimitsByLimitId")
    if isinstance(buckets, dict) and buckets:
        bucket = buckets.get("codex")
        if not isinstance(bucket, dict):
            bucket = next((v for v in buckets.values() if isinstance(v, dict) and v.get("limitId") == "codex"), None)
        # Do not accidentally display a model-specific bucket as account usage.
    else:
        bucket = response.get("rateLimits")
    windows = []
    if isinstance(bucket, dict):
        for key in ("primary", "secondary"):
            window = bucket.get(key)
            if not isinstance(window, dict) or not finite_number(window.get("usedPercent")):
                continue
            minutes = window.get("windowDurationMins")
            minutes = int(minutes) if finite_number(minutes) and minutes > 0 else None
            label = {300: "5H", 10080: "WEEK"}.get(minutes, "OTHER")
            reset = window.get("resetsAt")
            reset = int(reset) if finite_number(reset) and reset > 0 else None
            windows.append({"label": label, "used": max(0, min(100, window["usedPercent"])), "reset": reset, "minutes": minutes})
    windows.sort(key=lambda w: w["minutes"] if w["minutes"] is not None else float("inf"))
    return {"type": "usage", "windows": windows, "updated": int(time.time() if now is None else now)}


class AppServer:
    def __init__(self, executable):
        self.executable = executable
        self.process = None
        self.messages = queue.Queue()
        self.request_id = 0

    def close(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process = None

    def start(self):
        self.close()
        self.messages = queue.Queue()
        self.process = subprocess.Popen(
            [self.executable, "app-server", "--stdio"], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), bufsize=1,
        )
        def reader(stream, messages):
            for line in stream:
                try:
                    messages.put(json.loads(line))
                except json.JSONDecodeError:
                    pass
            messages.put(None)
        threading.Thread(target=reader, args=(self.process.stdout, self.messages), daemon=True).start()
        self.request("initialize", {"clientInfo": {"name": "codex_usage_display", "version": "1.0.0"}})
        self.send({"method": "initialized"})

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params=None):
        self.request_id += 1
        request_id = self.request_id
        message = {"id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self.send(message)
        deadline = time.monotonic() + 30
        while True:
            try:
                response = self.messages.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty:
                raise RuntimeError("Codex request timed out") from None
            if response is None:
                raise RuntimeError("Codex app-server stopped")
            if response.get("id") == request_id:
                if "error" in response:
                    # Raw errors may contain account details. Never print or transmit them.
                    raise RuntimeError("Codex usage unavailable; check desktop sign-in")
                return response.get("result", {})

    def read_usage(self):
        if not self.process or self.process.poll() is not None:
            self.start()
        return usage_packet(self.request("account/rateLimits/read"))


def find_port(explicit=None):
    from serial.tools import list_ports
    if explicit:
        return explicit
    matches = [p.device for p in list_ports.comports() if p.vid == 0x303A and p.pid == 0x1001]
    if len(matches) > 1:
        raise RuntimeError("Multiple ESP32 boards; select --port")
    return matches[0] if matches else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default=shutil.which("codex.exe") or shutil.which("codex"))
    parser.add_argument("--port", help="Optional COM port; default detects ESP32 USB VID/PID")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--once", action="store_true", help="Read and print sanitized usage once; no serial connection")
    parser.add_argument("--status-file", type=Path, default=Path(__file__).resolve().parent / "runtime" / "status.json")
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI was not found; pass --codex PATH")
    if args.interval < 30:
        parser.error("--interval must be at least 30 seconds")
    server = AppServer(args.codex)
    connection = None
    singleton = None
    status = None
    try:
        if args.once:
            print(json.dumps(server.read_usage(), separators=(",", ":")))
            return
        import serial
        # Lock is fixed per installed bridge, independently of a custom status path.
        try:
            singleton = Singleton(Path(__file__).resolve().parent / "runtime" / "bridge.lock")
        except RuntimeError:
            return
        status = Status(args.status_file)
        packet = {"type": "status", "message": "Connecting to Codex"}
        next_poll = 0
        last_sent = 0
        serial_buffer = b""
        while True:
            now = time.monotonic()
            if now >= next_poll:
                try:
                    packet = server.read_usage()
                    status.sample(packet)
                except Exception:
                    server.close()
                    packet = {"type": "status", "message": "Codex unavailable - check PC"}
                    status.data["api_state"] = "unavailable"
                next_poll = time.monotonic() + args.interval
                last_sent = 0
            try:
                if connection is None:
                    port = find_port(args.port)
                    if port:
                        connection = serial.Serial(port, 115200, timeout=0, write_timeout=2)
                        status.data["com"] = port
                        serial_buffer = b""
                        last_sent = 0
                if connection:
                    # Resend to cover a board reset; updated remains the actual sample time.
                    if time.monotonic() - last_sent >= 5:
                        connection.write((json.dumps(packet, separators=(",", ":")) + "\n").encode("utf-8"))
                        last_sent = time.monotonic()
                    serial_buffer += connection.read(min(connection.in_waiting, 4096))
                    while b"\n" in serial_buffer:
                        line, serial_buffer = serial_buffer.split(b"\n", 1)
                        status.ack(line)
                    serial_buffer = serial_buffer[-4096:]
            except (serial.SerialException, OSError, RuntimeError):
                if connection:
                    connection.close()
                connection = None
                status.data["com"] = None
            status.write()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        if connection:
            connection.close()
        server.close()
        if status:
            status.data["running"] = False
            status.data["com"] = None
            status.write()
        if singleton:
            singleton.close()


if __name__ == "__main__":
    main()
