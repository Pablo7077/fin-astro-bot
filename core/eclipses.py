"""
=============================================================
FIN ASTRO BOT v2.0 — Eclipse Detection & Corridor Analysis
=============================================================
Detects solar/lunar eclipses, eclipse seasons (corridors),
and their market impact windows.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
from core.astro_engine import date_to_jd, get_planetary_positions, angular_distance
import os

EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)


def find_eclipses_in_range(start_date, end_date):
    """Find all solar and lunar eclipses in a date range."""
    eclipses = []

    start_jd = date_to_jd(start_date)
    end_jd = date_to_jd(end_date)

    # Find solar eclipses
    jd = start_jd
    while jd < end_jd:
        try:
            result = swe.sol_eclipse_when_glob(jd, swe.FLG_SWIEPH)
            eclipse_jd = result[1][0]

            if eclipse_jd > end_jd:
                break

            # Get date
            utc = swe.jdut1_to_utc(eclipse_jd, 1)
            date = f"{int(utc[0])}-{int(utc[1]):02d}-{int(utc[2]):02d}"

            eclipse_type = 'Total Solar' if result[0] & swe.SE_ECL_TOTAL else \
                          'Annular Solar' if result[0] & swe.SE_ECL_ANNULAR else \
                          'Partial Solar'

            eclipses.append({
                'type': eclipse_type,
                'date': date,
                'jd': eclipse_jd,
                'category': 'solar',
                'market_impact': _get_eclipse_market_impact(eclipse_type),
            })

            jd = eclipse_jd + 25  # Jump ahead to find next
        except Exception:
            jd += 30
            continue

    # Find lunar eclipses
    jd = start_jd
    while jd < end_jd:
        try:
            result = swe.lun_eclipse_when(jd, swe.FLG_SWIEPH)
            eclipse_jd = result[1][0]

            if eclipse_jd > end_jd:
                break

            utc = swe.jdut1_to_utc(eclipse_jd, 1)
            date = f"{int(utc[0])}-{int(utc[1]):02d}-{int(utc[2]):02d}"

            eclipse_type = 'Total Lunar' if result[0] & swe.SE_ECL_TOTAL else \
                          'Partial Lunar' if result[0] & swe.SE_ECL_PARTIAL else \
                          'Penumbral Lunar'

            eclipses.append({
                'type': eclipse_type,
                'date': date,
                'jd': eclipse_jd,
                'category': 'lunar',
                'market_impact': _get_eclipse_market_impact(eclipse_type),
            })

            jd = eclipse_jd + 25
        except Exception:
            jd += 30
            continue

    return sorted(eclipses, key=lambda x: x['jd'])


def _get_eclipse_market_impact(eclipse_type):
    impacts = {
        'Total Solar': {
            'severity': 'EXTREME',
            'pre_days': 7,
            'post_days': 30,
            'note': 'Total Solar Eclipse: Maximum disruption. Markets typically sell off 5-7 days before. Effect lasts ~1 month. Government/policy changes likely.'
        },
        'Annular Solar': {
            'severity': 'HIGH',
            'pre_days': 5,
            'post_days': 21,
            'note': 'Annular Solar Eclipse: Strong disruption. Markets volatile. Ring of fire = hidden power shifts.'
        },
        'Partial Solar': {
            'severity': 'MODERATE',
            'pre_days': 3,
            'post_days': 14,
            'note': 'Partial Solar Eclipse: Moderate disruption. Specific sectors affected based on sign.'
        },
        'Total Lunar': {
            'severity': 'HIGH',
            'pre_days': 3,
            'post_days': 14,
            'note': 'Total Lunar Eclipse (Blood Moon): Emotional peak. Mass psychology reversal. Full Moon energy amplified.'
        },
        'Partial Lunar': {
            'severity': 'MODERATE',
            'pre_days': 2,
            'post_days': 7,
            'note': 'Partial Lunar Eclipse: Emotional disturbance. Sentiment shifts.'
        },
        'Penumbral Lunar': {
            'severity': 'LOW',
            'pre_days': 1,
            'post_days': 3,
            'note': 'Penumbral Lunar Eclipse: Subtle emotional undercurrent. Minor market impact.'
        },
    }
    return impacts.get(eclipse_type, {
        'severity': 'UNKNOWN', 'pre_days': 3, 'post_days': 7, 'note': 'Eclipse detected.'
    })


def check_eclipse_corridor(date_str, eclipses=None):
    """
    Check if a date falls within an eclipse corridor
    (the ~35-day window between consecutive eclipses).
    This is historically the MOST volatile period.
    """
    if eclipses is None:
        # Look within +/- 6 months
        start = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=180)).strftime('%Y-%m-%d')
        end = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=180)).strftime('%Y-%m-%d')
        eclipses = find_eclipses_in_range(start, end)

    target = datetime.strptime(date_str, '%Y-%m-%d')
    in_corridor = False
    corridor_info = None

    for i in range(len(eclipses) - 1):
        e1_date = datetime.strptime(eclipses[i]['date'], '%Y-%m-%d')
        e2_date = datetime.strptime(eclipses[i + 1]['date'], '%Y-%m-%d')

        gap = (e2_date - e1_date).days

        if gap <= 40 and e1_date <= target <= e2_date:
            in_corridor = True
            corridor_info = {
                'eclipse_1': eclipses[i],
                'eclipse_2': eclipses[i + 1],
                'corridor_days': gap,
                'day_in_corridor': (target - e1_date).days,
                'note': '⚠️ IN ECLIPSE CORRIDOR: Historically the most volatile period. '
                        'Expect large swings, reversals, and unexpected news.'
            }
            break

    # Also check if near a single eclipse
    nearest = None
    min_distance = float('inf')
    for e in eclipses:
        e_date = datetime.strptime(e['date'], '%Y-%m-%d')
        distance = abs((target - e_date).days)
        if distance < min_distance:
            min_distance = distance
            nearest = e

    return {
        'in_corridor': in_corridor,
        'corridor_info': corridor_info,
        'nearest_eclipse': nearest,
        'days_to_nearest': min_distance if nearest else None,
    }


def get_eclipse_analysis(date_str):
    """Full eclipse analysis for a date."""
    # Get eclipses for current year
    year = date_str[:4]
    eclipses = find_eclipses_in_range(f'{year}-01-01', f'{year}-12-31')
    corridor = check_eclipse_corridor(date_str, eclipses)

    return {
        'date': date_str,
        'year_eclipses': eclipses,
        'corridor': corridor,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    year = today[:4]
    print(f"\n🌑 ECLIPSE ANALYSIS — {year}")
    print("=" * 65)

    analysis = get_eclipse_analysis(today)

    print(f"\n🔭 ECLIPSES IN {year}:")
    for e in analysis['year_eclipses']:
        print(f"  {e['date']}: {e['type']} [{e['market_impact']['severity']}]")

    corridor = analysis['corridor']
    if corridor['in_corridor']:
        print(f"\n⚠️ {corridor['corridor_info']['note']}")
    elif corridor['nearest_eclipse']:
        print(f"\n📅 Nearest eclipse: {corridor['nearest_eclipse']['date']} "
              f"({corridor['nearest_eclipse']['type']})")
        print(f"   Distance: {corridor['days_to_nearest']} days")