"""
=============================================================
FIN ASTRO BOT v2.0 — Divisional Charts (Vargas)
=============================================================
Navamsha (D-9):  Hidden strength of planets. The "confirmation" chart.
Dashamsha (D-10): Career & public status. Directly applicable to indices.
Hora (D-2):      Wealth division — Sun's hora vs Moon's hora.
=============================================================
"""

from core.astro_engine import get_planetary_positions, SIGNS, get_dignity, get_dignity_score, SIGN_LORDS


def calculate_navamsha_sign(longitude):
    """
    Calculate Navamsha (D-9) sign for a given sidereal longitude.
    Each sign is divided into 9 parts of 3°20' each.
    """
    # Each navamsha = 3.3333 degrees
    navamsha_num = int(longitude / (30.0 / 9.0)) % 108
    # Navamsha signs cycle: Aries sign starts from Aries,
    # Taurus from Capricorn, Gemini from Libra, Cancer from Cancer, etc.
    # Simplified: navamsha_num directly maps to sign
    sign_idx = navamsha_num % 12
    return SIGNS[sign_idx], sign_idx


def calculate_dashamsha_sign(longitude):
    """
    Calculate Dashamsha (D-10) sign.
    Each sign is divided into 10 parts of 3° each.
    Odd signs count from same sign, even signs count from 9th sign.
    """
    rashi_num = int(longitude / 30.0) % 12  # 0-indexed
    degrees_in_sign = longitude % 30.0
    dashamsha_part = int(degrees_in_sign / 3.0)  # 0-9

    if rashi_num % 2 == 0:  # Odd signs (0-indexed: Aries=0 is odd sign)
        d10_sign_idx = (rashi_num + dashamsha_part) % 12
    else:  # Even signs
        d10_sign_idx = (rashi_num + 9 + dashamsha_part) % 12

    return SIGNS[d10_sign_idx], d10_sign_idx


def calculate_hora_sign(longitude):
    """
    Calculate Hora (D-2) sign.
    First 15° = Sun's hora (Leo), Last 15° = Moon's hora (Cancer).
    Odd signs: first half = Sun, second half = Moon.
    Even signs: first half = Moon, second half = Sun.
    """
    rashi_num = int(longitude / 30.0) % 12
    degrees_in_sign = longitude % 30.0

    if rashi_num % 2 == 0:  # Odd signs
        if degrees_in_sign < 15:
            return 'Leo', 4  # Sun's hora
        else:
            return 'Cancer', 3  # Moon's hora
    else:  # Even signs
        if degrees_in_sign < 15:
            return 'Cancer', 3  # Moon's hora
        else:
            return 'Leo', 4  # Sun's hora


def get_all_divisional_positions(date_str, time_str='12:00'):
    """Calculate D-1 (Rashi), D-2 (Hora), D-9 (Navamsha), D-10 (Dashamsha) for all planets."""
    positions = get_planetary_positions(date_str, time_str)
    divisional = {}

    for name, data in positions.items():
        long = data['longitude']

        # Navamsha (D-9)
        nav_sign, nav_idx = calculate_navamsha_sign(long)
        nav_dignity = get_dignity(name, nav_sign, (long % (30.0/9.0)) * 9)

        # Dashamsha (D-10)
        d10_sign, d10_idx = calculate_dashamsha_sign(long)
        d10_dignity = get_dignity(name, d10_sign, (long % 3.0) * 10)

        # Hora (D-2)
        hora_sign, hora_idx = calculate_hora_sign(long)

        # Vargottama check: same sign in D-1 and D-9
        is_vargottama = data['sign'] == nav_sign

        divisional[name] = {
            # D-1 (Rashi)
            'rashi_sign': data['sign'],
            'rashi_dignity': data['dignity'],
            'rashi_score': data['dignity_score'],

            # D-9 (Navamsha)
            'navamsha_sign': nav_sign,
            'navamsha_dignity': nav_dignity,
            'navamsha_score': get_dignity_score(nav_dignity),

            # D-10 (Dashamsha)
            'dashamsha_sign': d10_sign,
            'dashamsha_dignity': d10_dignity,
            'dashamsha_score': get_dignity_score(d10_dignity),

            # D-2 (Hora)
            'hora_sign': hora_sign,
            'hora_type': 'Sun (Gold/Authority)' if hora_sign == 'Leo' else 'Moon (Silver/Liquidity)',

            # Special
            'is_vargottama': is_vargottama,

            # Composite strength (D1 + D9 weighted)
            'composite_strength': round(
                data['dignity_score'] * 0.6 + get_dignity_score(nav_dignity) * 0.4, 2
            ),
        }

    return divisional


def get_vargottama_planets(divisional_data):
    """Find planets that are Vargottama (same sign in D-1 and D-9) — very strong."""
    return [name for name, data in divisional_data.items() if data['is_vargottama']]


def get_composite_strength_ranking(divisional_data):
    """Rank planets by composite strength (D-1 + D-9)."""
    ranking = []
    for name, data in divisional_data.items():
        ranking.append({
            'planet': name,
            'rashi': f"{data['rashi_sign']} ({data['rashi_dignity']})",
            'navamsha': f"{data['navamsha_sign']} ({data['navamsha_dignity']})",
            'composite': data['composite_strength'],
            'vargottama': data['is_vargottama'],
        })
    return sorted(ranking, key=lambda x: x['composite'], reverse=True)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📐 DIVISIONAL CHARTS — {today}")
    print("=" * 80)

    div = get_all_divisional_positions(today)

    print(f"\n{'Planet':10s} {'Rashi(D1)':16s} {'Navamsha(D9)':16s} {'Dashams(D10)':16s} {'Hora':12s} {'VG':4s} {'Str':>5s}")
    print("-" * 85)
    for name, data in div.items():
        vg = '✅' if data['is_vargottama'] else ''
        print(f"{name:10s} {data['rashi_sign']:8s}({data['rashi_dignity'][:4]:4s}) "
              f"{data['navamsha_sign']:8s}({data['navamsha_dignity'][:4]:4s}) "
              f"{data['dashamsha_sign']:8s}({data['dashamsha_dignity'][:4]:4s}) "
              f"{data['hora_type'][:10]:12s} {vg:4s} {data['composite_strength']:5.2f}")

    vg_planets = get_vargottama_planets(div)
    if vg_planets:
        print(f"\n⭐ VARGOTTAMA PLANETS (Extra Strong): {', '.join(vg_planets)}")

    print(f"\n📊 COMPOSITE STRENGTH RANKING:")
    ranking = get_composite_strength_ranking(div)
    for r in ranking:
        emoji = '💪' if r['composite'] >= 3 else ('😐' if r['composite'] >= 0 else '😰')
        print(f"  {emoji} {r['planet']:10s} → {r['composite']:+.2f} "
              f"| D1: {r['rashi']:22s} | D9: {r['navamsha']}")