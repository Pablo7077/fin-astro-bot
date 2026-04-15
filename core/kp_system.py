"""
=============================================================
FIN ASTRO BOT v2.0 — KP (Krishnamurti Paddhati) System
=============================================================
Sub-lord theory for precise prediction. Each nakshatra is
divided into 9 unequal sub-divisions based on Vimshottari.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, get_ascendant,
    NAKSHATRAS, NAKSHATRA_LORDS, NAKSHATRA_SPAN
)
from core.dasha import DASHA_YEARS, DASHA_SEQUENCE, TOTAL_DASHA_YEARS
from datetime import datetime


# ── KP Sub-Lord Table ─────────────────────────────────────

def build_kp_sublord_table():
    """
    Build the KP sub-lord table. Each nakshatra (13°20') is divided
    into 9 sub-divisions proportional to Vimshottari dasha years,
    starting from the nakshatra lord.
    """
    table = []

    for nak_idx in range(27):
        nak_lord = NAKSHATRA_LORDS[nak_idx]
        nak_start = nak_idx * NAKSHATRA_SPAN

        # Start sub-lord sequence from nakshatra lord
        start_seq_idx = DASHA_SEQUENCE.index(nak_lord)

        current_deg = nak_start
        for i in range(9):
            sub_lord_idx = (start_seq_idx + i) % 9
            sub_lord = DASHA_SEQUENCE[sub_lord_idx]

            # Sub-division span proportional to dasha years
            sub_span = NAKSHATRA_SPAN * (DASHA_YEARS[sub_lord] / TOTAL_DASHA_YEARS)
            sub_end = current_deg + sub_span

            table.append({
                'start_deg': round(current_deg, 4),
                'end_deg': round(sub_end, 4),
                'nakshatra': NAKSHATRAS[nak_idx],
                'nakshatra_lord': nak_lord,
                'sub_lord': sub_lord,
            })

            current_deg = sub_end

    return table


# Build once
KP_TABLE = build_kp_sublord_table()


def get_kp_sublord(degree):
    """Get KP sub-lord for a given sidereal degree."""
    degree = degree % 360.0
    for entry in KP_TABLE:
        if entry['start_deg'] <= degree < entry['end_deg']:
            return entry
    # Edge case: last entry
    return KP_TABLE[-1]


def get_kp_significators(positions):
    """
    Get star lord (nakshatra lord) and sub-lord for each planet.
    In KP, the sub-lord is the MOST important factor for prediction.
    """
    kp_data = {}

    for name, data in positions.items():
        kp_entry = get_kp_sublord(data['longitude'])
        kp_data[name] = {
            'longitude': data['longitude'],
            'sign': data['sign'],
            'sign_lord': data.get('sign_lord', ''),
            'star_lord': kp_entry['nakshatra_lord'],
            'sub_lord': kp_entry['sub_lord'],
            'nakshatra': kp_entry['nakshatra'],
        }

    return kp_data


def get_ruling_planets(date_str, time_str='09:15', lat=19.0760, lon=72.8777):
    """
    KP Ruling Planets at a given moment.
    These are the 5 significators of the current moment:
    1. Ascendant sign lord
    2. Ascendant star lord
    3. Ascendant sub lord
    4. Moon sign lord
    5. Moon star lord
    6. Day lord
    
    Ruling planets that agree with a chart's significators = CONFIRMATION.
    """
    positions = get_planetary_positions(date_str, time_str)
    ascendant = get_ascendant(date_str, time_str, lat, lon)

    # Ascendant KP
    asc_kp = get_kp_sublord(ascendant['degree'])

    # Moon KP
    moon_kp = get_kp_sublord(positions['Moon']['longitude'])

    # Day lord
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    day_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
    day_lord = day_lords[dt.weekday()]

    ruling = {
        'asc_sign_lord': ascendant.get('nakshatra_lord', asc_kp['nakshatra_lord']),
        'asc_star_lord': asc_kp['nakshatra_lord'],
        'asc_sub_lord': asc_kp['sub_lord'],
        'moon_sign_lord': positions['Moon'].get('sign_lord', ''),
        'moon_star_lord': moon_kp['nakshatra_lord'],
        'day_lord': day_lord,
    }

    # Get unique ruling planets
    all_rulers = list(set(ruling.values()))

    # Market interpretation
    bullish_rulers = ['Jupiter', 'Venus', 'Moon', 'Mercury']
    bearish_rulers = ['Saturn', 'Mars', 'Rahu', 'Ketu']

    bull_count = sum(1 for r in all_rulers if r in bullish_rulers)
    bear_count = sum(1 for r in all_rulers if r in bearish_rulers)

    if bull_count > bear_count:
        bias = 'BULLISH'
        note = 'Ruling planets favor optimism and buying'
    elif bear_count > bull_count:
        bias = 'BEARISH'
        note = 'Ruling planets favor caution and selling'
    else:
        bias = 'NEUTRAL'
        note = 'Mixed ruling planets — no clear direction'

    return {
        'components': ruling,
        'unique_rulers': all_rulers,
        'bullish_count': bull_count,
        'bearish_count': bear_count,
        'bias': bias,
        'note': note,
    }


def get_kp_analysis(date_str, time_str='09:15'):
    """Full KP analysis for market timing."""
    positions = get_planetary_positions(date_str, time_str)
    kp_sig = get_kp_significators(positions)
    ruling = get_ruling_planets(date_str, time_str)

    return {
        'date': date_str,
        'kp_significators': kp_sig,
        'ruling_planets': ruling,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 KP SYSTEM ANALYSIS — {today}")
    print("=" * 70)

    analysis = get_kp_analysis(today)

    print(f"\n📍 KP SIGNIFICATORS:")
    print(f"{'Planet':10s} {'Sign':10s} {'Sign Lord':10s} {'Star Lord':10s} {'Sub Lord':10s}")
    print("-" * 55)
    for name, data in analysis['kp_significators'].items():
        print(f"{name:10s} {data['sign']:10s} {data['sign_lord']:10s} "
              f"{data['star_lord']:10s} {data['sub_lord']:10s}")

    rp = analysis['ruling_planets']
    print(f"\n🎯 RULING PLANETS (9:15 AM Mumbai):")
    for key, value in rp['components'].items():
        print(f"  {key:20s}: {value}")
    print(f"\n  Unique Rulers: {', '.join(rp['unique_rulers'])}")
    print(f"  Bullish/Bearish: {rp['bullish_count']}/{rp['bearish_count']}")
    print(f"  📊 BIAS: {rp['bias']} — {rp['note']}")