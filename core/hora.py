"""
=============================================================
FIN ASTRO BOT v2.0 — Planetary Hours (Hora) & Rahu Kaal
=============================================================
Calculates which planet rules each hour of the trading day.
THE #1 intraday timing tool in financial astrology.
=============================================================
"""

from datetime import datetime, timedelta
import swisseph as swe
from core.astro_engine import date_to_jd
import math

# ── Constants ─────────────────────────────────────────────

# Planetary hour sequence (Chaldean order)
HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']

# Day rulers (which planet starts the hora sequence)
DAY_RULERS = {
    0: 'Moon',      # Monday
    1: 'Mars',      # Tuesday
    2: 'Mercury',   # Wednesday
    3: 'Jupiter',   # Thursday
    4: 'Venus',     # Friday
    5: 'Saturn',    # Saturday
    6: 'Sun',       # Sunday
}

# Market interpretation of each hora
HORA_MARKET_EFFECT = {
    'Sun': {
        'bias': 'bullish',
        'note': 'Authority, government orders, power stocks. Strong directional move.',
        'sectors': ['Power', 'Pharma', 'Government PSUs'],
        'action': 'Good for trend trades',
    },
    'Moon': {
        'bias': 'volatile',
        'note': 'Emotional trading, liquidity moves, sentiment shifts.',
        'sectors': ['FMCG', 'Silver', 'Hospitality'],
        'action': 'Watch for sentiment reversals',
    },
    'Mars': {
        'bias': 'volatile',
        'note': 'Aggressive moves, breakouts/breakdowns, high volume spikes.',
        'sectors': ['Real Estate', 'Defense', 'Steel', 'Energy'],
        'action': '⚠️ Quick scalps only. Set tight stops.',
    },
    'Mercury': {
        'bias': 'neutral',
        'note': 'Communication, data, fast trades. Good for IT/banking.',
        'sectors': ['IT', 'Telecom', 'Banking (trading)'],
        'action': 'Good for quick in-out trades',
    },
    'Jupiter': {
        'bias': 'bullish',
        'note': '🟢 BEST hora for buying. Optimism, expansion, institutional flow.',
        'sectors': ['Banking (investment)', 'Finance', 'Education'],
        'action': '✅ BEST TIME TO BUY. Accumulate.',
    },
    'Venus': {
        'bias': 'bullish',
        'note': 'Luxury, comfort, steady gains. Good for accumulation.',
        'sectors': ['Auto', 'Luxury', 'Entertainment', 'Sugar'],
        'action': 'Good for buying, especially value stocks',
    },
    'Saturn': {
        'bias': 'bearish',
        'note': '🔴 CAUTION hora. Slow, heavy, restrictive. Profit booking time.',
        'sectors': ['Infrastructure', 'Mining', 'Oil & Gas'],
        'action': '⚠️ AVOID new buys. Book profits. Bears active.',
    },
}

# Rahu Kaal timings per weekday (based on sunrise division)
# Format: (start_segment, end_segment) — each day is divided into 8 segments
RAHU_KAAL_SEGMENTS = {
    0: (2, 3),    # Monday: 2nd segment
    1: (7, 8),    # Tuesday: 8th segment
    2: (5, 6),    # Wednesday: 6th segment
    3: (4, 5),    # Thursday: 5th segment
    4: (3, 4),    # Friday: 4th segment
    5: (1, 2),    # Saturday: 2nd segment
    6: (6, 7),    # Sunday: 7th segment
}

GULIKA_SEGMENTS = {
    0: (6, 7),    # Monday
    1: (5, 6),    # Tuesday
    2: (4, 5),    # Wednesday
    3: (3, 4),    # Thursday
    4: (2, 3),    # Friday
    5: (1, 2),    # Saturday
    6: (0, 1),    # Sunday
}

YAMAGANDA_SEGMENTS = {
    0: (4, 5),    # Monday
    1: (3, 4),    # Tuesday
    2: (2, 3),    # Wednesday
    3: (1, 2),    # Thursday
    4: (0, 1),    # Friday
    5: (6, 7),    # Saturday
    6: (5, 6),    # Sunday
}


# ── Sunrise / Sunset ─────────────────────────────────────

