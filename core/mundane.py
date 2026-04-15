"""
=============================================================
FIN ASTRO BOT v2.0 — Mundane Astrology (Nation/Index Charts)
=============================================================
Transits to India's independence chart and Nifty's birth chart.
The backbone of macro-level market forecasting.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, angular_distance, get_sign,
    get_nakshatra, SIGNS
)
from datetime import datetime


# ── Birth Chart Data ──────────────────────────────────────

INDIA_CHART = {
    'name': 'India Independence',
    'date': '1947-08-15',
    'time': '00:00',
    'place': 'Delhi',
    'lat': 28.6139, 'lon': 77.2090,
    'description': 'India\'s independence. Transits to this chart affect national policy, economy, and markets.'
}

NIFTY_CHART = {
    'name': 'Nifty 50 (NSE)',
    'date': '1995-11-03',
    'time': '09:55',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'NSE Nifty 50 launch. The "birth chart" of India\'s primary index.'
}

BANKNIFTY_CHART = {
    'name': 'Bank Nifty',
    'date': '2005-06-13',
    'time': '09:15',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'Bank Nifty launch. Represents Indian banking sector.'
}

SENSEX_CHART = {
    'name': 'BSE Sensex',
    'date': '1986-01-02',
    'time': '10:00',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'BSE Sensex base date. India\'s oldest major index.'
}

BITCOIN_CHART = {
    'name': 'Bitcoin',
    'date': '2009-01-03',
    'time': '18:15',  # Genesis block approximate
    'place': 'Global',
    'lat': 0.0, 'lon': 0.0,
    'description': 'Bitcoin genesis block. Reference chart for crypto.'
}

ALL_CHARTS = {
    'india': INDIA_CHART,
    'nifty': NIFTY_CHART,
    'banknifty': BANKNIFTY_CHART,
    'sensex': SENSEX_CHART,
    'bitcoin': BITCOIN_CHART,
}


def get_natal_positions(chart_name='nifty'):
    """Get planetary positions at birth of an entity."""
    chart = ALL_CHARTS.get(chart_name.lower(), NIFTY_CHART)
    return get_planetary_positions(chart['date'], chart['time'])


def transit_to_natal_aspects(transit_date, chart_name='nifty'):
    """
    Calculate aspects between current transiting planets
    and natal chart positions.
    """
    chart = ALL_CHARTS.get(chart_name.lower(), NIFTY_CHART)
    natal = get_planetary_positions(chart['date'], chart['time'])
    transit = get_planetary_positions(transit_date)

    aspects = []
    aspect_types = {
        0: ('Conjunction', 8), 60: ('Sextile', 5),
        90: ('Square', 6), 120: ('Trine', 6), 180: ('Opposition', 8),
    }

    # Key transit-to-natal combinations
    key_transits = {
        ('Jupiter', 'Moon'): ('Jupiter transit to natal Moon — MOST bullish. Major rallies.', 25),
        ('Jupiter', 'Sun'): ('Jupiter transit to natal Sun — Authority boosted. Policy positive.', 20),
        ('Saturn', 'Moon'): ('Saturn transit to natal Moon — Sade Sati pressure. Corrections.', -25),
        ('Saturn', 'Sun'): ('Saturn transit to natal Sun — Government pressure, restrictions.', -20),
        ('Rahu', 'Moon'): ('Rahu transit to natal Moon — Speculation frenzy, then crash.', -15),
        ('Rahu', 'Jupiter'): ('Rahu transit to natal Jupiter — Distorted growth, bubble.', -10),
        ('Mars', 'Saturn'): ('Mars transit to natal Saturn — Accidents, sharp drops.', -18),
        ('Venus', 'Jupiter'): ('Venus transit to natal Jupiter — Wealth flows, prosperity.', 15),
    }

    important_transit_planets = ['Jupiter', 'Saturn', 'Rahu', 'Mars', 'Venus']
    important_natal_planets = ['Sun', 'Moon', 'Mercury', 'Jupiter', 'Saturn', 'Rahu']

    for t_name in important_transit_planets:
        for n_name in important_natal_planets:
            if t_name not in transit or n_name not in natal:
                continue

            t_deg = transit[t_name]['longitude']
            n_deg = natal[n_name]['longitude']
            dist = angular_distance(t_deg, n_deg)

            for exact_deg, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_deg) <= orb:
                    pair = (t_name, n_name)
                    interp = key_transits.get(pair, (f'{t_name} {aspect_name} natal {n_name}', 0))

                    is_bullish = interp[1] > 0
                    is_tight = abs(dist - exact_deg) <= 2

                    aspects.append({
                        'transit_planet': t_name,
                        'natal_planet': n_name,
                        'aspect': aspect_name,
                        'orb': round(abs(dist - exact_deg), 2),
                        'tight': is_tight,
                        'interpretation': interp[0],
                        'score': interp[1],
                        'bias': 'bullish' if is_bullish else 'bearish',
                    })

    return {
        'chart': chart['name'],
        'transit_date': transit_date,
        'aspects': sorted(aspects, key=lambda x: abs(x['score']), reverse=True),
    }


def get_mundane_analysis(transit_date, charts=None):
    """Get transit analysis for all relevant charts."""
    if charts is None:
        charts = ['nifty', 'india']

    results = {}
    for chart_name in charts:
        results[chart_name] = transit_to_natal_aspects(transit_date, chart_name)

    # Aggregate scores
    total_score = 0
    key_aspects = []
    for chart_name, data in results.items():
        for aspect in data['aspects']:
            if aspect['tight']:
                total_score += aspect['score']
                key_aspects.append(f"[{chart_name.upper()}] {aspect['interpretation']}")

    overall = 'BULLISH' if total_score > 10 else ('BEARISH' if total_score < -10 else 'NEUTRAL')

    return {
        'date': transit_date,
        'chart_analyses': results,
        'total_score': total_score,
        'overall_bias': overall,
        'key_aspects': key_aspects,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🏛️ MUNDANE ASTROLOGY — {today}")
    print("=" * 65)

    analysis = get_mundane_analysis(today)

    for chart_name, data in analysis['chart_analyses'].items():
        print(f"\n📋 TRANSITS TO {data['chart'].upper()}:")
        if data['aspects']:
            for a in data['aspects'][:5]:
                emoji = '🟢' if a['bias'] == 'bullish' else '🔴'
                tight_mark = '🎯' if a['tight'] else ''
                print(f"  {emoji} Transit {a['transit_planet']} {a['aspect']} "
                      f"Natal {a['natal_planet']} (orb: {a['orb']}°) {tight_mark}")
                print(f"     {a['interpretation']}")
        else:
            print("  No major transit aspects active.")

    print(f"\n📊 OVERALL MUNDANE SCORE: {analysis['total_score']:+d}")
    print(f"📈 BIAS: {analysis['overall_bias']}")