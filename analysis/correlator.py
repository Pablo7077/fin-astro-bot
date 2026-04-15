"""
=============================================================
FIN ASTRO BOT v2.0 — Astro-Market Correlator
=============================================================
Merges planetary data with market data for any symbol.
Creates the master dataset for correlation analysis.
=============================================================
"""

import pandas as pd
import pickle
import os
from datetime import datetime
from core.astro_engine import get_planetary_positions
from core.panchang import get_full_panchang
from market.data_fetcher import get_market_data_with_gaps

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')


def build_astro_market_dataset(user_input='nifty', start_date='2015-01-01', end_date=None):
    """
    Build merged astro + market dataset for ANY symbol.
    Calculates planetary positions for each trading day.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    print(f"🔮 Building Astro-Market Dataset for '{user_input}'...")
    print("   (Calculating planets for each trading day — takes a few minutes)\n")

    # Fetch market data
    market, display_name = get_market_data_with_gaps(user_input, start=start_date, end=end_date)
    if market.empty:
        return pd.DataFrame(), display_name

    # Calculate astro for each trading day
    astro_records = []
    total = len(market)

    for idx, (date, row) in enumerate(market.iterrows()):
        date_str = date.strftime('%Y-%m-%d')

        if (idx + 1) % 100 == 0 or idx == 0:
            print(f"   Processing {idx + 1}/{total} ({date_str})...")

        try:
            pos = get_planetary_positions(date_str)
            panchang = get_full_panchang(date_str, pos)

            record = {
                'Date': date,
                # Moon (fast-moving, daily impact)
                'Moon_Sign': pos['Moon']['sign'],
                'Moon_Nakshatra': pos['Moon']['nakshatra'],
                'Moon_Degree': pos['Moon']['longitude'],
                'Moon_Dignity': pos['Moon']['dignity'],

                # Key planet signs
                'Sun_Sign': pos['Sun']['sign'],
                'Mercury_Sign': pos['Mercury']['sign'],
                'Venus_Sign': pos['Venus']['sign'],
                'Mars_Sign': pos['Mars']['sign'],
                'Jupiter_Sign': pos['Jupiter']['sign'],
                'Saturn_Sign': pos['Saturn']['sign'],
                'Rahu_Sign': pos['Rahu']['sign'],

                # Retrogrades
                'Mercury_Retro': pos['Mercury']['retrograde'],
                'Venus_Retro': pos['Venus']['retrograde'],
                'Mars_Retro': pos['Mars']['retrograde'],
                'Jupiter_Retro': pos['Jupiter']['retrograde'],
                'Saturn_Retro': pos['Saturn']['retrograde'],

                'Retro_Count': sum(1 for p in ['Mercury', 'Venus', 'Mars',
                                                'Jupiter', 'Saturn']
                                   if pos[p]['retrograde']),

                # Dignities
                'Jupiter_Dignity': pos['Jupiter']['dignity'],
                'Saturn_Dignity': pos['Saturn']['dignity'],
                'Venus_Dignity': pos['Venus']['dignity'],

                # Panchang
                'Tithi': panchang['tithi']['name'],
                'Tithi_Num': panchang['tithi']['number'],
                'Paksha': panchang['tithi']['paksha'],
                'Karana': panchang['karana']['name'],
                'Karana_Vishti': panchang['karana']['is_vishti'],
                'Nitya_Yoga': panchang['nitya_yoga']['name'],
                'Nitya_Yoga_Bad': panchang['nitya_yoga']['is_inauspicious'],
                'Weekday': panchang['vara']['name'],

                # Sun-Moon distance (phase)
                'Sun_Moon_Dist': (pos['Moon']['longitude'] - pos['Sun']['longitude']) % 360,
            }
            astro_records.append(record)

        except Exception:
            continue

    if not astro_records:
        print("❌ Could not calculate astro data.")
        return pd.DataFrame(), display_name

    astro_df = pd.DataFrame(astro_records)
    astro_df.set_index('Date', inplace=True)

    # Merge
    merged = market.join(astro_df, how='inner')
    print(f"\n✅ Dataset built: {len(merged)} trading days with astro data for {display_name}.")

    # Cache it
    safe_name = display_name.replace(' ', '_').replace('/', '_').replace('^', '')
    cache_file = os.path.join(CACHE_DIR, f'dataset_{safe_name}.pkl')
    with open(cache_file, 'wb') as f:
        pickle.dump({'data': merged, 'name': display_name}, f)
    print(f"💾 Cached to {cache_file}")

    return merged, display_name


def load_cached_dataset(user_input):
    """Load previously built dataset from cache."""
    from market.symbols import resolve_symbol
    symbol, display_name = resolve_symbol(user_input)

    safe_name = display_name.replace(' ', '_').replace('/', '_').replace('^', '')
    cache_file = os.path.join(CACHE_DIR, f'dataset_{safe_name}.pkl')

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cached = pickle.load(f)
        print(f"📂 Loaded cached dataset: {len(cached['data'])} days for {cached['name']}")
        return cached['data'], cached['name']

    return pd.DataFrame(), display_name


def get_or_build_dataset(user_input, start_date='2018-01-01'):
    """Load from cache or build fresh."""
    data, name = load_cached_dataset(user_input)
    if not data.empty:
        return data, name
    return build_astro_market_dataset(user_input, start_date=start_date)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    # Build for nifty (short range for testing)
    data, name = build_astro_market_dataset('nifty', start_date='2024-01-01')
    if not data.empty:
        print(f"\nColumns: {list(data.columns)}")
        print(f"\nSample:")
        print(data[['Close', 'Gap_Pct', 'Moon_Sign', 'Moon_Nakshatra',
                     'Tithi', 'Karana', 'Retro_Count']].tail(5))