"""
=============================================================
FIN ASTRO BOT v2.0 — Daily Report Generator
=============================================================
"""

import os
from datetime import datetime
from analysis.projector import generate_full_projection


REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def generate_daily_report(date_str=None, symbol='nifty', dataset=None, save=True):
    """Generate and optionally save daily report."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    os.makedirs(REPORT_DIR, exist_ok=True)

    result = generate_full_projection(date_str, symbol, dataset)

    if save:
        safe_sym = symbol.replace(' ', '_').replace('^', '')
        filename = os.path.join(REPORT_DIR, f'daily_{safe_sym}_{date_str}.txt')

        with open(filename, 'w') as f:
            f.write(f"FIN ASTRO BOT v2.0 — DAILY REPORT\n")
            f.write(f"Date: {date_str} | Symbol: {symbol}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"GAP PROJECTION: {result['gap_projection']}\n")
            f.write(f"DAY BIAS: {result['bias']}\n")
            f.write(f"CONFIDENCE: ~{result['confidence']:.0f}%\n\n")
            f.write(f"SCORES:\n")
            f.write(f"  Bullish:  {result['bullish_score']}\n")
            f.write(f"  Bearish:  {result['bearish_score']}\n")
            f.write(f"  Volatile: {result['volatile_score']}\n\n")
            f.write(f"SIGNALS ({len(result['signals'])}):\n")
            for name, direction, weight, detail in result['signals']:
                f.write(f"  [{direction:10s}] {name:30s} wt:{weight:3d} | {detail}\n")
            f.write(f"\nDISCLAIMER: For research & education only.\n")

        print(f"\n💾 Report saved to: {filename}")

    return result


if __name__ == '__main__':
    generate_daily_report()