"""
=============================================================
FIN ASTRO BOT v2.0 — Advanced Gap Analyzer
=============================================================
"""

import pandas as pd
import numpy as np
from market.data_fetcher import get_market_data_with_gaps, get_gap_statistics


def analyze_gap_patterns(data, display_name=''):
    """Detailed gap pattern analysis."""
    if data.empty:
        return {}

    results = {}

    # Day-of-week gap patterns
    data_copy = data.copy()
    data_copy['Weekday'] = data_copy.index.day_name()

    print(f"\n📅 GAP BY DAY OF WEEK{' — ' + display_name if display_name else ''}:")
    print(f"{'Day':12s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s} {'Avg Range%':>11s}")
    print("-" * 52)

    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        subset = data_copy[data_copy['Weekday'] == day]
        if len(subset) > 5:
            avg_gap = subset['Gap_Pct'].mean()
            bullish = (subset['Day_Direction'] == 'Bullish').mean() * 100
            avg_range = subset['Intraday_Range'].mean()
            print(f"  {day:10s} {len(subset):5d}  {avg_gap:+8.4f}  {bullish:8.1f}  {avg_range:10.3f}")

            results[day] = {
                'count': len(subset),
                'avg_gap': round(avg_gap, 4),
                'bullish_pct': round(bullish, 1),
                'avg_range': round(avg_range, 3),
            }

    # Monthly patterns
    data_copy['Month'] = data_copy.index.month
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    print(f"\n📆 GAP BY MONTH:")
    print(f"{'Month':6s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s}")
    print("-" * 35)

    for m in range(1, 13):
        subset = data_copy[data_copy['Month'] == m]
        if len(subset) > 5:
            avg_gap = subset['Gap_Pct'].mean()
            bullish = (subset['Day_Direction'] == 'Bullish').mean() * 100
            print(f"  {month_names[m-1]:4s} {len(subset):5d}  {avg_gap:+8.4f}  {bullish:8.1f}")

    return results


def find_extreme_gaps(data, top_n=10, display_name=''):
    """Find the most extreme gap days."""
    if data.empty or 'Gap_Pct' not in data.columns:
        return

    print(f"\n🔺 TOP {top_n} LARGEST GAP UPS{' — ' + display_name if display_name else ''}:")
    top_up = data.nlargest(top_n, 'Gap_Pct')[['Open', 'Close', 'Gap_Pct', 'Day_Direction']]
    print(top_up.to_string())

    print(f"\n🔻 TOP {top_n} LARGEST GAP DOWNS:")
    top_down = data.nsmallest(top_n, 'Gap_Pct')[['Open', 'Close', 'Gap_Pct', 'Day_Direction']]
    print(top_down.to_string())


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    data, name = get_market_data_with_gaps('nifty', start='2020-01-01')
    if not data.empty:
        get_gap_statistics(data, name)
        analyze_gap_patterns(data, name)
        find_extreme_gaps(data, top_n=5, display_name=name)