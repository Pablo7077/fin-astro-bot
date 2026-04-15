"""
=============================================================
FIN ASTRO BOT v2.0 — Vimshottari Dasha System
=============================================================
Calculates Mahadasha → Antardasha → Pratyantardasha
for any birth chart (especially Nifty/Bank Nifty).
=============================================================
"""

from datetime import datetime, timedelta
from core.astro_engine import get_nakshatra, get_planetary_positions, NAKSHATRA_LORDS

# ── Vimshottari Dasha Periods (years) ─────────────────────
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
    'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17,
}

# Dasha sequence (always this order)
DASHA_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
                  'Rahu', 'Jupiter', 'Saturn', 'Mercury']

TOTAL_DASHA_YEARS = 120  # Full Vimshottari cycle

# Market interpretation of each Mahadasha lord
DASHA_MARKET_INTERPRETATION = {
    'Sun': {
        'general': 'Government focus, policy-driven markets, gold bullish',
        'bullish_sectors': ['Power', 'Pharma', 'PSU Banks', 'Gold'],
        'bearish_sectors': ['Opposition-linked sectors'],
        'overall': 'Moderate bullish with authority/policy themes',
    },
    'Moon': {
        'general': 'Sentiment-driven markets, liquidity focus, silver & FMCG',
        'bullish_sectors': ['FMCG', 'Silver', 'Hospitality', 'Water'],
        'bearish_sectors': ['Heavy industry (lack of stability)'],
        'overall': 'Emotional, volatile, liquidity-dependent',
    },
    'Mars': {
        'general': 'Aggressive markets, high volatility, defense & real estate focus',
        'bullish_sectors': ['Real Estate', 'Defense', 'Steel', 'Energy'],
        'bearish_sectors': ['Peaceful sectors', 'Tourism'],
        'overall': 'Volatile with sharp rallies AND crashes',
    },
    'Mercury': {
        'general': 'Communication, IT, trade-focused markets, fast moves',
        'bullish_sectors': ['IT', 'Telecom', 'E-commerce', 'Banking'],
        'bearish_sectors': ['Traditional manufacturing'],
        'overall': 'Smart money, quick trades, data-driven moves',
    },
    'Jupiter': {
        'general': 'Expansion, optimism, banking & finance boom, bull markets',
        'bullish_sectors': ['Banking', 'Finance', 'Education', 'Law'],
        'bearish_sectors': ['Rarely bearish in Jupiter period'],
        'overall': '🟢 MOST BULLISH dasha — expansion, prosperity',
    },
    'Venus': {
        'general': 'Luxury, consumption, auto, entertainment focus',
        'bullish_sectors': ['Auto', 'Luxury', 'Entertainment', 'Textiles'],
        'bearish_sectors': ['Austerity-linked sectors'],
        'overall': 'Bullish with consumer & lifestyle themes',
    },
    'Saturn': {
        'general': 'Restrictive, slow, infrastructure focus, corrections',
        'bullish_sectors': ['Infrastructure', 'Mining', 'Oil & Gas', 'Agriculture'],
        'bearish_sectors': ['Luxury', 'Entertainment', 'Growth stocks'],
        'overall': '🔴 MOST CHALLENGING dasha — corrections, bear phases',
    },
    'Rahu': {
        'general': 'Foreign influence, speculation, crypto, disruption',
        'bullish_sectors': ['Tech disruption', 'Crypto', 'Foreign investment'],
        'bearish_sectors': ['Traditional value stocks'],
        'overall': 'Wild, speculative, unpredictable — booms AND busts',
    },
    'Ketu': {
        'general': 'Spiritual, detached, sudden events, IT backend',
        'bullish_sectors': ['Pharma (research)', 'IT services', 'Spiritual'],
        'bearish_sectors': ['Material luxury', 'Entertainment'],
        'overall': 'Confusing, detached, sudden reversals',
    },
}


# ── Dasha Calculation ─────────────────────────────────────

