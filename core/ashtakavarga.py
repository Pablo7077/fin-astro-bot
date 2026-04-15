"""
=============================================================
FIN ASTRO BOT v2.0 — Ashtakavarga Transit Scoring
=============================================================
Calculates Bindu (point) scores for planetary transits.
Each planet gets 0-8 points per sign based on contributions
from all other planets. Higher score = stronger transit.

Sarvashtakavarga (SAV) = total of all planets' bindus per sign.
=============================================================
"""

from core.astro_engine import get_planetary_positions, SIGNS

# ── Ashtakavarga Bindu Tables ─────────────────────────────
# Format: For each planet, from each contributor planet's position,
# which houses (counted from contributor) give a bindu (point).
# Source: Standard Parashari Ashtakavarga tables

# Houses that give bindu (1-indexed from contributor's sign)
BINDU_TABLES = {
    'Sun': {
        'Sun':     [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon':    [3, 6, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus':   [6, 7, 12],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [3, 4, 6, 10, 11, 12],
    },
    'Moon': {
        'Sun':     [3, 6, 7, 8, 10, 11],
        'Moon':    [1, 3, 6, 7, 10, 11],
        'Mars':    [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus':   [3, 4, 5, 7, 9, 10, 11],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [3, 6, 10, 11],
    },
    'Mars': {
        'Sun':     [3, 5, 6, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus':   [6, 8, 11, 12],
        'Saturn':  [1, 4, 7, 8, 9, 10, 11],
        'Lagna':   [1, 3, 6, 10, 11],
    },
    'Mercury': {
        'Sun':     [5, 6, 9, 11, 12],
        'Moon':    [2, 4, 6, 8, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [1, 2, 4, 6, 8, 10, 11],
    },
    'Jupiter': {
        'Sun':     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon':    [2, 5, 7, 9, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus':   [2, 5, 6, 9, 10, 11],
        'Saturn':  [3, 5, 6, 12],
        'Lagna':   [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    'Venus': {
        'Sun':     [8, 11, 12],
        'Moon':    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars':    [3, 5, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn':  [3, 4, 5, 8, 9, 10, 11],
        'Lagna':   [1, 2, 3, 4, 5, 8, 9, 11],
    },
    'Saturn': {
        'Sun':     [1, 2, 4, 7, 8, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus':   [6, 11, 12],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [1, 3, 4, 6, 10, 11],
    },
}


def calculate_ashtakavarga(positions, lagna_sign_index=None):
    """
    Calculate Ashtakavarga scores for all planets in all signs.
    
    Returns:
        prashtara: Dict of {planet: [score_aries, score_taurus, ...]}
        sarvashtakavarga: [total_aries, total_taurus, ...] (sum of all planets)
    """
    # If no lagna provided, use Aries as reference
    if lagna_sign_index is None:
        lagna_sign_index = 0

    prashtara = {}

    for planet_name in BINDU_TABLES:
        scores = [0] * 12  # One score per sign

        for contributor, bindu_houses in BINDU_TABLES[planet_name].items():
            if contributor == 'Lagna':
                contrib_sign_idx = lagna_sign_index
            elif contributor in positions:
                contrib_sign_idx = positions[contributor]['sign_index']
            else:
                continue

            for house in bindu_houses:
                target_sign = (contrib_sign_idx + house - 1) % 12
                scores[target_sign] += 1

        prashtara[planet_name] = scores

    # Sarvashtakavarga = sum across all planets for each sign
    sav = [0] * 12
    for planet_scores in prashtara.values():
        for i in range(12):
            sav[i] += planet_scores[i]

    return {
        'prashtara': prashtara,
        'sarvashtakavarga': sav,
    }


def get_transit_score(positions, ashtakavarga):
    """
    Score each planet's current transit based on its Ashtakavarga bindus
    in its current sign.
    """
    scores = {}
    prashtara = ashtakavarga['prashtara']

    for planet_name in prashtara:
        if planet_name in positions:
            current_sign_idx = positions[planet_name]['sign_index']
            bindus = prashtara[planet_name][current_sign_idx]

            if bindus >= 5:
                quality = 'STRONG (Bullish)'
                market_note = f'{planet_name} transit supported — positive for its sectors'
            elif bindus >= 4:
                quality = 'MODERATE'
                market_note = f'{planet_name} transit average — mixed results'
            else:
                quality = 'WEAK (Bearish)'
                market_note = f'{planet_name} transit unsupported — negative for its sectors'

            scores[planet_name] = {
                'bindus': bindus,
                'max_possible': 8,
                'quality': quality,
                'current_sign': positions[planet_name]['sign'],
                'market_note': market_note,
            }

    return scores


def get_sav_analysis(sav):
    """Analyze Sarvashtakavarga for overall sign strength."""
    avg = sum(sav) / 12
    analysis = []

    for i, score in enumerate(sav):
        sign = SIGNS[i]
        if score >= 30:
            strength = 'VERY STRONG'
            note = f'Planets transiting {sign} give excellent results'
        elif score >= 27:
            strength = 'STRONG'
            note = f'Planets transiting {sign} give good results'
        elif score >= 24:
            strength = 'AVERAGE'
            note = f'Planets transiting {sign} give mixed results'
        elif score >= 20:
            strength = 'WEAK'
            note = f'Planets transiting {sign} give poor results'
        else:
            strength = 'VERY WEAK'
            note = f'Planets transiting {sign} give negative results'

        analysis.append({
            'sign': sign,
            'score': score,
            'strength': strength,
            'note': note,
        })

    return sorted(analysis, key=lambda x: x['score'], reverse=True)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📊 ASHTAKAVARGA ANALYSIS — {today}")
    print("=" * 65)

    # Get current positions
    positions = get_planetary_positions(today)

    # Calculate Ashtakavarga
    av = calculate_ashtakavarga(positions)

    # Transit scores
    transit_scores = get_transit_score(positions, av)

    print("\n🎯 CURRENT TRANSIT SCORES:")
    print(f"{'Planet':10s} {'Sign':13s} {'Bindus':>7s} {'Quality'}")
    print("-" * 50)
    for planet, data in transit_scores.items():
        emoji = '🟢' if data['bindus'] >= 5 else ('🔴' if data['bindus'] <= 3 else '🟡')
        print(f"{planet:10s} {data['current_sign']:13s} {data['bindus']:4d}/8   "
              f"{emoji} {data['quality']}")

    # SAV Analysis
    print(f"\n📈 SARVASHTAKAVARGA (Sign Strength):")
    print(f"{'Sign':13s} {'Score':>6s} {'Strength'}")
    print("-" * 40)
    sav_analysis = get_sav_analysis(av['sarvashtakavarga'])
    for item in sav_analysis:
        bar = '█' * (item['score'] // 3)
        print(f"{item['sign']:13s} {item['score']:4d}    {item['strength']:12s} {bar}")