"""
=============================================================
FIN ASTRO BOT v2.0 — Panchang (Daily Vedic Calendar) Engine
=============================================================
Calculates: Tithi, Karana, Nitya Yoga, Vara (weekday),
Nakshatra, Gandanta zones, Void of Course Moon.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, date_to_jd, get_sign,
    get_nakshatra, angular_distance, SIGNS, NAKSHATRA_SPAN
)
import swisseph as swe
from datetime import datetime


# ── TITHI ─────────────────────────────────────────────────

TITHI_NAMES = [
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
    'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
    'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima',
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
    'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
    'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Amavasya'
]

TITHI_MARKET_NOTES = {
    'Pratipada': 'New beginning energy. Markets may set new direction.',
    'Dwitiya': 'Building phase. Moderate positivity.',
    'Tritiya': 'Creative energy. Good for growth stocks.',
    'Chaturthi': 'Vinayaka\'s tithi. Obstacles possible, then resolution.',
    'Panchami': 'Lakshmi\'s tithi. Generally auspicious for wealth.',
    'Shashthi': 'Mars energy. Volatility, quick moves.',
    'Saptami': 'Sun energy. Authority, government policy impact.',
    'Ashtami': '⚠️ CRITICAL: 8th tithi = transformation, sudden reversals, high risk.',
    'Navami': 'Mars energy. Aggressive moves, breakouts.',
    'Dashami': 'Completion energy. Trend may exhaust.',
    'Ekadashi': 'Fasting day. Low volume possible, spiritual energy.',
    'Dwadashi': 'Recovery phase after Ekadashi restraint.',
    'Trayodashi': 'Pradosh. Shiva energy. Destruction of old trends.',
    'Chaturdashi': '⚠️ Day before New/Full Moon. High tension. Avoid big bets.',
    'Purnima': '⚠️ FULL MOON: Peak emotion, reversals common, high volatility.',
    'Amavasya': '⚠️ NEW MOON: Low energy, confusion, avoid new positions.',
}


def get_tithi(moon_deg, sun_deg):
    diff = (moon_deg - sun_deg) % 360.0
    tithi_num = int(diff / 12.0) + 1
    tithi_num = min(tithi_num, 30)
    paksha = 'Shukla' if tithi_num <= 15 else 'Krishna'
    name = TITHI_NAMES[tithi_num - 1]
    market_note = TITHI_MARKET_NOTES.get(name, '')
    return {
        'number': tithi_num,
        'name': name,
        'paksha': paksha,
        'market_note': market_note,
        'is_critical': name in ['Ashtami', 'Chaturdashi', 'Purnima', 'Amavasya'],
    }


# ── KARANA ────────────────────────────────────────────────

KARANA_NAMES = [
    'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garija',
    'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Nagava', 'Kimstughna'
]

KARANA_NATURE = {
    'Bava': ('Movable', 'bullish', 'Good for starting trades'),
    'Balava': ('Movable', 'bullish', 'Strength, upward momentum'),
    'Kaulava': ('Movable', 'bullish', 'Friendship energy, accumulation'),
    'Taitila': ('Movable', 'bullish', 'Wealth building, steady gains'),
    'Garija': ('Movable', 'neutral', 'Mixed energy, consolidation'),
    'Vanija': ('Movable', 'bullish', 'Trade & commerce favorable'),
    'Vishti': ('Fixed', 'bearish', '⚠️ BHADRA KARANA: Very inauspicious. Avoid new trades. Losses likely.'),
    'Shakuni': ('Fixed', 'volatile', 'Bird of omen — sudden news, unexpected moves'),
    'Chatushpada': ('Fixed', 'bearish', 'Stubbornness, resistance to trend'),
    'Nagava': ('Fixed', 'bearish', 'Snake energy — hidden dangers, manipulation'),
    'Kimstughna': ('Fixed', 'neutral', 'Confusion, unclear direction'),
}


def get_karana(moon_deg, sun_deg):
    diff = (moon_deg - sun_deg) % 360.0
    karana_num = int(diff / 6.0) + 1  # Each karana = 6° of Moon-Sun distance

    # First karana of Shukla Pratipada is Kimstughna
    # Cycle: Kimstughna (1st half of 1st tithi), then Bava-Vishti repeat,
    # last 4 karanas of Krishna Chaturdashi-Amavasya are fixed
    if karana_num == 1:
        name = 'Kimstughna'
    elif karana_num >= 58:
        fixed_karanas = ['Shakuni', 'Chatushpada', 'Nagava']
        name = fixed_karanas[karana_num - 58] if karana_num - 58 < 3 else 'Kimstughna'
    else:
        cycle_idx = (karana_num - 2) % 7
        name = KARANA_NAMES[cycle_idx]

    nature, bias, note = KARANA_NATURE.get(name, ('Unknown', 'neutral', ''))
    return {
        'number': karana_num,
        'name': name,
        'nature': nature,
        'market_bias': bias,
        'note': note,
        'is_vishti': name == 'Vishti',
    }


# ── NITYA YOGA (Astronomical Yoga) ───────────────────────

NITYA_YOGA_NAMES = [
    'Vishkambha', 'Preeti', 'Ayushman', 'Saubhagya', 'Shobhana',
    'Atiganda', 'Sukarma', 'Dhriti', 'Shoola', 'Ganda',
    'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
    'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
    'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
    'Indra', 'Vaidhriti'
]

NITYA_YOGA_NATURE = {
    'Vishkambha': ('Shubha', 'bullish', 'Obstacle-removing, good start'),
    'Preeti': ('Shubha', 'bullish', 'Love/joy — positive sentiment'),
    'Ayushman': ('Shubha', 'bullish', 'Long life — stability, longevity of trends'),
    'Saubhagya': ('Shubha', 'bullish', 'Good fortune — lucky day for markets'),
    'Shobhana': ('Shubha', 'bullish', 'Beauty — aesthetics, luxury sector up'),
    'Atiganda': ('Ashubha', 'bearish', '⚠️ Danger — accidents, sudden drops'),
    'Sukarma': ('Shubha', 'bullish', 'Good deeds rewarded — righteous gains'),
    'Dhriti': ('Shubha', 'bullish', 'Determination — trend holds strong'),
    'Shoola': ('Ashubha', 'bearish', '⚠️ Thorn/pain — losses, sharp pricks'),
    'Ganda': ('Ashubha', 'bearish', '⚠️ Knot — trapped, no exit, stuck markets'),
    'Vriddhi': ('Shubha', 'bullish', 'Growth — expansion, bullish signal'),
    'Dhruva': ('Shubha', 'bullish', 'Fixed/stable — consolidation, hold positions'),
    'Vyaghata': ('Ashubha', 'bearish', '⚠️ Destruction — breakdowns, crashes'),
    'Harshana': ('Shubha', 'bullish', 'Joy — optimistic buying'),
    'Vajra': ('Mixed', 'volatile', 'Thunderbolt — sudden powerful moves either way'),
    'Siddhi': ('Shubha', 'bullish', 'Accomplishment — targets hit, success'),
    'Vyatipata': ('Ashubha', 'bearish', '⚠️ Calamity — one of worst yogas. Major negativity.'),
    'Variyan': ('Shubha', 'bullish', 'Comfort — easy, flowing markets'),
    'Parigha': ('Ashubha', 'bearish', '⚠️ Obstacle/iron bar — blocked, resistance'),
    'Shiva': ('Shubha', 'bullish', 'Auspicious — divine blessing on markets'),
    'Siddha': ('Shubha', 'bullish', 'Accomplished — completion, profit booking'),
    'Sadhya': ('Shubha', 'bullish', 'Achievable — realistic targets met'),
    'Shubha': ('Shubha', 'bullish', 'Auspicious — one of the best yogas'),
    'Shukla': ('Shubha', 'bullish', 'Bright/white — clarity, transparency'),
    'Brahma': ('Shubha', 'bullish', 'Creator — new beginnings, IPOs favored'),
    'Indra': ('Shubha', 'bullish', 'King of gods — power, authority, leadership stocks'),
    'Vaidhriti': ('Ashubha', 'bearish', '⚠️ Split apart — division, breakdown, worst yoga'),
}


def get_nitya_yoga(moon_deg, sun_deg):
    """Nitya Yoga = (Sun longitude + Moon longitude) / 13°20'."""
    total = (sun_deg + moon_deg) % 360.0
    yoga_num = int(total / NAKSHATRA_SPAN) + 1
    yoga_num = min(yoga_num, 27)
    name = NITYA_YOGA_NAMES[yoga_num - 1]
    nature, bias, note = NITYA_YOGA_NATURE.get(name, ('Unknown', 'neutral', ''))
    return {
        'number': yoga_num,
        'name': name,
        'nature': nature,
        'market_bias': bias,
        'note': note,
        'is_inauspicious': nature == 'Ashubha',
    }


