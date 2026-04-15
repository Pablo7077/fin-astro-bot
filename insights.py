"""
=============================================================
FIN ASTRO BOT — Insight & Correlation Engine
=============================================================
Merges planetary data with market data to find patterns,
compute hit rates, and generate actionable insights.
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from astro_engine import full_astro_analysis, get_planetary_positions
from market_data import get_nifty_data

import warnings
warnings.filterwarnings('ignore')


def build_astro_market_dataset(start_date='2015-01-01', end_date=None):
    """
    Build a merged dataset: each trading day gets planetary data + market data.
    This is the CORE dataset for all correlations.
    """
    print("🔮 Building Astro-Market Dataset...")
    print("   (This takes a few minutes — calculating planets for each trading day)\n")

    # Get market data
    market = get_nifty_data(start=start_date, end=end_date)
    if market.empty:
        return pd.DataFrame()

    # For each trading day, calculate key astro features
    astro_records = []
    total = len(market)

    for idx, (date, row) in enumerate(market.iterrows()):
        date_str = date.strftime('%Y-%m-%d')

        if (idx + 1) % 100 == 0:
            print(f"   Processing {idx + 1}/{total}...")

        try:
            pos = get_planetary_positions(date_str)

            record = {
                'Date': date,
                # Moon data (fast-moving, most impact on daily)
                'Moon_Sign': pos['Moon']['sign'],
                'Moon_Nakshatra': pos['Moon']['nakshatra'],
                'Moon_Degree': pos['Moon']['longitude'],

                # Key planet signs
                'Mercury_Sign': pos['Mercury']['sign'],
                'Venus_Sign': pos['Venus']['sign'],
                'Mars_Sign': pos['Mars']['sign'],
                'Jupiter_Sign': pos['Jupiter']['sign'],
                'Saturn_Sign': pos['Saturn']['sign'],

                # Retrogrades
                'Mercury_Retro': pos['Mercury']['retrograde'],
                'Venus_Retro': pos['Venus']['retrograde'],
                'Mars_Retro': pos['Mars']['retrograde'],
                'Jupiter_Retro': pos['Jupiter']['retrograde'],
                'Saturn_Retro': pos['Saturn']['retrograde'],

                # Retrograde count
                'Retro_Count': sum(1 for p in ['Mercury', 'Venus', 'Mars',
                                                'Jupiter', 'Saturn']
                                   if pos[p]['retrograde']),

                # Rahu-Ketu axis
                'Rahu_Sign': pos['Rahu']['sign'],
                'Ketu_Sign': pos['Ketu']['sign'],

                # Sun-Moon distance (for tithi/phase)
                'Sun_Moon_Dist': (pos['Moon']['longitude'] -
                                  pos['Sun']['longitude']) % 360,
            }
            astro_records.append(record)

        except Exception as e:
            # Skip dates with calculation errors
            continue

    astro_df = pd.DataFrame(astro_records)
    astro_df.set_index('Date', inplace=True)

    # Merge
    merged = market.join(astro_df, how='inner')
    print(f"\n✅ Dataset built: {len(merged)} trading days with astro data.")

    return merged


def analyze_moon_sign_gaps(dataset):
    """Analyze gap patterns by Moon sign."""
    print("\n🌙 GAP PATTERNS BY MOON SIGN")
    print("=" * 65)

    results = []
    for sign in dataset['Moon_Sign'].dropna().unique():
        mask = dataset['Moon_Sign'] == sign
        subset = dataset[mask]
        if len(subset) < 10:
            continue

        avg_gap = subset['Gap_Pct'].mean()
        gap_up_rate = (subset['Gap_Pct'] > 0.1).mean() * 100
        gap_down_rate = (subset['Gap_Pct'] < -0.1).mean() * 100
        bullish_rate = (subset['Day_Direction'] == 'Bullish').mean() * 100
        count = len(subset)

        results.append({
            'Moon_Sign': sign,
            'Count': count,
            'Avg_Gap%': round(avg_gap, 3),
            'Gap_Up%': round(gap_up_rate, 1),
            'Gap_Down%': round(gap_down_rate, 1),
            'Bullish_Day%': round(bullish_rate, 1),
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Avg_Gap%', ascending=False)
    print(results_df.to_string(index=False))

    return results_df


def analyze_moon_nakshatra_gaps(dataset):
    """Analyze gap patterns by Moon nakshatra."""
    print("\n⭐ GAP PATTERNS BY MOON NAKSHATRA (Top 10 Bullish & Bearish)")
    print("=" * 65)

    results = []
    for nak in dataset['Moon_Nakshatra'].dropna().unique():
        mask = dataset['Moon_Nakshatra'] == nak
        subset = dataset[mask]
        if len(subset) < 5:
            continue

        avg_gap = subset['Gap_Pct'].mean()
        bullish_rate = (subset['Day_Direction'] == 'Bullish').mean() * 100
        count = len(subset)

        results.append({
            'Nakshatra': nak,
            'Count': count,
            'Avg_Gap%': round(avg_gap, 3),
            'Bullish%': round(bullish_rate, 1),
        })

    results_df = pd.DataFrame(results).sort_values('Avg_Gap%', ascending=False)

    print("\n📈 TOP 10 BULLISH NAKSHATRAS:")
    print(results_df.head(10).to_string(index=False))
    print("\n📉 TOP 10 BEARISH NAKSHATRAS:")
    print(results_df.tail(10).to_string(index=False))

    return results_df


def analyze_retrograde_impact(dataset):
    """Analyze market behavior during retrogrades."""
    print("\n🔄 RETROGRADE IMPACT ANALYSIS")
    print("=" * 65)

    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        col = f'{planet}_Retro'
        if col not in dataset.columns:
            continue

        retro = dataset[dataset[col] == True]
        direct = dataset[dataset[col] == False]

        if len(retro) < 5 or len(direct) < 5:
            continue

        print(f"\n  {planet}:")
        print(f"    Retrograde days: {len(retro)}, Direct days: {len(direct)}")
        print(f"    Avg Gap (Retro):  {retro['Gap_Pct'].mean():.4f}%")
        print(f"    Avg Gap (Direct): {direct['Gap_Pct'].mean():.4f}%")
        print(f"    Bullish% (Retro):  {(retro['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
        print(f"    Bullish% (Direct): {(direct['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
        print(f"    Volatility (Retro):  {retro['Intraday_Range'].mean():.3f}%")
        print(f"    Volatility (Direct): {direct['Intraday_Range'].mean():.3f}%")


def analyze_retro_count_impact(dataset):
    """Analyze market by number of simultaneous retrogrades."""
    print("\n🔄 IMPACT BY NUMBER OF SIMULTANEOUS RETROGRADES")
    print("=" * 65)

    for count in sorted(dataset['Retro_Count'].unique()):
        subset = dataset[dataset['Retro_Count'] == count]
        if len(subset) < 10:
            continue
        print(f"  {int(count)} planets retrograde: "
              f"{len(subset)} days, "
              f"Avg Gap: {subset['Gap_Pct'].mean():.4f}%, "
              f"Bullish: {(subset['Day_Direction'] == 'Bullish').mean() * 100:.1f}%, "
              f"Avg Range: {subset['Intraday_Range'].mean():.3f}%")


def generate_today_projection(dataset, target_date=None):
    """
    Generate gap projection and bias for a specific date
    based on historical pattern matching.
    """
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\n{'='*65}")
    print(f"🎯 ASTRO GAP PROJECTION FOR {target_date}")
    print(f"{'='*65}")

    # Get today's astro data
    analysis = full_astro_analysis(target_date)
    pos = analysis['positions']

    moon_sign = pos['Moon']['sign']
    moon_nak = pos['Moon']['nakshatra']
    mercury_retro = pos['Mercury']['retrograde']
    retro_count = sum(1 for p in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                      if pos[p]['retrograde'])

    # ── Print current astro snapshot ──
    print(f"\n📍 Key Positions:")
    for name in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu']:
        p = pos[name]
        r = ' ℞' if p['retrograde'] and name not in ['Rahu'] else ''
        print(f"   {name:10s}: {p['sign']:13s} {p['sign_degree']:6.2f}° "
              f"({p['nakshatra']} P{p['pada']}){r}")
    print(f"   {'Ketu':10s}: {pos['Ketu']['sign']:13s} "
          f"{pos['Ketu']['sign_degree']:6.2f}°")

    # Moon phase
    mp = analysis['moon_phase']
    print(f"\n🌙 Moon Phase: {mp['phase']}")
    print(f"   Tithi: {mp['paksha']} {mp['tithi_name']}")
    print(f"   Market Note: {mp['market_note']}")

    # Yogas
    if analysis['yogas']:
        print(f"\n⭐ Active Yogas:")
        for y in analysis['yogas']:
            print(f"   {y['name']}: {y['effect']} [{y['market_bias'].upper()}]")

    # Combustions
    if analysis['combustions']:
        print(f"\n🔥 Combustions:")
        for c in analysis['combustions']:
            print(f"   {c['planet']} ({c['severity']}, {c['distance_from_sun']}° from Sun)")

    # Ingresses
    if analysis['ingresses']:
        print(f"\n🚀 Sign Changes:")
        for ing in analysis['ingresses']:
            print(f"   {ing['event']}")

    # ── Historical Pattern Matching ──
    print(f"\n📊 HISTORICAL PATTERN MATCHING:")
    print("-" * 50)

    signals = []  # (signal_name, direction, confidence)

    # 1. Moon Sign pattern
    if 'Moon_Sign' in dataset.columns:
        moon_data = dataset[dataset['Moon_Sign'] == moon_sign]
        if len(moon_data) >= 10:
            avg_gap = moon_data['Gap_Pct'].mean()
            bullish_pct = (moon_data['Day_Direction'] == 'Bullish').mean() * 100
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(bullish_pct - 50) * 2, 30)  # Max 30% confidence from this
            signals.append(('Moon Sign', direction, conf))
            print(f"  Moon in {moon_sign}: {len(moon_data)} historical days, "
                  f"Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}% → {direction}")

    # 2. Moon Nakshatra pattern
    if 'Moon_Nakshatra' in dataset.columns:
        nak_data = dataset[dataset['Moon_Nakshatra'] == moon_nak]
        if len(nak_data) >= 5:
            avg_gap = nak_data['Gap_Pct'].mean()
            bullish_pct = (nak_data['Day_Direction'] == 'Bullish').mean() * 100
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(bullish_pct - 50) * 2, 25)
            signals.append(('Moon Nakshatra', direction, conf))
            print(f"  Moon in {moon_nak}: {len(nak_data)} historical days, "
                  f"Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}% → {direction}")

    # 3. Mercury Retrograde
    if mercury_retro and 'Mercury_Retro' in dataset.columns:
        retro_data = dataset[dataset['Mercury_Retro'] == True]
        if len(retro_data) >= 10:
            avg_gap = retro_data['Gap_Pct'].mean()
            bullish_pct = (retro_data['Day_Direction'] == 'Bullish').mean() * 100
            vol = retro_data['Intraday_Range'].mean()
            direction = 'VOLATILE'
            conf = 10
            signals.append(('Mercury Retro', direction, conf))
            print(f"  Mercury Retrograde: Avg Gap: {avg_gap:+.3f}%, "
                  f"Bullish: {bullish_pct:.1f}%, Avg Range: {vol:.2f}% → VOLATILE")

    # 4. Retrograde count
    if 'Retro_Count' in dataset.columns:
        rc_data = dataset[dataset['Retro_Count'] == retro_count]
        if len(rc_data) >= 10:
            avg_gap = rc_data['Gap_Pct'].mean()
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(avg_gap) * 100, 15)
            signals.append(('Retro Count', direction, conf))
            print(f"  {retro_count} Retrogrades active: {len(rc_data)} days, "
                  f"Avg Gap: {avg_gap:+.3f}% → {direction}")

    # 5. Yoga-based signals
    for yoga in analysis['yogas']:
        bias = yoga['market_bias']
        if 'bullish' in bias:
            signals.append(('Yoga: ' + yoga['name'], 'BULLISH', 15))
        elif 'bearish' in bias:
            signals.append(('Yoga: ' + yoga['name'], 'BEARISH', 15))
        else:
            signals.append(('Yoga: ' + yoga['name'], 'VOLATILE', 10))

    # 6. Moon phase signal
    moon_phase_text = mp['phase']
    if 'New Moon' in moon_phase_text:
        signals.append(('Moon Phase', 'VOLATILE', 10))
    elif 'Full Moon' in moon_phase_text:
        signals.append(('Moon Phase', 'VOLATILE', 10))
    elif 'Waxing' in moon_phase_text:
        signals.append(('Moon Phase', 'BULLISH', 8))
    elif 'Waning' in moon_phase_text:
        signals.append(('Moon Phase', 'BEARISH', 8))

    # ── Aggregate Signals ──
    print(f"\n{'='*50}")
    print("🎯 SIGNAL AGGREGATION:")
    print("-" * 50)

    bullish_score = sum(c for _, d, c in signals if d == 'BULLISH')
    bearish_score = sum(c for _, d, c in signals if d == 'BEARISH')
    volatile_score = sum(c for _, d, c in signals if d == 'VOLATILE')

    for name, direction, conf in signals:
        emoji = '🟢' if direction == 'BULLISH' else ('🔴' if direction == 'BEARISH' else '🟡')
        print(f"  {emoji} {name:25s} → {direction:10s} (weight: {conf})")

    total_directional = bullish_score + bearish_score
    if total_directional > 0:
        bull_pct = (bullish_score / (total_directional + volatile_score)) * 100
        bear_pct = (bearish_score / (total_directional + volatile_score)) * 100
    else:
        bull_pct = bear_pct = 0

    print(f"\n  Bullish Score:  {bullish_score} ({bull_pct:.0f}%)")
    print(f"  Bearish Score:  {bearish_score} ({bear_pct:.0f}%)")
    print(f"  Volatile Score: {volatile_score}")

    # Final Projection
    print(f"\n{'='*50}")
    if bullish_score > bearish_score * 1.3 and bullish_score > volatile_score:
        gap_proj = "GAP UP"
        direction_bias = "BULLISH"
        confidence = min(bull_pct, 70)
    elif bearish_score > bullish_score * 1.3 and bearish_score > volatile_score:
        gap_proj = "GAP DOWN"
        direction_bias = "BEARISH"
        confidence = min(bear_pct, 70)
    elif volatile_score > bullish_score and volatile_score > bearish_score:
        gap_proj = "FLAT/VOLATILE"
        direction_bias = "SIDEWAYS WITH WHIPSAWS"
        confidence = 40
    else:
        gap_proj = "FLAT/UNCERTAIN"
        direction_bias = "MIXED — NO CLEAR EDGE"
        confidence = 30

    print(f"  📊 ASTRO GAP PROJECTION:  {gap_proj}")
    print(f"  📈 DAY DIRECTION BIAS:    {direction_bias}")
    print(f"  🎯 CONFIDENCE:            ~{confidence:.0f}%")
    print(f"{'='*50}")

    # Cautions
    print(f"\n⚠️  CAUTIONS:")
    print(f"  • Astro signals are PROBABILISTIC, not deterministic.")
    print(f"  • Always combine with price action / technical analysis.")
    print(f"  • This is for RESEARCH & EDUCATION only.")
    print(f"  • Never risk capital solely on astrological signals.")

    return {
        'date': target_date,
        'gap_projection': gap_proj,
        'direction_bias': direction_bias,
        'confidence': confidence,
        'signals': signals,
        'analysis': analysis,
    }


# ── Quick Test ────────────────────────────────────────────
if __name__ == '__main__':
    # Build dataset (this takes a while first time)
    dataset = build_astro_market_dataset(start_date='2020-01-01')

    if not dataset.empty:
        # Run analyses
        analyze_moon_sign_gaps(dataset)
        analyze_moon_nakshatra_gaps(dataset)
        analyze_retrograde_impact(dataset)
        analyze_retro_count_impact(dataset)

        # Generate today's projection
        today = datetime.now().strftime('%Y-%m-%d')
        generate_today_projection(dataset, target_date=today)