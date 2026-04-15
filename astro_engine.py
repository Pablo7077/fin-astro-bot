"""
=============================================================
FIN ASTRO BOT — Planetary Calculation Engine
=============================================================
Calculates Vedic (sidereal/Lahiri) planetary positions,
retrogrades, combustions, nakshatras, and key yogas.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
import math
import os

# ── Setup Swiss Ephemeris ─────────────────────────────────
EPHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ephe')
swe.set_ephe_path(EPHE_PATH)
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Standard Indian Astrology

# ── Constants ─────────────────────────────────────────────
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,    # North Node
}

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
    'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
    'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
    'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
    'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13.333... degrees each

# Combustion ranges (degrees from Sun) — standard Vedic values
COMBUSTION_RANGES = {
    'Moon': 12.0,
    'Mercury': 14.0,
    'Venus': 10.0,
    'Mars': 17.0,
    'Jupiter': 11.0,
    'Saturn': 15.0,
}

# ── Helper Functions ──────────────────────────────────────

def date_to_jd(date_str, time_str='12:00'):
    """Convert date string 'YYYY-MM-DD' and time 'HH:MM' to Julian Day."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd = swe.julday(dt.year, dt.month, dt.day,
                     dt.hour + dt.minute / 60.0)
    return jd


def get_sign(degree):
    """Get zodiac sign from sidereal degree (0-360)."""
    sign_index = int(degree / 30.0) % 12
    return SIGNS[sign_index]


def get_sign_degree(degree):
    """Get degree within sign (0-30)."""
    return degree % 30.0


def get_nakshatra(degree):
    """Get nakshatra name and pada from sidereal degree."""
    nak_index = int(degree / NAKSHATRA_SPAN) % 27
    pada = int((degree % NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4.0)) + 1
    return NAKSHATRAS[nak_index], pada


def get_tithi(moon_deg, sun_deg):
    """Calculate lunar tithi (1-30) from Moon and Sun positions."""
    diff = (moon_deg - sun_deg) % 360.0
    tithi_num = int(diff / 12.0) + 1
    tithi_names = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima',
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Amavasya'
    ]
    paksha = 'Shukla' if tithi_num <= 15 else 'Krishna'
    name = tithi_names[min(tithi_num - 1, 29)]
    return tithi_num, name, paksha


def angular_distance(deg1, deg2):
    """Shortest angular distance between two degrees."""
    diff = abs(deg1 - deg2) % 360.0
    return min(diff, 360.0 - diff)


# ── Main Planetary Calculation ────────────────────────────

def get_planetary_positions(date_str, time_str='12:00'):
    """
    Calculate all planetary positions for a given date.
    Returns a dictionary with full details for each planet.
    """
    jd = date_to_jd(date_str, time_str)
    positions = {}

    for name, planet_id in PLANETS.items():
        # Calculate position with speed
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        result = swe.calc_ut(jd, planet_id, flags)
        
        longitude = result[0][0]  # Sidereal longitude
        speed = result[0][3]      # Daily speed in degrees

        # Normalize longitude to 0-360
        longitude = longitude % 360.0

        sign = get_sign(longitude)
        sign_deg = get_sign_degree(longitude)
        nakshatra, pada = get_nakshatra(longitude)
        is_retrograde = speed < 0

        positions[name] = {
            'longitude': round(longitude, 4),
            'sign': sign,
            'sign_degree': round(sign_deg, 2),
            'nakshatra': nakshatra,
            'pada': pada,
            'speed': round(speed, 4),
            'retrograde': is_retrograde,
        }

    # Calculate Ketu (always exactly opposite Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180.0) % 360.0
    positions['Ketu'] = {
        'longitude': round(ketu_long, 4),
        'sign': get_sign(ketu_long),
        'sign_degree': round(get_sign_degree(ketu_long), 2),
        'nakshatra': get_nakshatra(ketu_long)[0],
        'pada': get_nakshatra(ketu_long)[1],
        'speed': -abs(positions['Rahu']['speed']),  # Always retrograde
        'retrograde': True,  # Nodes always retrograde
    }

    return positions


# ── Astro Event Detection ─────────────────────────────────

def detect_combustions(positions):
    """Detect planets combust (too close to Sun)."""
    combustions = []
    sun_deg = positions['Sun']['longitude']

    for planet, max_dist in COMBUSTION_RANGES.items():
        if planet in positions:
            planet_deg = positions[planet]['longitude']
            dist = angular_distance(sun_deg, planet_deg)
            if dist <= max_dist:
                combustions.append({
                    'planet': planet,
                    'distance_from_sun': round(dist, 2),
                    'max_range': max_dist,
                    'severity': 'Deep' if dist < max_dist / 2 else 'Partial'
                })

    return combustions


