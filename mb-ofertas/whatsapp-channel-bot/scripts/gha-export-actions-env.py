#!/usr/bin/env python3
"""
Imprime linhas `export VAR=...` para `eval` no bash.
O runner injeta ACTIONS_* no processo pai; o shell do step nem sempre os repassa ao Node.
Percorre a cadeia PPid em /proc até achar ACTIONS_RUNTIME_TOKEN e ACTIONS_RESULTS_URL.
"""
from __future__ import annotations

import os
import shlex
import sys

KEYS = ("ACTIONS_RUNTIME_TOKEN", "ACTIONS_RESULTS_URL")


def read_environ(pid: int) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        with open(f"/proc/{pid}/environ", "rb") as f:
            for part in f.read().split(b"\0"):
                if not part or b"=" not in part:
                    continue
                k, v = part.split(b"=", 1)
                ks = k.decode("utf-8", "replace")
                out[ks] = v.decode("utf-8", "replace")
    except OSError:
        pass
    return out


def ppid_of(pid: int) -> int | None:
    try:
        with open(f"/proc/{pid}/status") as fh:
            for line in fh:
                if line.startswith("PPid:"):
                    return int(line.split()[1])
    except (OSError, ValueError, IndexError):
        pass
    return None


def main() -> int:
    missing = {k for k in KEYS if not os.environ.get(k)}
    if not missing:
        return 0
    pid = os.getpid()
    for _ in range(24):
        pid = ppid_of(pid)
        if pid is None or pid <= 1:
            break
        env = read_environ(pid)
        for k in list(missing):
            val = env.get(k, "")
            if val:
                print(f"export {k}={shlex.quote(val)}")
                missing.discard(k)
        if not missing:
            return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
