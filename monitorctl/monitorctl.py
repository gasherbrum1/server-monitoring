import json
import os
import sys
import ipaddress
import urllib.request

TARGETS_FILE = os.environ.get("TARGETS_FILE", "/targets/manual_targets.json")
DEFAULT_PORT = int(os.environ.get("DEFAULT_PORT", "9100"))
PROM_RELOAD_URL = os.environ.get("PROM_RELOAD_URL", "http://prometheus:9090/-/reload")


def normalize_target(user_input: str) -> str:
    s = user_input.strip()
    if not s:
        raise ValueError("Empty input")

    host = s
    port = DEFAULT_PORT

    if ":" in s and s.count(":") == 1:
        host, p = s.split(":", 1)
        host = host.strip()
        p = p.strip()
        if not p.isdigit():
            raise ValueError("Port must be a number")
        port = int(p)

    try:
        ipaddress.ip_address(host)
    except ValueError:
        if " " in host or "/" in host:
            raise ValueError("Invalid IP/hostname format")

    if not (1 <= port <= 65535):
        raise ValueError("Port must be 1–65535")

    return f"{host}:{port}"


def load_targets(path: str):
    if not os.path.exists(path):
        return [{"targets": [], "labels": {"job": "manual"}}]

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_targets(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def reload_prometheus():
    try:
        req = urllib.request.Request(PROM_RELOAD_URL, method="POST")
        with urllib.request.urlopen(req, timeout=5):
            pass
        print("[ok] Prometheus reloaded.")
    except Exception as e:
        print(f"[warn] Could not reload Prometheus: {e}")


def main():
    raw = input("Enter the public IP of the instance you want to monitor: ").strip()
    try:
        target = normalize_target(raw)
    except ValueError as e:
        print(f"[error] {e}")
        sys.exit(1)

    data = load_targets(TARGETS_FILE)
    targets = data[0].setdefault("targets", [])

    if target in targets:
        print(f"[ok] Already present: {target}")
    else:
        targets.append(target)
        print(f"[ok] Added: {target}")
        save_targets(TARGETS_FILE, data)
        reload_prometheus()


if __name__ == "__main__":
    main()