# ── VARA (Weekday) ───────────────────────────────────────

VARA_DATA = {
    0: ('Monday', 'Moon', 'Liquidity, silver, FMCG. Moon-ruled day — emotional trading.'),
    1: ('Tuesday', 'Mars', 'Volatility, real estate, defense. Aggressive moves.'),
    2: ('Wednesday', 'Mercury', 'IT, telecom, banking. Communication, fast trades.'),
    3: ('Thursday', 'Jupiter', 'Finance, education, law. Expansion, bullish tendency.'),
    4: ('Friday', 'Venus', 'Luxury, auto, entertainment. Positive, accumulation.'),
    5: ('Saturday', 'Saturn', 'Infrastructure, oil. Slow, heavy, restrictive.'),
    6: ('Sunday', 'Sun', 'Market closed. But astro energy still applies for Monday open.'),
}


def get_vara(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    day_num = dt.weekday()
    name, lord, note = VARA_DATA[day_num]
    return {'name': name, 'lord': lord, 'note': note}


# ── GANDANTA ZONES ────────────────────────────────────────

GANDANTA_JUNCTIONS = [
    (0, 'Pisces→Aries', 'Water→Fire: Emotional to aggressive. Deep karmic transition.'),
    (120, 'Cancer→Leo', 'Water→Fire: Nurturing to authoritative. Policy shifts.'),
    (240, 'Scorpio→Sagittarius', 'Water→Fire: Hidden to expansive. Secrets revealed.'),
]


def check_gandanta(positions):
    """Check if Moon (or any planet) is in Gandanta zone (last 3°20' or first 3°20' of junction)."""
    gandantas = []
    gandanta_range = 3.333  # 3°20'

    for planet_name, data in positions.items():
        deg = data['longitude']
        sign_deg = data['sign_degree']

        for junction_deg, junction_name, note in GANDANTA_JUNCTIONS:
            # Last 3°20' of water sign
            if abs((deg % 360) - junction_deg) < gandanta_range or \
               abs((deg % 360) - (junction_deg + 360)) < gandanta_range:
                if sign_deg >= (30 - gandanta_range) or sign_deg <= gandanta_range:
                    gandantas.append({
                        'planet': planet_name,
                        'junction': junction_name,
                        'sign_degree': data['sign_degree'],
                        'note': note,
                        'severity': 'Exact' if sign_deg >= 29 or sign_deg <= 1 else 'Approaching',
                        'market_impact': 'HIGH — reversals, karmic events' if planet_name == 'Moon' else 'MEDIUM',
                    })

    return gandantas


# ── VOID OF COURSE MOON ──────────────────────────────────

def check_void_of_course(date_str, positions):
    """
    Simplified VOC check: Moon makes no major aspect to any planet
    before leaving current sign. Approximation for daily use.
    """
    moon_deg = positions['Moon']['longitude']
    moon_sign_deg = positions['Moon']['sign_degree']
    moon_speed = abs(positions['Moon']['speed'])

    # Degrees left in current sign
    degrees_left = 30.0 - moon_sign_deg

    # Time to leave sign (hours)
    if moon_speed > 0:
        hours_left = (degrees_left / moon_speed) * 24
    else:
        hours_left = float('inf')

    # Check if Moon will aspect any planet before leaving sign
    # Simplified: if Moon is in last 5° and no planet within aspect range ahead
    is_voc = False
    voc_note = ''

    if moon_sign_deg >= 25:  # Last 5 degrees
        # Check if any planet is in the remaining degrees of this sign
        has_aspect_ahead = False
        for planet_name, pdata in positions.items():
            if planet_name == 'Moon':
                continue
            p_deg = pdata['longitude']
            dist = (p_deg - moon_deg) % 360
            if dist < degrees_left and dist > 0:
                has_aspect_ahead = True
                break

        if not has_aspect_ahead:
            is_voc = True
            voc_note = f'Moon void of course — last {degrees_left:.1f}° in {positions["Moon"]["sign"]}. Market may drift, avoid new entries.'

    return {
        'is_voc': is_voc,
        'degrees_left_in_sign': round(degrees_left, 2),
        'approx_hours_left': round(hours_left, 1) if hours_left != float('inf') else None,
        'note': voc_note,
    }


# ── MOON PHASE ────────────────────────────────────────────

def get_moon_phase(positions):
    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']
    diff = (moon_deg - sun_deg) % 360.0

    if diff < 15:
        phase = 'New Moon (Amavasya zone)'
        note = 'Low energy, reversals possible, avoid big positions'
    elif diff < 90:
        phase = 'Waxing Crescent'
        note = 'Building momentum, cautious buying'
    elif diff < 135:
        phase = 'Waxing Gibbous'
        note = 'Strong momentum, trend continuation likely'
    elif diff < 195:
        phase = 'Full Moon (Purnima zone)'
        note = 'Peak emotion, high volatility, possible reversal'
    elif diff < 270:
        phase = 'Waning Gibbous'
        note = 'Profit booking phase, declining momentum'
    elif diff < 345:
        phase = 'Waning Crescent'
        note = 'Exhaustion, caution, prepare for new cycle'
    else:
        phase = 'New Moon (Amavasya zone)'
        note = 'Low energy, reversals possible, avoid big positions'

    return {'phase': phase, 'sun_moon_distance': round(diff, 2), 'market_note': note}


# ── FULL PANCHANG ─────────────────────────────────────────

def get_full_panchang(date_str, positions=None):
    """Complete Panchang for a date."""
    if positions is None:
        positions = get_planetary_positions(date_str)

    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']

    tithi = get_tithi(moon_deg, sun_deg)
    karana = get_karana(moon_deg, sun_deg)
    nitya_yoga = get_nitya_yoga(moon_deg, sun_deg)
    vara = get_vara(date_str)
    moon_phase = get_moon_phase(positions)
    gandantas = check_gandanta(positions)
    voc = check_void_of_course(date_str, positions)

    # Moon nakshatra
    moon_nak, moon_pada, moon_nak_lord = get_nakshatra(moon_deg)

    return {
        'date': date_str,
        'vara': vara,
        'tithi': tithi,
        'karana': karana,
        'nitya_yoga': nitya_yoga,
        'moon_phase': moon_phase,
        'moon_nakshatra': {'name': moon_nak, 'pada': moon_pada, 'lord': moon_nak_lord},
        'gandantas': gandantas,
        'void_of_course': voc,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📅 FULL PANCHANG — {today}")
    print("=" * 60)

    panchang = get_full_panchang(today)

    v = panchang['vara']
    print(f"\n📆 Vara: {v['name']} (Lord: {v['lord']})")
    print(f"   {v['note']}")

    t = panchang['tithi']
    print(f"\n🌙 Tithi: {t['paksha']} {t['name']} (#{t['number']})")
    print(f"   {t['market_note']}")
    if t['is_critical']:
        print(f"   ⚠️ CRITICAL TITHI — Extra caution!")

    k = panchang['karana']
    print(f"\n🔷 Karana: {k['name']} ({k['nature']})")
    print(f"   {k['note']}")
    if k['is_vishti']:
        print(f"   🚫 VISHTI KARANA (BHADRA) — AVOID new trades!")

    ny = panchang['nitya_yoga']
    print(f"\n⭐ Nitya Yoga: {ny['name']} ({ny['nature']})")
    print(f"   {ny['note']}")
    if ny['is_inauspicious']:
        print(f"   ⚠️ INAUSPICIOUS YOGA — Caution advised!")

    mp = panchang['moon_phase']
    print(f"\n🌗 Moon Phase: {mp['phase']}")
    print(f"   {mp['market_note']}")

    mn = panchang['moon_nakshatra']
    print(f"\n🌟 Moon Nakshatra: {mn['name']} Pada {mn['pada']} (Lord: {mn['lord']})")

    if panchang['gandantas']:
        print(f"\n🔥 GANDANTA ALERTS:")
        for g in panchang['gandantas']:
            print(f"   {g['planet']}: {g['junction']} ({g['severity']})")
            print(f"   {g['note']}")

    voc = panchang['void_of_course']
    if voc['is_voc']:
        print(f"\n🕳️ VOID OF COURSE MOON: {voc['note']}")