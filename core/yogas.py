"""
=============================================================
FIN ASTRO BOT v2.0 — Complete Yoga Detection Engine
=============================================================
20+ Vedic yogas relevant to financial markets.
Each yoga returns market bias + confidence weight.
=============================================================
"""

from core.astro_engine import angular_distance, sign_distance, SIGNS, SIGN_LORDS


def detect_all_yogas(positions, aspects=None):
    """Master function: detect ALL yogas and return list."""
    yogas = []

    yogas += _conjunction_yogas(positions)
    yogas += _solar_yogas(positions)
    yogas += _lunar_yogas(positions)
    yogas += _node_yogas(positions)
    yogas += _strength_yogas(positions)
    yogas += _special_combinations(positions)

    return yogas


# ── 1. CONJUNCTION / ASPECT YOGAS ─────────────────────────

def _conjunction_yogas(pos):
    yogas = []

    # Guru-Chandala: Jupiter + Rahu
    if angular_distance(pos['Jupiter']['longitude'], pos['Rahu']['longitude']) <= 15:
        yogas.append({
            'name': 'Guru-Chandala Yoga',
            'planets': ['Jupiter', 'Rahu'],
            'description': 'Jupiter polluted by Rahu — distorted wisdom, over-speculation',
            'market_bias': 'volatile_bearish',
            'weight': 20,
            'category': 'conjunction',
        })

    # Venus-Jupiter: Wealth combination
    if angular_distance(pos['Venus']['longitude'], pos['Jupiter']['longitude']) <= 10:
        yogas.append({
            'name': 'Venus-Jupiter Conjunction',
            'planets': ['Venus', 'Jupiter'],
            'description': 'Two greatest benefics together — wealth, optimism, bullish sentiment',
            'market_bias': 'bullish',
            'weight': 18,
            'category': 'conjunction',
        })

    # Saturn-Mars: Conflict energy
    sat_mars = angular_distance(pos['Saturn']['longitude'], pos['Mars']['longitude'])
    if sat_mars <= 10:
        yogas.append({
            'name': 'Saturn-Mars Conjunction (Graha Yuddha)',
            'planets': ['Saturn', 'Mars'],
            'description': 'Extreme tension, fear vs aggression — sharp drops, conflict',
            'market_bias': 'bearish',
            'weight': 22,
            'category': 'conjunction',
        })
    elif abs(sat_mars - 180) <= 10:
        yogas.append({
            'name': 'Saturn-Mars Opposition',
            'planets': ['Saturn', 'Mars'],
            'description': 'Push-pull conflict — whipsaw, indecision, eventual breakdown',
            'market_bias': 'volatile_bearish',
            'weight': 18,
            'category': 'conjunction',
        })

    # Chandra-Mangala: Moon-Mars
    if angular_distance(pos['Moon']['longitude'], pos['Mars']['longitude']) <= 10:
        yogas.append({
            'name': 'Chandra-Mangala Yoga',
            'planets': ['Moon', 'Mars'],
            'description': 'Emotional aggression — high volume, impulsive trading, volatility',
            'market_bias': 'volatile',
            'weight': 15,
            'category': 'conjunction',
        })

    # Budha-Aditya: Mercury + Sun (check NOT combust)
    merc_sun = angular_distance(pos['Mercury']['longitude'], pos['Sun']['longitude'])
    if merc_sun <= 10 and merc_sun > 3:  # Close but not too combust
        yogas.append({
            'name': 'Budha-Aditya Yoga',
            'planets': ['Mercury', 'Sun'],
            'description': 'Intelligence + authority — smart money moves, policy clarity',
            'market_bias': 'bullish',
            'weight': 12,
            'category': 'conjunction',
        })

    # Saturn-Jupiter: Policy/expansion cycle
    if angular_distance(pos['Saturn']['longitude'], pos['Jupiter']['longitude']) <= 10:
        yogas.append({
            'name': 'Saturn-Jupiter Conjunction',
            'planets': ['Saturn', 'Jupiter'],
            'description': 'Great Conjunction — new 20-year economic cycle begins',
            'market_bias': 'volatile',
            'weight': 25,
            'category': 'conjunction',
        })

    # Mercury-Venus: Commerce + luxury
    if angular_distance(pos['Mercury']['longitude'], pos['Venus']['longitude']) <= 8:
        yogas.append({
            'name': 'Mercury-Venus Conjunction',
            'planets': ['Mercury', 'Venus'],
            'description': 'Commerce + luxury — consumer spending, retail sector bullish',
            'market_bias': 'bullish',
            'weight': 10,
            'category': 'conjunction',
        })

    return yogas


