"""
=============================================================
FIN ASTRO BOT v2.0 — Bradley Siderograph
=============================================================
A composite indicator summing declination-based aspects.
Its TURNING POINTS (peaks/troughs) correlate with market reversals.
NOTE: Direction is NOT the signal — the CHANGE in direction is.
=============================================================
"""

import swisseph as swe
from core.astro_engine import date_to_jd, PLANETS
from datetime import datetime, timedelta
import os

EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)

# Aspect weights for Bradley calculation
ASPECT_WEIGHTS = {
    0: 10,     # Conjunction
    60: 4,     # Sextile
    90: -6,    # Square
    120: 6,    # Trine
    180: -8,   # Opposition
}

# Planet pairs to consider (major planets only)
BRADLEY_PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
}

# Declination weights
DECL_WEIGHTS = {
    ('Sun', 'Moon'): 5,
    ('Sun', 'Mercury'): 2,
    ('Sun', 'Venus'): 3,
    ('Sun', 'Mars'): 3,
    ('Sun', 'Jupiter'): 4,
    ('Sun', 'Saturn'): 4,
    ('Moon', 'Jupiter'): 3,
    ('Moon', 'Saturn'): 3,
    ('Jupiter', 'Saturn'): 5,
    ('Mars', 'Jupiter'): 3,
    ('Mars', 'Saturn'): 4,
    ('Venus', 'Jupiter'): 3,
}


def calculate_bradley_value(date_str):
    """
    Calculate Bradley Siderograph value for a single date.
    Uses geocentric declinations and longitude aspects.
    """
    jd = date_to_jd(date_str, '12:00')
    value = 0

    # Get all planet positions and declinations
    planet_data = {}
    for name, pid in BRADLEY_PLANETS.items():
        result = swe.calc_ut(jd, pid, swe.FLG_SPEED)
        planet_data[name] = {
            'longitude': result[0][0] % 360,
            'declination': result[0][1],
        }

    # Calculate aspect-based component
    planet_names = list(BRADLEY_PLANETS.keys())
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]

            long1 = planet_data[p1]['longitude']
            long2 = planet_data[p2]['longitude']

            diff = abs(long1 - long2) % 360
            if diff > 180:
                diff = 360 - diff

            # Check each aspect
            for aspect_deg, weight in ASPECT_WEIGHTS.items():
                orb = 8 if aspect_deg in [0, 180] else 6
                if abs(diff - aspect_deg) <= orb:
                    # Weight by closeness to exact
                    closeness = 1 - (abs(diff - aspect_deg) / orb)

                    # Get pair weight
                    pair = tuple(sorted([p1, p2]))
                    pair_weight = DECL_WEIGHTS.get(pair, DECL_WEIGHTS.get((pair[1], pair[0]), 1))

                    value += weight * closeness * pair_weight * 0.1

    # Add declination parallel/contra-parallel component
    for pair, weight in DECL_WEIGHTS.items():
        if pair[0] in planet_data and pair[1] in planet_data:
            decl1 = planet_data[pair[0]]['declination']
            decl2 = planet_data[pair[1]]['declination']

            # Parallel (same declination) = conjunction-like
            if abs(decl1 - decl2) <= 1.5:
                value += weight * 0.5

            # Contra-parallel (opposite declination) = opposition-like
            if abs(decl1 + decl2) <= 1.5:
                value -= weight * 0.3

    return round(value, 2)


def calculate_bradley_series(start_date, end_date=None, days=90):
    """
    Calculate Bradley Siderograph for a date range.
    Returns list of (date, value) for charting.
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end = start + timedelta(days=days)

    series = []
    current = start
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        try:
            value = calculate_bradley_value(date_str)
            series.append({'date': date_str, 'value': value})
        except Exception:
            pass
        current += timedelta(days=1)

    return series


def find_turning_points(series, window=5):
    """
    Find peaks and troughs in Bradley series.
    THESE are the market reversal signals (not the direction).
    """
    if len(series) < window * 2 + 1:
        return []

    turning_points = []
    values = [s['value'] for s in series]

    for i in range(window, len(values) - window):
        # Check if local maximum
        if all(values[i] >= values[i - j] for j in range(1, window + 1)) and \
           all(values[i] >= values[i + j] for j in range(1, window + 1)):
            turning_points.append({
                'date': series[i]['date'],
                'value': series[i]['value'],
                'type': 'PEAK',
                'market_signal': 'Potential market HIGH — watch for reversal DOWN',
            })

        # Check if local minimum
        elif all(values[i] <= values[i - j] for j in range(1, window + 1)) and \
             all(values[i] <= values[i + j] for j in range(1, window + 1)):
            turning_points.append({
                'date': series[i]['date'],
                'value': series[i]['value'],
                'type': 'TROUGH',
                'market_signal': 'Potential market LOW — watch for reversal UP',
            })

    return turning_points


def get_bradley_analysis(date_str, lookahead=30, lookbehind=30):
    """Complete Bradley analysis: current value + nearby turning points."""
    start = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=lookbehind)).strftime('%Y-%m-%d')
    end = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=lookahead)).strftime('%Y-%m-%d')

    series = calculate_bradley_series(start, end)
    current_value = calculate_bradley_value(date_str)
    turning_points = find_turning_points(series)

    # Find nearest turning points
    target_dt = datetime.strptime(date_str, '%Y-%m-%d')
    upcoming = [tp for tp in turning_points
                if datetime.strptime(tp['date'], '%Y-%m-%d') >= target_dt]
    recent = [tp for tp in turning_points
              if datetime.strptime(tp['date'], '%Y-%m-%d') < target_dt]

    return {
        'date': date_str,
        'current_value': current_value,
        'trend': 'RISING' if len(series) >= 2 and series[-1]['value'] > series[-2]['value'] else 'FALLING',
        'upcoming_turning_points': upcoming[:3],
        'recent_turning_points': recent[-3:],
        'series': series,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📈 BRADLEY SIDEROGRAPH — {today}")
    print("=" * 60)

    analysis = get_bradley_analysis(today)

    print(f"\n📊 Current Value: {analysis['current_value']}")
    print(f"📈 Trend: {analysis['trend']}")

    if analysis['upcoming_turning_points']:
        print(f"\n🔮 UPCOMING TURNING POINTS:")
        for tp in analysis['upcoming_turning_points']:
            emoji = '🔺' if tp['type'] == 'PEAK' else '🔻'
            print(f"  {emoji} {tp['date']}: {tp['type']} (value: {tp['value']})")
            print(f"     {tp['market_signal']}")

    if analysis['recent_turning_points']:
        print(f"\n📅 RECENT TURNING POINTS:")
        for tp in analysis['recent_turning_points']:
            emoji = '🔺' if tp['type'] == 'PEAK' else '🔻'
            print(f"  {emoji} {tp['date']}: {tp['type']} (value: {tp['value']})")