def get_sunrise_sunset(date_str, lat=19.0760, lon=72.8777):
    """
    Calculate sunrise and sunset for Mumbai (NSE location).
    Returns times in IST.
    """
    jd = date_to_jd(date_str, '12:00')

    # Swiss Ephemeris sunrise
    try:
        result_rise = swe.rise_trans(
            jd, swe.SUN, lon, lat, 0.0, 0.0,
            swe.CALC_RISE | swe.BIT_DISC_CENTER
        )
        result_set = swe.rise_trans(
            jd, swe.SUN, lon, lat, 0.0, 0.0,
            swe.CALC_SET | swe.BIT_DISC_CENTER
        )

        sunrise_jd = result_rise[1][0]
        sunset_jd = result_set[1][0]

        # Convert JD to datetime (already in UT, add 5:30 for IST)
        sunrise_ut = swe.jdut1_to_utc(sunrise_jd, 1)
        sunset_ut = swe.jdut1_to_utc(sunset_jd, 1)

        ist_offset = timedelta(hours=5, minutes=30)

        sunrise = datetime(int(sunrise_ut[0]), int(sunrise_ut[1]),
                          int(sunrise_ut[2]), int(sunrise_ut[3]),
                          int(sunrise_ut[4]), int(sunrise_ut[5])) + ist_offset
        sunset = datetime(int(sunset_ut[0]), int(sunset_ut[1]),
                         int(sunset_ut[2]), int(sunset_ut[3]),
                         int(sunset_ut[4]), int(sunset_ut[5])) + ist_offset

        return sunrise, sunset

    except Exception:
        # Fallback: approximate for Mumbai
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        sunrise = dt.replace(hour=6, minute=15)
        sunset = dt.replace(hour=18, minute=30)
        return sunrise, sunset


# ── Planetary Hours Calculation ───────────────────────────

def get_planetary_hours(date_str, market_start='09:15', market_end='15:30'):
    """
    Calculate planetary hours for the trading day.
    Returns hora table for market hours.
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    weekday = dt.weekday()
    day_ruler = DAY_RULERS[weekday]

    sunrise, sunset = get_sunrise_sunset(date_str)

    # Day duration and night duration
    day_length = (sunset - sunrise).total_seconds()
    night_length = 86400 - day_length  # 24 hours - day

    # Each day hora = day_length / 12
    day_hora_seconds = day_length / 12.0
    night_hora_seconds = night_length / 12.0

    # Find starting planet index
    start_idx = HORA_SEQUENCE.index(day_ruler)

    # Generate all 24 horas
    all_horas = []
    current_time = sunrise

    for i in range(24):
        planet_idx = (start_idx + i) % 7
        planet = HORA_SEQUENCE[planet_idx]

        if i < 12:
            duration = timedelta(seconds=day_hora_seconds)
        else:
            duration = timedelta(seconds=night_hora_seconds)

        end_time = current_time + duration

        all_horas.append({
            'hora_number': i + 1,
            'planet': planet,
            'start': current_time,
            'end': end_time,
            'is_day': i < 12,
        })

        current_time = end_time

    # Filter for market hours
    mkt_start = datetime.strptime(f"{date_str} {market_start}", "%Y-%m-%d %H:%M")
    mkt_end = datetime.strptime(f"{date_str} {market_end}", "%Y-%m-%d %H:%M")

    market_horas = []
    for hora in all_horas:
        # Check overlap with market hours
        overlap_start = max(hora['start'], mkt_start)
        overlap_end = min(hora['end'], mkt_end)

        if overlap_start < overlap_end:
            effect = HORA_MARKET_EFFECT.get(hora['planet'], {})
            market_horas.append({
                'planet': hora['planet'],
                'start': overlap_start.strftime('%H:%M'),
                'end': overlap_end.strftime('%H:%M'),
                'duration_min': round((overlap_end - overlap_start).total_seconds() / 60),
                'bias': effect.get('bias', 'neutral'),
                'note': effect.get('note', ''),
                'sectors': effect.get('sectors', []),
                'action': effect.get('action', ''),
            })

    return {
        'date': date_str,
        'weekday': dt.strftime('%A'),
        'day_ruler': day_ruler,
        'sunrise': sunrise.strftime('%H:%M'),
        'sunset': sunset.strftime('%H:%M'),
        'market_horas': market_horas,
    }


# ── Rahu Kaal & Inauspicious Periods ─────────────────────

def get_inauspicious_periods(date_str):
    """Calculate Rahu Kaal, Gulika, and Yamaganda for the day."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    weekday = dt.weekday()
    sunrise, sunset = get_sunrise_sunset(date_str)

    day_length = (sunset - sunrise).total_seconds()
    segment_duration = timedelta(seconds=day_length / 8.0)

    periods = {}

    # Rahu Kaal
    rk_start_seg, rk_end_seg = RAHU_KAAL_SEGMENTS[weekday]
    rk_start = sunrise + segment_duration * rk_start_seg
    rk_end = sunrise + segment_duration * rk_end_seg
    periods['rahu_kaal'] = {
        'start': rk_start.strftime('%H:%M'),
        'end': rk_end.strftime('%H:%M'),
        'note': '⚠️ RAHU KAAL: Avoid new trades. Fake moves & traps common. Wait it out.',
        'duration_min': round((rk_end - rk_start).total_seconds() / 60),
    }

    # Gulika Kaal
    gk_start_seg, gk_end_seg = GULIKA_SEGMENTS[weekday]
    gk_start = sunrise + segment_duration * gk_start_seg
    gk_end = sunrise + segment_duration * gk_end_seg
    periods['gulika_kaal'] = {
        'start': gk_start.strftime('%H:%M'),
        'end': gk_end.strftime('%H:%M'),
        'note': 'Gulika Kaal: Subtle negative energy. Not ideal for new positions.',
        'duration_min': round((gk_end - gk_start).total_seconds() / 60),
    }

    # Yamaganda
    yk_start_seg, yk_end_seg = YAMAGANDA_SEGMENTS[weekday]
    yk_start = sunrise + segment_duration * yk_start_seg
    yk_end = sunrise + segment_duration * yk_end_seg
    periods['yamaganda'] = {
        'start': yk_start.strftime('%H:%M'),
        'end': yk_end.strftime('%H:%M'),
        'note': 'Yamaganda: Death-like stagnation. Markets may go completely flat.',
        'duration_min': round((yk_end - yk_start).total_seconds() / 60),
    }

    # Abhijit Muhurta (midday, ~24 min window around solar noon)
    solar_noon = sunrise + timedelta(seconds=day_length / 2)
    abhijit_start = solar_noon - timedelta(minutes=12)
    abhijit_end = solar_noon + timedelta(minutes=12)
    periods['abhijit_muhurta'] = {
        'start': abhijit_start.strftime('%H:%M'),
        'end': abhijit_end.strftime('%H:%M'),
        'note': '✅ ABHIJIT MUHURTA: Most auspicious 24 min of the day. Best for important trades.',
        'duration_min': 24,
    }

    return periods


