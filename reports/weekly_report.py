"""
=============================================================
FIN ASTRO BOT v2.5 — Weekly Report Generator
=============================================================
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from reports.daily_report import generate_daily_report

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def generate_weekly_report(start_date: Optional[str] = None, symbol: str = "nifty", dataset=None, verbose: bool = True):
    """Generate projections for Monday-Friday. Prints full daily output."""
    if start_date is None:
        today = datetime.now()
        days_until_monday = (7 - today.weekday()) % 7
        start = today + timedelta(days=days_until_monday)
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")

    os.makedirs(REPORT_DIR, exist_ok=True)

    if dataset is None:
        try:
            from analysis.correlator import get_or_build_dataset
            dataset, _ = get_or_build_dataset(symbol)
        except Exception as e:
            dataset = None
            if verbose:
                print(f"⚠️ Dataset unavailable for weekly historical context: {e}")

    print(f"\n📅 WEEKLY REPORT — Week of {start.strftime('%Y-%m-%d')}")
    print("=" * 60)

    week_results = []
    for i in range(5):
        day = start + timedelta(days=i)
        if day.weekday() >= 5:
            continue
        date_str = day.strftime("%Y-%m-%d")
        day_name = day.strftime("%A")
        print(f"\n\n{'#'*60}")
        print(f"# {day_name} — {date_str}")
        print(f"{'#'*60}")
        result = generate_daily_report(date_str, symbol, dataset, save=True, verbose=True)
        result["day_name"] = day_name
        week_results.append(result)

    print(f"\n\n{'='*60}")
    print(f"📊 WEEKLY SUMMARY — {symbol.upper()}")
    print(f"{'='*60}")
    print(f"{'Day':12s} {'Projection':28s} {'Bias':14s} {'Conf':>6s} {'Regime':>10s}")
    print("─" * 80)
    for r in week_results:
        print(f"{r.get('day_name',''):12s} {str(r.get('gap_projection',''))[:28]:28s} "
              f"{str(r.get('bias',''))[:14]:14s} {_fmt_conf(r.get('confidence')):>6s} {str(r.get('market_regime','')):>10s}")

    total_bull = sum(_safe_float(r.get("bullish_score")) for r in week_results)
    total_bear = sum(_safe_float(r.get("bearish_score")) for r in week_results)
    print(f"\n  Week Bullish Total:  {total_bull:.1f}")
    print(f"  Week Bearish Total:  {total_bear:.1f}")
    print(f"  Week Bias: {'BULLISH' if total_bull > total_bear * 1.15 else ('BEARISH' if total_bear > total_bull * 1.15 else 'MIXED')}")

    safe_sym = symbol.replace(" ", "_").replace("^", "")
    filename = os.path.join(REPORT_DIR, f"weekly_{safe_sym}_{start.strftime('%Y-%m-%d')}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("FIN ASTRO BOT v2.5 — WEEKLY REPORT\n")
        f.write(f"Week of: {start.strftime('%Y-%m-%d')}\n")
        f.write(f"Symbol: {symbol}\n\n")
        for r in week_results:
            f.write(f"{r.get('day_name',''):12s} {str(r.get('gap_projection','')):28s} "
                    f"{str(r.get('bias','')):14s} {_fmt_conf(r.get('confidence')):>6s} {str(r.get('market_regime','')):>10s}\n")
        f.write(f"\nBullish Total: {total_bull:.1f}\n")
        f.write(f"Bearish Total: {total_bear:.1f}\n")
    print(f"\n💾 Weekly report saved to: {filename}")
    return week_results


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _fmt_conf(value) -> str:
    return f"{_safe_float(value):.0f}%"


if __name__ == "__main__":
    generate_weekly_report()
