"""
=============================================================
FIN ASTRO BOT v2.0 — Core Planetary Engine
=============================================================
Calculates Vedic (sidereal/Lahiri) planetary positions with
full dignity analysis, speed, and state detection.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
import math
import os

# ── Setup ─────────────────────────────────────────────────
EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ── Constants ─────────────────────────────────────────────
PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE,
}

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
    'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
    'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
    'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
    'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter',
    'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
    'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun',
    'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13°20' each

# ── Exaltation / Debilitation Data ────────────────────────
EXALTATION = {
    'Sun': ('Aries', 10), 'Moon': ('Taurus', 3), 'Mercury': ('Virgo', 15),
    'Venus': ('Pisces', 27), 'Mars': ('Capricorn', 28),
    'Jupiter': ('Cancer', 5), 'Saturn': ('Libra', 20),
    'Rahu': ('Taurus', 20), 'Ketu': ('Scorpio', 20),
}

DEBILITATION = {
    'Sun': ('Libra', 10), 'Moon': ('Scorpio', 3), 'Mercury': ('Pisces', 15),
    'Venus': ('Virgo', 27), 'Mars': ('Cancer', 28),
    'Jupiter': ('Capricorn', 5), 'Saturn': ('Aries', 20),
    'Rahu': ('Scorpio', 20), 'Ketu': ('Taurus', 20),
}

MOOLATRIKONA = {
    'Sun': ('Leo', 0, 20), 'Moon': ('Taurus', 3, 30),
    'Mercury': ('Virgo', 15, 20), 'Venus': ('Libra', 0, 15),
    'Mars': ('Aries', 0, 12), 'Jupiter': ('Sagittarius', 0, 10),
    'Saturn': ('Aquarius', 0, 20),
}

OWN_SIGNS = {
    'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
    'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
    'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius'],
}

# Planetary friendship table
NATURAL_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
}

NATURAL_ENEMIES = {
    'Sun': ['Venus', 'Saturn'],
    'Moon': [],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
}

# Combustion ranges
COMBUSTION_RANGES = {
    'Moon': 12.0, 'Mercury': 14.0, 'Venus': 10.0,
    'Mars': 17.0, 'Jupiter': 11.0, 'Saturn': 15.0,
}

# ── Helper Functions ──────────────────────────────────────

def date_to_jd(date_str, time_str='12:00'):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

def get_sign_index(degree):
    return int(degree / 30.0) % 12

def get_sign(degree):
    return SIGNS[get_sign_index(degree)]

def get_sign_degree(degree):
    return degree % 30.0

def get_nakshatra(degree):
    nak_index = int(degree / NAKSHATRA_SPAN) % 27
    pada = int((degree % NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4.0)) + 1
    return NAKSHATRAS[nak_index], pada, NAKSHATRA_LORDS[nak_index]

def angular_distance(deg1, deg2):
    diff = abs(deg1 - deg2) % 360.0
    return min(diff, 360.0 - diff)

def sign_distance(sign1, sign2):
    """Houses between two signs (1-indexed)."""
    idx1 = SIGNS.index(sign1)
    idx2 = SIGNS.index(sign2)
    return ((idx2 - idx1) % 12) + 1

# ── Planetary Dignity ─────────────────────────────────────

def get_dignity(planet_name, sign, sign_deg):
    """
    Determine the dignity/state of a planet.
    Returns: 'Exalted', 'Moolatrikona', 'Own Sign', 'Friendly',
             'Neutral', 'Enemy', 'Debilitated'
    """
    # Check Exaltation
    if planet_name in EXALTATION:
        ex_sign, ex_deg = EXALTATION[planet_name]
        if sign == ex_sign:
            return 'Exalted'

    # Check Debilitation
    if planet_name in DEBILITATION:
        deb_sign, deb_deg = DEBILITATION[planet_name]
        if sign == deb_sign:
            return 'Debilitated'

    # Check Moolatrikona
    if planet_name in MOOLATRIKONA:
        mt_sign, mt_start, mt_end = MOOLATRIKONA[planet_name]
        if sign == mt_sign and mt_start <= sign_deg <= mt_end:
            return 'Moolatrikona'

    # Check Own Sign
    if planet_name in OWN_SIGNS:
        if sign in OWN_SIGNS[planet_name]:
            return 'Own Sign'

    # Check Friend/Enemy based on sign lord
    sign_lord = SIGN_LORDS.get(sign, '')
    if planet_name in NATURAL_FRIENDS:
        if sign_lord in NATURAL_FRIENDS.get(planet_name, []):
            return 'Friendly'
    if planet_name in NATURAL_ENEMIES:
        if sign_lord in NATURAL_ENEMIES.get(planet_name, []):
            return 'Enemy'

    return 'Neutral'


def get_dignity_score(dignity):
    """Numerical score for dignity (for weighted calculations)."""
    scores = {
        'Exalted': 5, 'Moolatrikona': 4, 'Own Sign': 3,
        'Friendly': 2, 'Neutral': 1, 'Enemy': -1, 'Debilitated': -2,
    }
    return scores.get(dignity, 0)


# ── Main Calculation ──────────────────────────────────────

def get_planetary_positions(date_str, time_str='12:00'):
    """Full planetary positions with dignity, nakshatra lords, etc."""
    jd = date_to_jd(date_str, time_str)
    positions = {}

    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        result = swe.calc_ut(jd, planet_id, flags)

        longitude = result[0][0] % 360.0
        lat = result[0][1]
        speed = result[0][3]

        sign = get_sign(longitude)
        sign_deg = get_sign_degree(longitude)
        nakshatra, pada, nak_lord = get_nakshatra(longitude)
        is_retro = speed < 0
        dignity = get_dignity(name, sign, sign_deg)

        positions[name] = {
            'longitude': round(longitude, 4),
            'latitude': round(lat, 4),
            'sign': sign,
            'sign_index': get_sign_index(longitude),
            'sign_degree': round(sign_deg, 2),
            'nakshatra': nakshatra,
            'pada': pada,
            'nakshatra_lord': nak_lord,
            'sign_lord': SIGN_LORDS.get(sign, ''),
            'speed': round(speed, 4),
            'retrograde': is_retro,
            'dignity': dignity,
            'dignity_score': get_dignity_score(dignity),
        }

    # Ketu (opposite Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180.0) % 360.0
    ketu_sign = get_sign(ketu_long)
    ketu_sign_deg = get_sign_degree(ketu_long)
    ketu_nak, ketu_pada, ketu_nak_lord = get_nakshatra(ketu_long)

    positions['Ketu'] = {
        'longitude': round(ketu_long, 4),
        'latitude': 0.0,
        'sign': ketu_sign,
        'sign_index': get_sign_index(ketu_long),
        'sign_degree': round(ketu_sign_deg, 2),
        'nakshatra': ketu_nak,
        'pada': ketu_pada,
        'nakshatra_lord': ketu_nak_lord,
        'sign_lord': SIGN_LORDS.get(ketu_sign, ''),
        'speed': -abs(positions['Rahu']['speed']),
        'retrograde': True,
        'dignity': get_dignity('Ketu', ketu_sign, ketu_sign_deg),
        'dignity_score': get_dignity_score(get_dignity('Ketu', ketu_sign, ketu_sign_deg)),
    }

    return positions


def detect_combustions(positions):
    """Detect combust planets with cazimi check."""
    combustions = []
    sun_deg = positions['Sun']['longitude']

    for planet, max_dist in COMBUSTION_RANGES.items():
        if planet in positions:
            dist = angular_distance(sun_deg, positions[planet]['longitude'])
            if dist <= max_dist:
                if dist <= 0.2833:  # 17 arcminutes = cazimi
                    severity = 'Cazimi (POWERFUL)'
                elif dist < max_dist / 3:
                    severity = 'Deep'
                elif dist < max_dist * 2 / 3:
                    severity = 'Moderate'
                else:
                    severity = 'Partial'

                combustions.append({
                    'planet': planet,
                    'distance_from_sun': round(dist, 2),
                    'max_range': max_dist,
                    'severity': severity,
                    'is_cazimi': dist <= 0.2833,
                })
    return combustions


def detect_planetary_war(positions):
    """Detect Graha Yuddha (planetary war) — two planets within 1°."""
    wars = []
    combat_planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    for i in range(len(combat_planets)):
        for j in range(i + 1, len(combat_planets)):
            p1, p2 = combat_planets[i], combat_planets[j]
            dist = angular_distance(
                positions[p1]['longitude'],
                positions[p2]['longitude']
            )
            if dist <= 1.0:
                # Winner has higher latitude (north)
                lat1 = positions[p1].get('latitude', 0)
                lat2 = positions[p2].get('latitude', 0)
                winner = p1 if lat1 > lat2 else p2
                loser = p2 if winner == p1 else p1

                wars.append({
                    'planet1': p1, 'planet2': p2,
                    'distance': round(dist, 3),
                    'winner': winner, 'loser': loser,
                    'sign': positions[p1]['sign'],
                })
    return wars


def detect_major_aspects(positions):
    """Detect aspects with Vedic special aspects included."""
    aspects = []
    planet_names = list(positions.keys())

    # Standard aspects
    aspect_types = {
        0: ('Conjunction', 10), 60: ('Sextile', 6),
        90: ('Square', 8), 120: ('Trine', 8), 180: ('Opposition', 10),
    }

    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1, p2 = planet_names[i], planet_names[j]
            dist = angular_distance(
                positions[p1]['longitude'], positions[p2]['longitude']
            )
            for exact_angle, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': p1, 'planet2': p2,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 2,
                    })

    # Vedic special aspects
    # Mars: 4th and 8th house aspects (90° and 210°)
    # Jupiter: 5th and 9th house aspects (120° and 240°)
    # Saturn: 3rd and 10th house aspects (60° and 270°)
    vedic_special = {
        'Mars': [(120, 'Mars 4th aspect', 8), (210, 'Mars 8th aspect', 8)],
        'Jupiter': [(150, 'Jupiter 5th aspect', 8), (240, 'Jupiter 9th aspect', 8)],
        'Saturn': [(60, 'Saturn 3rd aspect', 8), (270, 'Saturn 10th aspect', 8)],
    }

    for special_planet, aspect_list in vedic_special.items():
        if special_planet not in positions:
            continue
        sp_long = positions[special_planet]['longitude']
        for other_name in planet_names:
            if other_name == special_planet:
                continue
            dist = (positions[other_name]['longitude'] - sp_long) % 360
            for exact_angle, aspect_name, orb in aspect_list:
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': special_planet, 'planet2': other_name,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 3,
                    })

    return aspects


def detect_ingresses(date_str):
    """Check for sign changes (ingresses)."""
    jd_today = date_to_jd(date_str, '12:00')
    yesterday = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    jd_yesterday = date_to_jd(yesterday, '12:00')

    ingresses = []
    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL
        today_long = swe.calc_ut(jd_today, planet_id, flags)[0][0] % 360
        yest_long = swe.calc_ut(jd_yesterday, planet_id, flags)[0][0] % 360

        if get_sign(today_long) != get_sign(yest_long):
            ingresses.append({
                'planet': name,
                'from_sign': get_sign(yest_long),
                'to_sign': get_sign(today_long),
            })
    return ingresses


def detect_stations(date_str):
    """Detect planets turning retrograde or direct (station)."""
    stations = []
    today = datetime.strptime(date_str, '%Y-%m-%d')

    for name, planet_id in PLANETS.items():
        if name in ['Sun', 'Moon', 'Rahu']:
            continue

        jd_today = date_to_jd(date_str, '12:00')
        jd_yesterday = date_to_jd((today - timedelta(days=1)).strftime('%Y-%m-%d'), '12:00')

        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        speed_today = swe.calc_ut(jd_today, planet_id, flags)[0][3]
        speed_yesterday = swe.calc_ut(jd_yesterday, planet_id, flags)[0][3]

        if speed_yesterday >= 0 and speed_today < 0:
            stations.append({
                'planet': name, 'type': 'Turns Retrograde',
                'market_impact': 'HIGH — expect reversal/volatility'
            })
        elif speed_yesterday < 0 and speed_today >= 0:
            stations.append({
                'planet': name, 'type': 'Turns Direct',
                'market_impact': 'HIGH — blocked energy releases'
            })
        elif abs(speed_today) < 0.02 and name not in ['Moon']:
            stations.append({
                'planet': name, 'type': 'Near Stationary',
                'market_impact': 'MEDIUM — planet energy concentrated'
            })

    return stations


def get_ascendant(date_str, time_str='09:15', lat=19.0760, lon=72.8777):
    """
    Calculate Lagna (Ascendant) for a given date/time/location.
    Default: Mumbai (NSE location), 9:15 AM (market open).
    """
    jd = date_to_jd(date_str, time_str)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    asc_degree = ascmc[0] % 360
    return {
        'degree': round(asc_degree, 4),
        'sign': get_sign(asc_degree),
        'sign_degree': round(get_sign_degree(asc_degree), 2),
        'nakshatra': get_nakshatra(asc_degree)[0],
        'pada': get_nakshatra(asc_degree)[1],
        'nakshatra_lord': get_nakshatra(asc_degree)[2],
    }


# ── Full Analysis ─────────────────────────────────────────

def full_astro_analysis(date_str, time_str='12:00'):
    """Complete astrological analysis for a date."""
    positions = get_planetary_positions(date_str, time_str)
    return {
        'date': date_str,
        'positions': positions,
        'retrogrades': [n for n, d in positions.items()
                        if d['retrograde'] and n not in ['Rahu', 'Ketu']],
        'combustions': detect_combustions(positions),
        'planetary_wars': detect_planetary_war(positions),
        'aspects': detect_major_aspects(positions),
        'ingresses': detect_ingresses(date_str),
        'stations': detect_stations(date_str),
        'ascendant': get_ascendant(date_str),
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 FIN ASTRO v2.0 — Planetary Engine Test: {today}")
    print("=" * 60)

    analysis = full_astro_analysis(today)

    print("\n📍 PLANETARY POSITIONS:")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':18s} {'Dignity':14s} {'R':3s}")
    print("-" * 70)
    for name, d in analysis['positions'].items():
        r = '℞' if d['retrograde'] else ''
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:15s} P{d['pada']} "
              f"{d['dignity']:14s} {r}")

    if analysis['planetary_wars']:
        print(f"\n⚔️ PLANETARY WARS:")
        for w in analysis['planetary_wars']:
            print(f"  {w['planet1']} vs {w['planet2']} ({w['distance']:.3f}°) "
                  f"→ Winner: {w['winner']}, Loser: {w['loser']}")

    if analysis['stations']:
        print(f"\n🛑 STATIONS:")
        for s in analysis['stations']:
            print(f"  {s['planet']} — {s['type']} ({s['market_impact']})")

    print(f"\n🏠 ASCENDANT (Mumbai 9:15 AM): "
          f"{analysis['ascendant']['sign']} {analysis['ascendant']['sign_degree']:.2f}°")