# ── Hora Summary for Trading ─────────────────────────────

def get_trading_hora_summary(date_str):
    """Combined hora + inauspicious periods for complete intraday guide."""
    horas = get_planetary_hours(date_str)
    bad_periods = get_inauspicious_periods(date_str)

    # Find best and worst windows
    best_windows = [h for h in horas['market_horas']
                    if h['planet'] in ['Jupiter', 'Venus']]
    worst_windows = [h for h in horas['market_horas']
                     if h['planet'] in ['Saturn', 'Mars']]

    return {
        **horas,
        'inauspicious': bad_periods,
        'best_buy_windows': best_windows,
        'caution_windows': worst_windows,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n⏰ PLANETARY HOURS & TIMING — {today}")
    print("=" * 70)

    summary = get_trading_hora_summary(today)

    print(f"\n📅 {summary['weekday']} | Day Ruler: {summary['day_ruler']}")
    print(f"🌅 Sunrise: {summary['sunrise']} | 🌇 Sunset: {summary['sunset']}")

    print(f"\n📊 MARKET HORA TABLE (9:15 AM - 3:30 PM):")
    print(f"{'Time':15s} {'Planet':10s} {'Bias':10s} {'Action'}")
    print("-" * 70)
    for h in summary['market_horas']:
        emoji = '🟢' if h['bias'] == 'bullish' else (
            '🔴' if h['bias'] == 'bearish' else '🟡')
        print(f"{h['start']}-{h['end']}    {emoji} {h['planet']:10s} "
              f"{h['bias']:10s} {h['action']}")

    print(f"\n⚠️ INAUSPICIOUS PERIODS:")
    for name, period in summary['inauspicious'].items():
        print(f"  {name:20s}: {period['start']} - {period['end']} "
              f"({period['duration_min']} min)")

    if summary['best_buy_windows']:
        print(f"\n✅ BEST BUY WINDOWS:")
        for w in summary['best_buy_windows']:
            print(f"  {w['start']}-{w['end']} ({w['planet']} hora)")

    if summary['caution_windows']:
        print(f"\n🔴 CAUTION WINDOWS:")
        for w in summary['caution_windows']:
            print(f"  {w['start']}-{w['end']} ({w['planet']} hora)")