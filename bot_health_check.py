"""Basic project health check for FIN ASTRO BOT."""

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = [
    "main.py",
    "core/astro_engine.py",
    "core/yogas.py",
    "core/panchang.py",
    "core/hora.py",
    "core/dasha.py",
    "analysis/correlator.py",
    "analysis/projector.py",
    "analysis/backtester.py",
    "analysis/projection_backtester.py",
    "reports/daily_report.py",
    "reports/weekly_report.py",
    "market/data_fetcher.py",
    "market/symbols.py",
    "requirements.txt",
]


def main():
    print("🔎 FIN ASTRO BOT HEALTH CHECK")
    print("=" * 60)
    ok = True

    print("\nRequired files:")
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        exists = path.exists()
        print(f"  {'✅' if exists else '❌'} {rel}")
        ok = ok and exists

    print("\nPython syntax:")
    for path in sorted(ROOT.rglob("*.py")):
        if "venv" in path.parts or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8", errors="replace"))
            print(f"  ✅ {path.relative_to(ROOT)}")
        except Exception as e:
            ok = False
            print(f"  ❌ {path.relative_to(ROOT)} — {e}")

    print("\nRisky integer formatting scan:")
    risky = []
    for path in sorted(ROOT.rglob("*.py")):
        if "venv" in path.parts or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        patterns = ["weight" + ":3d", "score" + ":4d", "bullish_score" + ":4d", "bearish_score" + ":4d", "volatile_score" + ":4d"]
        if any(pat in text for pat in patterns):
            risky.append(path.relative_to(ROOT))
    if risky:
        ok = False
        for item in risky:
            print(f"  ⚠️ {item}")
    else:
        print("  ✅ No known risky weight/score integer formatting patterns found.")

    print("\nResult:")
    if ok:
        print("✅ Health check passed.")
        return 0
    print("❌ Health check found issues. Fix the items above before running the bot.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
