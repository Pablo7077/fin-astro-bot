"""
=============================================================
FIN ASTRO BOT v2.0 — Weekly Report Generator
=============================================================
Loops through upcoming week, generates batch projections.
=============================================================
"""

import os
from datetime import datetime, timedelta
from reports.daily_report import generate_daily_report

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def generate_weekly_report(start_date=None, symbol='nifty', dataset=None):
    """Generate projections for the entire upcoming week."""
    if start_date is None:
        today = datetime.now()
        # Find next Monday
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 0  # If today is Monday, use today
        start = today + timedelta(days=days_until_monday)
    else:
        start = datetime.strptime(start_date, '%Y-%m-%d')

    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"\n📅 WEEKLY REPORT — Week of {start.strftime('%Y-%m-%d')}")
    print(f"{'='*60}")

    week_results = []

    # Monday to Friday
    for i in range(5):
        day = start + timedelta(days=i)
        if day.weekday() >= 5:  # Skip weekends
            continue

        date_str = day.strftime('%Y-%m-%d')
        day_name = day.strftime('%A')

        print(f"\n\n{'#'*60}")
        print(f"# {day_name} — {date_str}")
        print(f"{'#'*60}")

        result = generate_daily_report(date_str, symbol, dataset, save=True)
        result['day_name'] = day_name
        week_results.append(result)

    # Weekly Summary
    print(f"\n\n{'='*60}")
    print(f"📊 WEEKLY SUMMARY — {symbol.upper()}")
    print(f"{'='*60}")
    print(f"{'Day':12s} {'Projection':25s} {'Bias':20s} {'Conf':>5s}")
    print(f"{'─'*65}")

    for r in week_results:
        print(f"{r.get('day_name', ''):12s} {r['gap_projection']:25s} "
              f"{r['bias']:20s} {r['confidence']:4.0f}%")

    total_bull = sum(r['bullish_score'] for r in week_results)
    total_bear = sum(r['bearish_score'] for r in week_results)

    print(f"\n  Week Bullish Total:  {total_bull}")
    print(f"  Week Bearish Total:  {total_bear}")
    print(f"  Week Bias: {'BULLISH' if total_bull > total_bear * 1.2 else ('BEARISH' if total_bear > total_bull * 1.2 else 'MIXED')}")

    # Save weekly summary
    safe_sym = symbol.replace(' ', '_').replace('^', '')
    filename = os.path.join(REPORT_DIR, f'weekly_{safe_sym}_{start.strftime("%Y-%m-%d")}.txt')
    with open(filename, 'w') as f:
        f.write(f"FIN ASTRO BOT — WEEKLY REPORT\n")
        f.write(f"Week of: {start.strftime('%Y-%m-%d')}\n")
        f.write(f"Symbol: {symbol}\n\n")
        for r in week_results:
            f.write(f"{r.get('day_name', ''):12s} {r['gap_projection']:25s} "
                    f"{r['bias']:20s} {r['confidence']:4.0f}%\n")
        f.write(f"\nBullish Total: {total_bull}\n")
        f.write(f"Bearish Total: {total_bear}\n")

    print(f"\n💾 Weekly report saved to: {filename}")

    return week_results


if __name__ == '__main__':
    generate_weekly_report()