def detect_major_aspects(positions):
    """Detect major Vedic aspects between planets."""
    aspects = []
    planet_names = list(positions.keys())

    # Standard aspect orbs (degrees) — Vedic uses wider orbs
    aspect_types = {
        0: ('Conjunction', 10),
        60: ('Sextile', 6),
        90: ('Square', 8),
        120: ('Trine', 8),
        180: ('Opposition', 10),
    }

    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]
            dist = angular_distance(
                positions[p1]['longitude'],
                positions[p2]['longitude']
            )
            for exact_angle, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': p1,
                        'planet2': p2,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 2
                    })

    return aspects


def detect_yogas(positions, aspects):
    """Detect important Vedic yogas relevant to markets."""
    yogas = []

    # 1. Guru-Chandala Yoga: Jupiter conjunct Rahu
    jup_deg = positions['Jupiter']['longitude']
    rahu_deg = positions['Rahu']['longitude']
    if angular_distance(jup_deg, rahu_deg) <= 15:
        yogas.append({
            'name': 'Guru-Chandala Yoga',
            'planets': ['Jupiter', 'Rahu'],
            'effect': 'Distorted wisdom, over-speculation, market manipulation risk',
            'market_bias': 'volatile_bearish'
        })

    # 2. Gaja-Kesari Yoga: Jupiter and Moon in mutual kendras (1/4/7/10)
    moon_deg = positions['Moon']['longitude']
    moon_sign_num = int(moon_deg / 30) % 12
    jup_sign_num = int(jup_deg / 30) % 12
    sign_diff = (jup_sign_num - moon_sign_num) % 12
    if sign_diff in [0, 3, 6, 9]:  # Kendra positions
        yogas.append({
            'name': 'Gaja-Kesari Yoga',
            'planets': ['Jupiter', 'Moon'],
            'effect': 'Prosperity, optimism, positive sentiment',
            'market_bias': 'bullish'
        })

    # 3. Grahan Yoga: Sun/Moon conjunct Rahu/Ketu (eclipse-like)
    ketu_deg = positions['Ketu']['longitude']
    sun_deg = positions['Sun']['longitude']
    for node_name, node_deg in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        for luminary, lum_deg in [('Sun', sun_deg), ('Moon', moon_deg)]:
            if angular_distance(lum_deg, node_deg) <= 12:
                yogas.append({
                    'name': f'Grahan Yoga ({luminary}-{node_name})',
                    'planets': [luminary, node_name],
                    'effect': f'{luminary} eclipsed — confusion, fear, sudden reversals',
                    'market_bias': 'volatile'
                })

    # 4. Saturn-Mars aspect/conjunction — aggression, crashes
    sat_deg = positions['Saturn']['longitude']
    mars_deg = positions['Mars']['longitude']
    sat_mars_dist = angular_distance(sat_deg, mars_deg)
    if sat_mars_dist <= 10:
        yogas.append({
            'name': 'Saturn-Mars Conjunction/War',
            'planets': ['Saturn', 'Mars'],
            'effect': 'Extreme tension, conflict energy, potential sharp drops',
            'market_bias': 'bearish'
        })
    elif abs(sat_mars_dist - 180) <= 10:
        yogas.append({
            'name': 'Saturn-Mars Opposition',
            'planets': ['Saturn', 'Mars'],
            'effect': 'Push-pull conflict, whipsaw markets',
            'market_bias': 'volatile_bearish'
        })

    # 5. Venus-Jupiter conjunction — wealth combination
    ven_deg = positions['Venus']['longitude']
    if angular_distance(ven_deg, jup_deg) <= 10:
        yogas.append({
            'name': 'Venus-Jupiter Conjunction',
            'planets': ['Venus', 'Jupiter'],
            'effect': 'Wealth, optimism, bullish sentiment for markets',
            'market_bias': 'bullish'
        })

    # 6. Multiple retrograde stress
    retro_count = sum(1 for p in positions.values() if p['retrograde']
                      and p != positions.get('Rahu') and p != positions.get('Ketu'))
    if retro_count >= 3:
        retro_planets = [name for name, data in positions.items()
                        if data['retrograde'] and name not in ['Rahu', 'Ketu']]
        yogas.append({
            'name': 'Multiple Retrograde Stress',
            'planets': retro_planets,
            'effect': f'{retro_count} planets retrograde — review, revision, uncertainty',
            'market_bias': 'volatile'
        })

    return yogas


