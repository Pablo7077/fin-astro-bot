"""
=============================================================
FIN ASTRO BOT v2.0 — Historical Back-Tester
=============================================================
Computes hit rates for all astro factors against market data.
=============================================================
"""

import pandas as pd
import numpy as np


def analyze_factor(dataset, factor_column, target='Gap_Pct', min_samples=10):
    """Analyze a single factor's impact on market."""
    results = []

    for value in dataset[factor_column].dropna().unique():
        subset = dataset[dataset[factor_column] == value]
        if len(subset) < min_samples:
            continue

        avg_gap = subset[target].mean()
        avg_return = subset['Daily_Return'].mean() if 'Daily_Return' in subset.columns else 0
        bullish_pct = (subset['Day_Direction'] == 'Bullish').mean() * 100 if 'Day_Direction' in subset.columns else 50
        avg_range = subset['Intraday_Range'].mean() if 'Intraday_Range' in subset.columns else 0

        results.append({
            'value': value,
            'count': len(subset),
            'avg_gap_pct': round(avg_gap, 4),
            'avg_return_pct': round(avg_return, 4),
            'bullish_pct': round(bullish_pct, 1),
            'avg_range_pct': round(avg_range, 3),
        })

    return sorted(results, key=lambda x: x['avg_gap_pct'], reverse=True)


def run_full_backtest(dataset, display_name=''):
    """Run backtest on all major astro factors."""
    if dataset.empty:
        print("No data for backtesting.")
        return {}

    results = {}

    factors = [
        ('Moon_Sign', 'Moon Sign'),
        ('Moon_Nakshatra', 'Moon Nakshatra'),
        ('Tithi', 'Tithi'),
        ('Karana', 'Karana'),
        ('Nitya_Yoga', 'Nitya Yoga'),
        ('Weekday', 'Weekday'),
        ('Paksha', 'Paksha'),
        ('Jupiter_Sign', 'Jupiter Sign'),
        ('Saturn_Sign', 'Saturn Sign'),
    ]

    for col, label in factors:
        if col not in dataset.columns:
            continue

        analysis = analyze_factor(dataset, col)
        if analysis:
            results[label] = analysis

            print(f"\n📊 {label.upper()} IMPACT{' — ' + display_name if display_name else ''}:")
            print(f"{'Value':20s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s} {'Range%':>8s}")
            print("-" * 58)
            for item in analysis[:15]:
                direction = '📈' if item['avg_gap_pct'] > 0.02 else ('📉' if item['avg_gap_pct'] < -0.02 else '➡️')
                print(f"{str(item['value']):20s} {item['count']:5d}  {item['avg_gap_pct']:+8.4f}  "
                      f"{item['bullish_pct']:8.1f}  {item['avg_range_pct']:7.3f} {direction}")

    # Retrograde analysis
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        col = f'{planet}_Retro'
        if col not in dataset.columns:
            continue

        retro = dataset[dataset[col] == True]
        direct = dataset[dataset[col] == False]

        if len(retro) >= 10 and len(direct) >= 10:
            print(f"\n🔄 {planet.upper()} RETROGRADE IMPACT:")
            print(f"  Retrograde: {len(retro)} days, Avg Gap: {retro['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(retro['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Direct:     {len(direct)} days, Avg Gap: {direct['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(direct['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    # Vishti (Bhadra) Karana
    if 'Karana_Vishti' in dataset.columns:
        vishti = dataset[dataset['Karana_Vishti'] == True]
        non_vishti = dataset[dataset['Karana_Vishti'] == False]
        if len(vishti) >= 5:
            print(f"\n🚫 VISHTI (BHADRA) KARANA IMPACT:")
            print(f"  Vishti days:     {len(vishti)}, Avg Gap: {vishti['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(vishti['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Non-Vishti days: {len(non_vishti)}, Avg Gap: {non_vishti['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(non_vishti['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    # Inauspicious Nitya Yoga
    if 'Nitya_Yoga_Bad' in dataset.columns:
        bad = dataset[dataset['Nitya_Yoga_Bad'] == True]
        good = dataset[dataset['Nitya_Yoga_Bad'] == False]
        if len(bad) >= 5:
            print(f"\n⚠️ INAUSPICIOUS NITYA YOGA IMPACT:")
            print(f"  Inauspicious: {len(bad)}, Avg Gap: {bad['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(bad['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Auspicious:   {len(good)}, Avg Gap: {good['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(good['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    return results


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from analysis.correlator import get_or_build_dataset

    data, name = get_or_build_dataset('nifty', start_date='2020-01-01')
    if not data.empty:
        run_full_backtest(data, name)