def calculate_dasha_periods(moon_longitude, birth_date_str):
    """
    Calculate all Mahadasha periods from birth date based on Moon's nakshatra.
    
    Args:
        moon_longitude: Sidereal longitude of Moon at birth
        birth_date_str: 'YYYY-MM-DD' format
    
    Returns:
        List of dasha periods with start/end dates
    """
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

    # Get Moon's nakshatra
    nak_name, pada, nak_lord = get_nakshatra(moon_longitude)

    # Calculate elapsed portion of starting nakshatra
    nak_span = 360.0 / 27.0  # 13.333...
    nak_start_deg = (moon_longitude // nak_span) * nak_span
    elapsed_in_nak = moon_longitude - nak_start_deg
    nak_fraction_elapsed = elapsed_in_nak / nak_span

    # First dasha lord = nakshatra lord
    first_lord = nak_lord
    first_lord_total_years = DASHA_YEARS[first_lord]
    first_lord_remaining_years = first_lord_total_years * (1 - nak_fraction_elapsed)

    # Build dasha sequence starting from first lord
    start_idx = DASHA_SEQUENCE.index(first_lord)

    dashas = []
    current_date = birth_date

    # First (partial) dasha
    days = first_lord_remaining_years * 365.25
    end_date = current_date + timedelta(days=days)
    interp = DASHA_MARKET_INTERPRETATION.get(first_lord, {})
    dashas.append({
        'lord': first_lord,
        'start': current_date,
        'end': end_date,
        'years': round(first_lord_remaining_years, 2),
        'is_partial': True,
        'interpretation': interp,
    })
    current_date = end_date

    # Remaining full dashas (cycle through)
    for i in range(1, 10):  # Up to 9 more dashas (full cycle = 120 years)
        lord_idx = (start_idx + i) % 9
        lord = DASHA_SEQUENCE[lord_idx]
        years = DASHA_YEARS[lord]
        days = years * 365.25
        end_date = current_date + timedelta(days=days)
        interp = DASHA_MARKET_INTERPRETATION.get(lord, {})

        dashas.append({
            'lord': lord,
            'start': current_date,
            'end': end_date,
            'years': years,
            'is_partial': False,
            'interpretation': interp,
        })
        current_date = end_date

        # Stop if we've gone 120+ years from birth
        if (current_date - birth_date).days > 120 * 365.25:
            break

    return {
        'moon_nakshatra': nak_name,
        'moon_pada': pada,
        'nakshatra_lord': nak_lord,
        'dashas': dashas,
    }


def calculate_antardasha(mahadasha_lord, maha_start, maha_end):
    """
    Calculate Antardasha (sub-periods) within a Mahadasha.
    """
    maha_days = (maha_end - maha_start).total_seconds() / 86400.0
    total_dasha_days = TOTAL_DASHA_YEARS * 365.25

    start_idx = DASHA_SEQUENCE.index(mahadasha_lord)
    antardashas = []
    current_date = maha_start

    for i in range(9):
        lord_idx = (start_idx + i) % 9
        lord = DASHA_SEQUENCE[lord_idx]

        # Antardasha proportion = (maha_years * antar_years) / total_years
        proportion = (DASHA_YEARS[mahadasha_lord] * DASHA_YEARS[lord]) / (TOTAL_DASHA_YEARS)
        antar_days = proportion * 365.25

        # Scale to actual mahadasha duration
        scale_factor = maha_days / (DASHA_YEARS[mahadasha_lord] * 365.25)
        actual_days = antar_days * scale_factor

        end_date = current_date + timedelta(days=actual_days)

        if end_date > maha_end:
            end_date = maha_end

        antardashas.append({
            'mahadasha_lord': mahadasha_lord,
            'antardasha_lord': lord,
            'start': current_date,
            'end': end_date,
            'days': round(actual_days),
        })

        current_date = end_date
        if current_date >= maha_end:
            break

    return antardashas


def get_current_dasha(dashas, target_date_str):
    """Find which Mahadasha and Antardasha is active on a given date."""
    target = datetime.strptime(target_date_str, '%Y-%m-%d')

    current_maha = None
    for d in dashas['dashas']:
        if d['start'] <= target <= d['end']:
            current_maha = d
            break

    if not current_maha:
        return None

    # Calculate antardashas
    antardashas = calculate_antardasha(
        current_maha['lord'], current_maha['start'], current_maha['end']
    )

    current_antar = None
    for a in antardashas:
        if a['start'] <= target <= a['end']:
            current_antar = a
            break

    return {
        'mahadasha': current_maha,
        'antardasha': current_antar,
        'all_antardashas': antardashas,
    }


# ── Predefined Birth Charts ──────────────────────────────

# Nifty 50: NSE launched 3 November 1995 at 9:55 AM IST
NIFTY_BIRTH = {
    'name': 'Nifty 50',
    'date': '1995-11-03',
    'time': '09:55',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

# Bank Nifty: launched 13 June 2005
BANKNIFTY_BIRTH = {
    'name': 'Bank Nifty',
    'date': '2005-06-13',
    'time': '09:15',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

# Sensex: launched 1 January 1986
SENSEX_BIRTH = {
    'name': 'BSE Sensex',
    'date': '1986-01-01',
    'time': '10:00',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

BIRTH_CHARTS = {
    'nifty': NIFTY_BIRTH,
    'banknifty': BANKNIFTY_BIRTH,
    'sensex': SENSEX_BIRTH,
}


def get_index_dasha(index_name='nifty', target_date=None):
    """Get current dasha period for a market index."""
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    birth = BIRTH_CHARTS.get(index_name.lower(), NIFTY_BIRTH)

    # Get Moon position at birth
    positions = get_planetary_positions(birth['date'], birth['time'])
    moon_long = positions['Moon']['longitude']

    # Calculate dashas
    dashas = calculate_dasha_periods(moon_long, birth['date'])

    # Get current period
    current = get_current_dasha(dashas, target_date)

    return {
        'index': birth['name'],
        'birth_date': birth['date'],
        'moon_nakshatra': dashas['moon_nakshatra'],
        'moon_pada': dashas['moon_pada'],
        'all_dashas': dashas,
        'current': current,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 VIMSHOTTARI DASHA — NIFTY 50")
    print(f"   Birth: 3 Nov 1995 (NSE Launch)")
    print(f"   Analysis for: {today}")
    print("=" * 65)

    result = get_index_dasha('nifty', today)

    print(f"\n🌙 Nifty Moon Nakshatra: {result['moon_nakshatra']} "
          f"(Pada {result['moon_pada']})")

    if result['current']:
        maha = result['current']['mahadasha']
        print(f"\n📊 CURRENT MAHADASHA: {maha['lord']}")
        print(f"   Period: {maha['start'].strftime('%Y-%m-%d')} to "
              f"{maha['end'].strftime('%Y-%m-%d')}")
        print(f"   Duration: {maha['years']} years")

        interp = maha.get('interpretation', {})
        if interp:
            print(f"   General: {interp.get('general', 'N/A')}")
            print(f"   Overall: {interp.get('overall', 'N/A')}")
            print(f"   Bullish: {', '.join(interp.get('bullish_sectors', []))}")
            print(f"   Bearish: {', '.join(interp.get('bearish_sectors', []))}")

        antar = result['current'].get('antardasha')
        if antar:
            print(f"\n📊 CURRENT ANTARDASHA: {antar['antardasha_lord']}")
            print(f"   Period: {antar['start'].strftime('%Y-%m-%d')} to "
                  f"{antar['end'].strftime('%Y-%m-%d')}")
            print(f"   Duration: {antar['days']} days")

        print(f"\n📋 ALL MAHADASHAS FOR NIFTY:")
        print(f"{'Lord':10s} {'Start':12s} {'End':12s} {'Years':>6s}")
        print("-" * 45)
        for d in result['all_dashas']['dashas']:
            marker = ' ◀ CURRENT' if d['lord'] == maha['lord'] else ''
            print(f"{d['lord']:10s} {d['start'].strftime('%Y-%m-%d'):12s} "
                  f"{d['end'].strftime('%Y-%m-%d'):12s} {d['years']:6.1f}{marker}")