# ── 2. SOLAR YOGAS (Planets relative to Sun) ─────────────

def _solar_yogas(pos):
    yogas = []
    sun_sign_idx = pos['Sun']['sign_index']
    non_luminaries = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    # Check which planets are in 2nd and 12th from Sun
    planets_in_2nd = []
    planets_in_12th = []
    planets_in_both_sides = False

    for planet in non_luminaries:
        p_sign_idx = pos[planet]['sign_index']
        house_from_sun = ((p_sign_idx - sun_sign_idx) % 12) + 1

        if house_from_sun == 2:
            planets_in_2nd.append(planet)
        elif house_from_sun == 12:
            planets_in_12th.append(planet)

    # Veshi Yoga: Planet in 2nd from Sun
    if planets_in_2nd:
        yogas.append({
            'name': 'Veshi Yoga',
            'planets': ['Sun'] + planets_in_2nd,
            'description': f'{", ".join(planets_in_2nd)} in 2nd from Sun — accumulation phase, market building strength',
            'market_bias': 'bullish',
            'weight': 12,
            'category': 'solar',
        })

    # Vashi Yoga: Planet in 12th from Sun
    if planets_in_12th:
        yogas.append({
            'name': 'Vashi Yoga',
            'planets': ['Sun'] + planets_in_12th,
            'description': f'{", ".join(planets_in_12th)} in 12th from Sun — distribution phase, smart money selling',
            'market_bias': 'bearish',
            'weight': 12,
            'category': 'solar',
        })

    # Ubhayachari Yoga: Planets on BOTH sides of Sun
    if planets_in_2nd and planets_in_12th:
        yogas.append({
            'name': 'Ubhayachari Yoga',
            'planets': ['Sun'] + planets_in_2nd + planets_in_12th,
            'description': 'Sun flanked by planets — strong directional trend, decisive market',
            'market_bias': 'trend_strong',
            'weight': 16,
            'category': 'solar',
        })

    return yogas


# ── 3. LUNAR YOGAS (Planets relative to Moon) ────────────

def _lunar_yogas(pos):
    yogas = []
    moon_sign_idx = pos['Moon']['sign_index']

    # Gaja-Kesari: Jupiter in kendra from Moon (1/4/7/10)
    jup_sign_idx = pos['Jupiter']['sign_index']
    house_diff = ((jup_sign_idx - moon_sign_idx) % 12)
    if house_diff in [0, 3, 6, 9]:
        yogas.append({
            'name': 'Gaja-Kesari Yoga',
            'planets': ['Jupiter', 'Moon'],
            'description': 'Jupiter in kendra from Moon — prosperity, institutional optimism',
            'market_bias': 'bullish',
            'weight': 18,
            'category': 'lunar',
        })

    # Kemadruma Yoga: No planet in 2nd or 12th from Moon
    has_2nd = False
    has_12th = False
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 1:
            has_2nd = True
        elif h == 11:
            has_12th = True

    if not has_2nd and not has_12th:
        yogas.append({
            'name': 'Kemadruma Yoga',
            'planets': ['Moon'],
            'description': 'Moon isolated — no support. Panic, loneliness, sharp drops, lack of buying interest',
            'market_bias': 'bearish',
            'weight': 20,
            'category': 'lunar',
        })

    # Shakata Yoga: Jupiter in 6th or 8th from Moon
    if house_diff in [5, 7]:  # 6th house = index 5, 8th house = index 7
        yogas.append({
            'name': 'Shakata Yoga',
            'planets': ['Jupiter', 'Moon'],
            'description': 'Jupiter in dusthana from Moon — instability, policy shocks, broken promises',
            'market_bias': 'volatile_bearish',
            'weight': 16,
            'category': 'lunar',
        })

    # Amala Yoga: Benefic in 10th from Moon
    benefics = ['Jupiter', 'Venus', 'Mercury']
    for b in benefics:
        b_sign_idx = pos[b]['sign_index']
        h = ((b_sign_idx - moon_sign_idx) % 12)
        if h == 9:  # 10th house = index 9
            yogas.append({
                'name': f'Amala Yoga ({b})',
                'planets': [b, 'Moon'],
                'description': f'{b} in 10th from Moon — clean rally, positive action, institutional buying',
                'market_bias': 'bullish',
                'weight': 14,
                'category': 'lunar',
            })
            break

    # Dur Yoga: Malefic in 10th from Moon
    malefics = ['Saturn', 'Mars']
    for m in malefics:
        m_sign_idx = pos[m]['sign_index']
        h = ((m_sign_idx - moon_sign_idx) % 12)
        if h == 9:
            yogas.append({
                'name': f'Dur Yoga ({m})',
                'planets': [m, 'Moon'],
                'description': f'{m} in 10th from Moon — dirty selloff, negative news driven',
                'market_bias': 'bearish',
                'weight': 14,
                'category': 'lunar',
            })
            break

    # Sunapha: Planet in 2nd from Moon (not Sun)
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 1:
            yogas.append({
                'name': f'Sunapha Yoga ({planet})',
                'planets': [planet, 'Moon'],
                'description': f'{planet} in 2nd from Moon — wealth growth, market support',
                'market_bias': 'bullish',
                'weight': 10,
                'category': 'lunar',
            })
            break

    # Anapha: Planet in 12th from Moon (not Sun)
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 11:
            yogas.append({
                'name': f'Anapha Yoga ({planet})',
                'planets': [planet, 'Moon'],
                'description': f'{planet} in 12th from Moon — past momentum, cautious optimism',
                'market_bias': 'mildly_bullish',
                'weight': 8,
                'category': 'lunar',
            })
            break

    return yogas