def get_moon_phase(positions):
    """Determine Moon phase for market sentiment."""
    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']
    diff = (moon_deg - sun_deg) % 360.0

    tithi_num, tithi_name, paksha = get_tithi(moon_deg, sun_deg)

    if diff < 15:
        phase = 'New Moon (Amavasya zone)'
        market_note = 'Low energy, reversals possible, avoid big positions'
    elif diff < 90:
        phase = 'Waxing Crescent'
        market_note = 'Building momentum, cautious buying'
    elif diff < 135:
        phase = 'Waxing Gibbous'
        market_note = 'Strong momentum, trend continuation likely'
    elif diff < 195:
        phase = 'Full Moon (Purnima zone)'
        market_note = 'Peak emotion, high volatility, possible reversal'
    elif diff < 270:
        phase = 'Waning Gibbous'
        market_note = 'Profit booking phase, declining momentum'
    elif diff < 345:
        phase = 'Waning Crescent'
        market_note = 'Exhaustion, caution, prepare for new cycle'
    else:
        phase = 'New Moon (Amavasya zone)'
        market_note = 'Low energy, reversals possible, avoid big positions'

    return {
        'phase': phase,
        'tithi_number': tithi_num,
        'tithi_name': tithi_name,
        'paksha': paksha,
        'sun_moon_distance': round(diff, 2),
        'market_note': market_note
    }


def detect_ingresses(date_str):
    """Check if any planet changes sign today (ingress = big energy shift)."""
    jd_today = date_to_jd(date_str, '12:00')
    jd_yesterday = date_to_jd(
        (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d'),
        '12:00'
    )

    ingresses = []
    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL
        res_today = swe.calc_ut(jd_today, planet_id, flags)
        res_yesterday = swe.calc_ut(jd_yesterday, planet_id, flags)

        sign_today = get_sign(res_today[0][0] % 360)
        sign_yesterday = get_sign(res_yesterday[0][0] % 360)

        if sign_today != sign_yesterday:
            ingresses.append({
                'planet': name,
                'from_sign': sign_yesterday,
                'to_sign': sign_today,
                'event': f'{name} enters {sign_today} (from {sign_yesterday})'
            })

    return ingresses


# ── Full Analysis for a Date ──────────────────────────────

def full_astro_analysis(date_str, time_str='12:00'):
    """
    Complete astrological analysis for a given date.
    Returns all data needed for market correlation.
    """
    positions = get_planetary_positions(date_str, time_str)
    combustions = detect_combustions(positions)
    aspects = detect_major_aspects(positions)
    yogas = detect_yogas(positions, aspects)
    moon_phase = get_moon_phase(positions)
    ingresses = detect_ingresses(date_str)

    # Build retrograde list
    retrogrades = [
        name for name, data in positions.items()
        if data['retrograde'] and name not in ['Rahu', 'Ketu']
    ]

    return {
        'date': date_str,
        'positions': positions,
        'retrogrades': retrogrades,
        'combustions': combustions,
        'aspects': aspects,
        'yogas': yogas,
        'moon_phase': moon_phase,
        'ingresses': ingresses,
    }


# ── Quick Test ────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 FIN ASTRO — Planetary Analysis for {today}")
    print("=" * 55)

    analysis = full_astro_analysis(today)

    print("\n📍 PLANETARY POSITIONS (Sidereal/Lahiri):")
    print("-" * 55)
    for name, data in analysis['positions'].items():
        retro_mark = ' ℞' if data['retrograde'] else ''
        print(f"  {name:10s} → {data['sign']:13s} "
              f"{data['sign_degree']:6.2f}° "
              f"| {data['nakshatra']} Pada-{data['pada']}"
              f"{retro_mark}")

    if analysis['retrogrades']:
        print(f"\n🔄 RETROGRADES: {', '.join(analysis['retrogrades'])}")

    if analysis['combustions']:
        print(f"\n🔥 COMBUSTIONS:")
        for c in analysis['combustions']:
            print(f"  {c['planet']} — {c['severity']} "
                  f"({c['distance_from_sun']}° from Sun)")

    print(f"\n🌙 MOON PHASE: {analysis['moon_phase']['phase']}")
    print(f"   Tithi: {analysis['moon_phase']['paksha']} "
          f"{analysis['moon_phase']['tithi_name']} "
          f"(#{analysis['moon_phase']['tithi_number']})")
    print(f"   Market Note: {analysis['moon_phase']['market_note']}")

    if analysis['yogas']:
        print(f"\n⭐ ACTIVE YOGAS:")
        for y in analysis['yogas']:
            print(f"  {y['name']}: {y['effect']} [{y['market_bias']}]")

    if analysis['ingresses']:
        print(f"\n🚀 SIGN CHANGES TODAY:")
        for ing in analysis['ingresses']:
            print(f"  {ing['event']}")

    if analysis['aspects']:
        tight = [a for a in analysis['aspects'] if a['tight']]
        if tight:
            print(f"\n🎯 TIGHT ASPECTS (within 2°):")
            for a in tight:
                print(f"  {a['planet1']} {a['aspect']} {a['planet2']} "
                      f"(orb: {a['orb']}°)")