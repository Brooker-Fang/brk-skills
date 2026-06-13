#!/usr/bin/env python3
"""commit-msg 钩子 — 保护路径守卫（spec-harness 的确定性层）。

改动了 .specharness/protected.txt 所列保护路径的提交，若 commit message 没有
`OVERRIDE: <原因>` 一行，则拦下。protected.txt 把自己也列为保护路径，防止
「删清单来绕过守卫」。无第三方依赖，跨平台。

安装：
  POSIX :  cp templates/commit-msg-protected.py .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg
  Windows:  copy 到 .git/hooks/commit-msg（确保 python 在 PATH；git 用 sh 调用，shebang 生效）
"""

from __future__ import annotations

import fnmatch
import pathlib
import subprocess
import sys

PROTECTED_LIST = pathlib.Path(".specharness/protected.txt")


def _staged_files() -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def _patterns() -> list[str]:
    if not PROTECTED_LIST.exists():
        return []
    return [
        ln.strip()
        for ln in PROTECTED_LIST.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]


def _matches(path: str, pattern: str) -> bool:
    base = pattern.rstrip("/")
    return path == base or path.startswith(base + "/") or fnmatch.fnmatch(path, pattern)


def main() -> int:
    msg = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    patterns = _patterns()
    if not patterns:
        return 0
    hits = sorted({f for f in _staged_files() for p in patterns if _matches(f, p)})
    if hits and "OVERRIDE:" not in msg:
        print("DETECTED: 改动了保护路径但提交信息无 OVERRIDE 说明：", file=sys.stderr)
        for h in hits:
            print(f"  - {h}", file=sys.stderr)
        print(
            "FIX: 确属必要则在 commit message 加一行 'OVERRIDE: <原因>'（强制留痕）；"
            "否则撤回这些改动。",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