# ── 4. NODE YOGAS (Rahu/Ketu) ────────────────────────────

def _node_yogas(pos):
    yogas = []

    rahu_deg = pos['Rahu']['longitude']
    ketu_deg = pos['Ketu']['longitude']
    sun_deg = pos['Sun']['longitude']
    moon_deg = pos['Moon']['longitude']

    # Grahan Yoga (Eclipse-like): Sun/Moon close to Rahu/Ketu
    for node, node_deg in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        for lum, lum_deg in [('Sun', sun_deg), ('Moon', moon_deg)]:
            dist = angular_distance(lum_deg, node_deg)
            if dist <= 12:
                yogas.append({
                    'name': f'Grahan Yoga ({lum}-{node})',
                    'planets': [lum, node],
                    'description': f'{lum} eclipsed by {node} — confusion, fear, sudden reversals',
                    'market_bias': 'volatile',
                    'weight': 20 if dist <= 5 else 12,
                    'category': 'nodal',
                })

    # Kala Sarpa Yoga: All planets on one side of Rahu-Ketu axis
    rahu_idx = pos['Rahu']['sign_index']
    ketu_idx = pos['Ketu']['sign_index']
    all_one_side = True
    side_count = 0
    check_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    for p in check_planets:
        p_idx = pos[p]['sign_index']
        # Check if planet is between Rahu and Ketu (going forward)
        if rahu_idx < ketu_idx:
            between = rahu_idx <= p_idx <= ketu_idx
        else:
            between = p_idx >= rahu_idx or p_idx <= ketu_idx
        if between:
            side_count += 1

    if side_count == len(check_planets) or side_count == 0:
        yogas.append({
            'name': 'Kala Sarpa Yoga',
            'planets': ['Rahu', 'Ketu'] + check_planets,
            'description': 'All planets hemmed by nodes — fatalistic, extreme moves, trapped energy',
            'market_bias': 'volatile_bearish',
            'weight': 25,
            'category': 'nodal',
        })

    return yogas


# ── 5. STRENGTH-BASED YOGAS ──────────────────────────────

