"""
=============================================================
FIN ASTRO BOT v2.5 — Daily Report Generator
=============================================================
"""

import os
from datetime import datetime
from typing import Any

from analysis.projector import generate_full_projection

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def generate_daily_report(date_str=None, symbol="nifty", dataset=None, save=True, verbose=True):
    """Generate and optionally save daily report."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(REPORT_DIR, exist_ok=True)
    result = generate_full_projection(date_str, symbol, dataset, return_result=True, verbose=verbose)

    if save:
        safe_sym = symbol.replace(" ", "_").replace("^", "")
        filename = os.path.join(REPORT_DIR, f"daily_{safe_sym}_{date_str}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("FIN ASTRO BOT v2.5 — DAILY REPORT\n")
            f.write(f"Model: {result.get('model_version', '')}\n")
            f.write(f"Date: {date_str} | Symbol: {symbol}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"GAP PROJECTION: {result['gap_projection']}\n")
            f.write(f"DAY BIAS: {result['bias']}\n")
            f.write(f"CONFIDENCE: ~{_safe_float(result.get('confidence')):.0f}%\n")
            f.write(f"MARKET REGIME: {result.get('market_regime', 'UNKNOWN')}\n\n")
            f.write("SCORES:\n")
            f.write(f"  Bullish:  {_safe_float(result.get('bullish_score')):.1f}\n")
            f.write(f"  Bearish:  {_safe_float(result.get('bearish_score')):.1f}\n")
            f.write(f"  Volatile: {_safe_float(result.get('volatile_score')):.1f}\n\n")
            f.write(f"SIGNALS ({len(result.get('signals', []))}):\n")
            for name, direction, weight, detail in result.get("signals", []):
                f.write(f"  [{str(direction):10s}] {str(name):30s} wt:{_safe_float(weight):5.1f} | {detail}\n")
            f.write("\nDECISION TRACE:\n")
            for item in str(result.get("decision_trace", "")).split(" | "):
                if item.strip():
                    f.write(f"  - {item}\n")
            f.write("\nDISCLAIMER: For research & education only. Not trading advice.\n")
        if verbose:
            print(f"\n💾 Report saved to: {filename}")

    return result


if __name__ == "__main__":
    generate_daily_report()