def _strength_yogas(pos):
    yogas = []

    # Multiple Retrograde Stress
    retro_planets = [n for n in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                     if pos[n]['retrograde']]
    if len(retro_planets) >= 3:
        yogas.append({
            'name': 'Multiple Retrograde Stress',
            'planets': retro_planets,
            'description': f'{len(retro_planets)} planets retrograde — uncertainty, review, revision mode',
            'market_bias': 'volatile',
            'weight': len(retro_planets) * 5,
            'category': 'strength',
        })

    # Neecha Bhanga Raja Yoga: Debilitated planet with cancellation
    # (Lord of debilitation sign is strong OR lord of exaltation sign aspects)
    for planet_name, data in pos.items():
        if data['dignity'] == 'Debilitated' and planet_name not in ['Rahu', 'Ketu']:
            deb_sign = data['sign']
            deb_lord = SIGN_LORDS.get(deb_sign, '')

            # Check if debilitation lord is exalted or in own sign
            if deb_lord in pos:
                lord_dignity = pos[deb_lord]['dignity']
                if lord_dignity in ['Exalted', 'Own Sign', 'Moolatrikona']:
                    yogas.append({
                        'name': f'Neecha Bhanga Raja Yoga ({planet_name})',
                        'planets': [planet_name, deb_lord],
                        'description': f'{planet_name} debilitated but saved by strong {deb_lord} — beaten-down sectors bounce back strongly',
                        'market_bias': 'bullish',
                        'weight': 18,
                        'category': 'strength',
                    })

    # Exalted benefic = very bullish
    for planet in ['Jupiter', 'Venus']:
        if pos[planet]['dignity'] == 'Exalted':
            yogas.append({
                'name': f'{planet} Exalted',
                'planets': [planet],
                'description': f'{planet} at peak strength — maximum optimism/wealth energy',
                'market_bias': 'bullish',
                'weight': 20,
                'category': 'strength',
            })

    # Debilitated malefic = reduced negative energy = mildly bullish
    for planet in ['Saturn', 'Mars']:
        if pos[planet]['dignity'] == 'Debilitated':
            yogas.append({
                'name': f'{planet} Debilitated',
                'planets': [planet],
                'description': f'{planet} weakened — reduced fear/aggression, but chaotic energy',
                'market_bias': 'volatile',
                'weight': 12,
                'category': 'strength',
            })

    # Exalted malefic = strong negative potential
    for planet in ['Saturn', 'Mars']:
        if pos[planet]['dignity'] == 'Exalted':
            yogas.append({
                'name': f'{planet} Exalted',
                'planets': [planet],
                'description': f'{planet} at peak power — structured but intense pressure on markets',
                'market_bias': 'volatile_bearish' if planet == 'Saturn' else 'volatile',
                'weight': 15,
                'category': 'strength',
            })

    return yogas


# ── 6. SPECIAL COMBINATIONS ──────────────────────────────

def _special_combinations(pos):
    yogas = []

    # Parivartana Yoga (Mutual Exchange)
    checked = set()
    for p1_name, p1_data in pos.items():
        if p1_name in ['Rahu', 'Ketu']:
            continue
        p1_sign = p1_data['sign']
        p1_sign_lord = SIGN_LORDS.get(p1_sign, '')

        if p1_sign_lord in pos and p1_sign_lord not in ['Rahu', 'Ketu']:
            p2_data = pos[p1_sign_lord]
            p2_sign = p2_data['sign']
            p2_sign_lord = SIGN_LORDS.get(p2_sign, '')

            pair = tuple(sorted([p1_name, p1_sign_lord]))
            if p2_sign_lord == p1_name and pair not in checked:
                checked.add(pair)
                yogas.append({
                    'name': f'Parivartana Yoga ({p1_name}-{p1_sign_lord})',
                    'planets': list(pair),
                    'description': f'{pair[0]} and {pair[1]} in mutual exchange — sector rotation, regime change, energy swap',
                    'market_bias': 'volatile',
                    'weight': 16,
                    'category': 'special',
                })

    # All benefics in one sign = massive positivity
    benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
    benefic_signs = [pos[b]['sign'] for b in benefics if b in pos]
    for sign in set(benefic_signs):
        count = benefic_signs.count(sign)
        if count >= 3:
            yogas.append({
                'name': f'Benefic Stellium in {sign}',
                'planets': [b for b in benefics if pos[b]['sign'] == sign],
                'description': f'{count} benefics concentrated in {sign} — extreme optimism, bubble risk',
                'market_bias': 'bullish',
                'weight': 20,
                'category': 'special',
            })

    # All malefics in one sign = concentrated negativity
    malefics_list = ['Saturn', 'Mars', 'Rahu', 'Ketu']
    malefic_signs = [pos[m]['sign'] for m in malefics_list if m in pos]
    for sign in set(malefic_signs):
        count = malefic_signs.count(sign)
        if count >= 3:
            yogas.append({
                'name': f'Malefic Stellium in {sign}',
                'planets': [m for m in malefics_list if pos[m]['sign'] == sign],
                'description': f'{count} malefics concentrated in {sign} — extreme stress sector-specific crash risk',
                'market_bias': 'bearish',
                'weight': 22,
                'category': 'special',
            })

    return yogas


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from core.astro_engine import get_planetary_positions
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n⭐ YOGA DETECTION TEST — {today}")
    print("=" * 60)

    pos = get_planetary_positions(today)
    yogas = detect_all_yogas(pos)

    if yogas:
        for y in yogas:
            emoji = '🟢' if 'bullish' in y['market_bias'] else (
                '🔴' if 'bearish' in y['market_bias'] else '🟡')
            print(f"\n{emoji} {y['name']} [{y['category'].upper()}]")
            print(f"   Planets: {', '.join(y['planets'])}")
            print(f"   {y['description']}")
            print(f"   Market Bias: {y['market_bias'].upper()}, Weight: {y['weight']}")
    else:
        print("No significant yogas detected today.")