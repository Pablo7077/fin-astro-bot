"""
=============================================================
FIN ASTRO BOT v2.0 — Projection Engine
=============================================================
Aggregates ALL signals (astro, panchang, yoga, hora, mundane,
KP, Bradley, Ashtakavarga) into a single projection.
=============================================================
"""

from datetime import datetime
from core.astro_engine import full_astro_analysis
from core.yogas import detect_all_yogas
from core.panchang import get_full_panchang
from core.hora import get_trading_hora_summary
from core.dasha import get_index_dasha
from core.kp_system import get_kp_analysis
from core.sector_map import get_top_sectors
from core.mundane import get_mundane_analysis


def generate_full_projection(target_date=None, symbol='nifty', dataset=None):
    """
    THE MASTER PROJECTION FUNCTION.
    Combines every astrological technique into one report.
    """
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\n{'='*70}")
    print(f"🔮 FIN ASTRO BOT v2.0 — COMPLETE PROJECTION")
    print(f"📅 Date: {target_date}  |  📊 Symbol: {symbol.upper()}")
    print(f"{'='*70}")

    signals = []  # (name, direction, weight, detail)

    # ── 1. PLANETARY POSITIONS + DIGNITY ──────────────────
    analysis = full_astro_analysis(target_date)
    pos = analysis['positions']

    print(f"\n{'─'*50}")
    print(f"📍 PLANETARY POSITIONS (Sidereal/Lahiri)")
    print(f"{'─'*50}")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':16s} {'Dignity':12s} {'R':3s}")
    print(f"{'─'*70}")

    for name, d in pos.items():
        r = '℞' if d['retrograde'] else ''
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:13s} P{d['pada']}  "
              f"{d['dignity']:12s} {r}")

    # Dignity-based signals
    for planet in ['Jupiter', 'Venus', 'Saturn', 'Mars']:
        dignity = pos[planet]['dignity']
        if dignity == 'Exalted':
            bias = 'BULLISH' if planet in ['Jupiter', 'Venus'] else 'VOLATILE'
            signals.append((f'{planet} Exalted', bias, 12, f'{planet} at peak strength'))
        elif dignity == 'Debilitated':
            bias = 'BEARISH' if planet in ['Jupiter', 'Venus'] else 'VOLATILE'
            signals.append((f'{planet} Debilitated', bias, 10, f'{planet} weakened'))

    # ── 2. YOGAS ──────────────────────────────────────────
    yogas = detect_all_yogas(pos)

    if yogas:
        print(f"\n{'─'*50}")
        print(f"⭐ ACTIVE YOGAS ({len(yogas)} found)")
        print(f"{'─'*50}")

        for y in yogas:
            emoji = '🟢' if 'bullish' in y['market_bias'] else (
                '🔴' if 'bearish' in y['market_bias'] else '🟡')
            print(f"  {emoji} {y['name']} [{y['category']}]")
            print(f"    {y['description']}")
            print(f"    Bias: {y['market_bias'].upper()} | Weight: {y['weight']}")

            if 'bullish' in y['market_bias']:
                signals.append((f"Yoga: {y['name']}", 'BULLISH', y['weight'], y['description']))
            elif 'bearish' in y['market_bias']:
                signals.append((f"Yoga: {y['name']}", 'BEARISH', y['weight'], y['description']))
            else:
                signals.append((f"Yoga: {y['name']}", 'VOLATILE', y['weight'] // 2, y['description']))

    # ── 3. PANCHANG ───────────────────────────────────────
    panchang = get_full_panchang(target_date, pos)

    print(f"\n{'─'*50}")
    print(f"📅 PANCHANG")
    print(f"{'─'*50}")

    t = panchang['tithi']
    k = panchang['karana']
    ny = panchang['nitya_yoga']
    v = panchang['vara']
    mp = panchang['moon_phase']

    print(f"  Vara:        {v['name']} (Lord: {v['lord']})")
    print(f"  Tithi:       {t['paksha']} {t['name']} (#{t['number']})")
    print(f"  Karana:      {k['name']} ({k['nature']})")
    print(f"  Nitya Yoga:  {ny['name']} ({ny['nature']})")
    print(f"  Moon Phase:  {mp['phase']}")
    print(f"  Moon Nak:    {panchang['moon_nakshatra']['name']} P{panchang['moon_nakshatra']['pada']}")

    # Panchang signals
    if t['is_critical']:
        signals.append(('Critical Tithi', 'VOLATILE', 15, f"{t['name']} — high risk day"))

    if k['is_vishti']:
        signals.append(('Vishti Karana', 'BEARISH', 18, 'Bhadra Karana — avoid new trades'))

    if ny['is_inauspicious']:
        signals.append(('Bad Nitya Yoga', 'BEARISH', 14, f"{ny['name']} — inauspicious yoga"))
    elif ny['nature'] == 'Shubha':
        signals.append(('Good Nitya Yoga', 'BULLISH', 10, f"{ny['name']} — auspicious yoga"))

    # Moon phase
    if 'New Moon' in mp['phase']:
        signals.append(('New Moon', 'VOLATILE', 12, 'Low energy, potential reversal'))
    elif 'Full Moon' in mp['phase']:
        signals.append(('Full Moon', 'VOLATILE', 12, 'Peak emotion, potential reversal'))
    elif 'Waxing' in mp['phase']:
        signals.append(('Waxing Moon', 'BULLISH', 8, 'Building momentum'))
    elif 'Waning' in mp['phase']:
        signals.append(('Waning Moon', 'BEARISH', 8, 'Declining momentum'))

    # Gandanta
    if panchang['gandantas']:
        for g in panchang['gandantas']:
            if g['planet'] == 'Moon':
                signals.append(('Moon Gandanta', 'VOLATILE', 20, f"Moon at {g['junction']} — extreme karmic zone"))
                print(f"\n  🔥 GANDANTA: Moon at {g['junction']} ({g['severity']})")

    # VOC
    if panchang['void_of_course']['is_voc']:
        signals.append(('Void of Course Moon', 'VOLATILE', 10, 'Market may drift aimlessly'))
        print(f"  🕳️ VOC Moon: {panchang['void_of_course']['note']}")

    # ── 4. HORA TIMING ────────────────────────────────────
    try:
        hora = get_trading_hora_summary(target_date)

        print(f"\n{'─'*50}")
        print(f"⏰ INTRADAY HORA TIMING")
        print(f"{'─'*50}")
        print(f"  Day Ruler: {hora['day_ruler']}")

        for h in hora['market_horas']:
            emoji = '🟢' if h['bias'] == 'bullish' else ('🔴' if h['bias'] == 'bearish' else '🟡')
            print(f"  {h['start']}-{h['end']} {emoji} {h['planet']:10s} {h['action']}")

        print(f"\n  ⚠️ Inauspicious Periods:")
        for name, period in hora['inauspicious'].items():
            if 'rahu' in name or 'abhijit' in name:
                print(f"    {name}: {period['start']}-{period['end']}")

    except Exception as e:
        print(f"  (Hora calculation skipped: {e})")

    # ── 5. SPECIAL EVENTS ─────────────────────────────────
    if analysis['combustions']:
        print(f"\n  🔥 Combustions:")
        for c in analysis['combustions']:
            print(f"    {c['planet']} — {c['severity']} ({c['distance_from_sun']}° from Sun)")

    if analysis['planetary_wars']:
        print(f"\n  ⚔️ Planetary Wars:")
        for w in analysis['planetary_wars']:
            print(f"    {w['planet1']} vs {w['planet2']} — Winner: {w['winner']}")
            signals.append(('Planetary War', 'VOLATILE', 15,
                          f"{w['planet1']} vs {w['planet2']}"))

    if analysis['stations']:
        print(f"\n  🛑 Stations:")
        for s in analysis['stations']:
            print(f"    {s['planet']}: {s['type']}")
            signals.append(('Planet Station', 'VOLATILE', 18,
                          f"{s['planet']} {s['type']}"))

    if analysis['ingresses']:
        print(f"\n  🚀 Sign Changes:")
        for ing in analysis['ingresses']:
            print(f"    {ing['planet']}: {ing['from_sign']} → {ing['to_sign']}")
            signals.append(('Sign Change', 'VOLATILE', 10,
                          f"{ing['planet']} enters {ing['to_sign']}"))

    # ── 6. DASHA (if applicable) ──────────────────────────
    try:
        if symbol.lower() in ['nifty', 'banknifty', 'sensex']:
            dasha = get_index_dasha(symbol.lower(), target_date)
            if dasha['current']:
                maha = dasha['current']['mahadasha']
                antar = dasha['current'].get('antardasha')

                print(f"\n{'─'*50}")
                print(f"🔮 DASHA PERIODS ({symbol.upper()})")
                print(f"{'─'*50}")
                print(f"  Mahadasha: {maha['lord']} "
                      f"({maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')})")
                if antar:
                    print(f"  Antardasha: {antar['antardasha_lord']} "
                          f"({antar['start'].strftime('%Y-%m-%d')} to {antar['end'].strftime('%Y-%m-%d')})")

                interp = maha.get('interpretation', {})
                if interp:
                    overall = interp.get('overall', '')
                    if 'BULLISH' in overall.upper():
                        signals.append(('Mahadasha', 'BULLISH', 15, f"{maha['lord']} Mahadasha — {overall}"))
                    elif 'CHALLENGING' in overall.upper() or 'BEARISH' in overall.upper():
                        signals.append(('Mahadasha', 'BEARISH', 15, f"{maha['lord']} Mahadasha — {overall}"))
    except Exception:
        pass

    # ── 7. KP RULING PLANETS ─────────────────────────────
    try:
        kp = get_kp_analysis(target_date)
        rp = kp['ruling_planets']

        print(f"\n{'─'*50}")
        print(f"🎯 KP RULING PLANETS")
        print(f"{'─'*50}")
        print(f"  Rulers: {', '.join(rp['unique_rulers'])}")
        print(f"  Bullish/Bearish: {rp['bullish_count']}/{rp['bearish_count']}")
        print(f"  Bias: {rp['bias']}")

        if rp['bias'] == 'BULLISH':
            signals.append(('KP Ruling Planets', 'BULLISH', 12, rp['note']))
        elif rp['bias'] == 'BEARISH':
            signals.append(('KP Ruling Planets', 'BEARISH', 12, rp['note']))
    except Exception:
        pass

    # ── 8. MUNDANE TRANSITS ──────────────────────────────
    try:
        if symbol.lower() in ['nifty', 'banknifty', 'sensex']:
            charts = ['nifty', 'india'] if symbol.lower() in ['nifty', 'banknifty'] else ['india']
            mundane = get_mundane_analysis(target_date, charts)

            if mundane['key_aspects']:
                print(f"\n{'─'*50}")
                print(f"🏛️ MUNDANE TRANSIT ASPECTS")
                print(f"{'─'*50}")
                for asp in mundane['key_aspects'][:5]:
                    print(f"  {asp}")

                if mundane['overall_bias'] == 'BULLISH':
                    signals.append(('Mundane Transits', 'BULLISH', 15, f"Score: {mundane['total_score']:+d}"))
                elif mundane['overall_bias'] == 'BEARISH':
                    signals.append(('Mundane Transits', 'BEARISH', 15, f"Score: {mundane['total_score']:+d}"))
    except Exception:
        pass

    # ── 9. HISTORICAL PATTERN MATCHING ────────────────────
    if dataset is not None and not dataset.empty:
        print(f"\n{'─'*50}")
        print(f"📊 HISTORICAL PATTERN MATCHING")
        print(f"{'─'*50}")

        moon_sign = pos['Moon']['sign']
        moon_nak = pos['Moon']['nakshatra']

        # Moon Sign pattern
        if 'Moon_Sign' in dataset.columns:
            moon_data = dataset[dataset['Moon_Sign'] == moon_sign]
            if len(moon_data) >= 10:
                avg_gap = moon_data['Gap_Pct'].mean()
                bullish_pct = (moon_data['Day_Direction'] == 'Bullish').mean() * 100
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                conf = min(abs(bullish_pct - 50) * 1.5, 20)
                signals.append((f'Moon in {moon_sign}', direction, conf,
                              f'{len(moon_data)} days, Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}%'))
                print(f"  Moon in {moon_sign}: {len(moon_data)} days, "
                      f"Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")

        # Moon Nakshatra pattern
        if 'Moon_Nakshatra' in dataset.columns:
            nak_data = dataset[dataset['Moon_Nakshatra'] == moon_nak]
            if len(nak_data) >= 5:
                avg_gap = nak_data['Gap_Pct'].mean()
                bullish_pct = (nak_data['Day_Direction'] == 'Bullish').mean() * 100
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                conf = min(abs(bullish_pct - 50) * 1.5, 18)
                signals.append((f'Moon in {moon_nak}', direction, conf,
                              f'{len(nak_data)} days, Avg Gap: {avg_gap:+.3f}%'))
                print(f"  Moon in {moon_nak}: {len(nak_data)} days, "
                      f"Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")

        # Tithi pattern
        if 'Tithi' in dataset.columns:
            tithi_name = panchang['tithi']['name']
            tithi_data = dataset[dataset['Tithi'] == tithi_name]
            if len(tithi_data) >= 5:
                avg_gap = tithi_data['Gap_Pct'].mean()
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                signals.append((f'Tithi: {tithi_name}', direction, 8,
                              f'Avg Gap: {avg_gap:+.3f}%'))

        # Retrograde count pattern
        if 'Retro_Count' in dataset.columns:
            retro_count = sum(1 for p in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                             if pos[p]['retrograde'])
            rc_data = dataset[dataset['Retro_Count'] == retro_count]
            if len(rc_data) >= 10:
                avg_gap = rc_data['Gap_Pct'].mean()
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                signals.append((f'{retro_count} Retrogrades', direction, 8,
                              f'Avg Gap: {avg_gap:+.3f}%'))

    # ══════════════════════════════════════════════════════
    # SIGNAL AGGREGATION
    # ══════════════════════════════════════════════════════

    print(f"\n{'='*70}")
    print(f"🎯 SIGNAL AGGREGATION ({len(signals)} signals)")
    print(f"{'='*70}")

    bullish_score = sum(w for _, d, w, _ in signals if d == 'BULLISH')
    bearish_score = sum(w for _, d, w, _ in signals if d == 'BEARISH')
    volatile_score = sum(w for _, d, w, _ in signals if d == 'VOLATILE')

    for name, direction, weight, detail in sorted(signals, key=lambda x: x[2], reverse=True):
        emoji = '🟢' if direction == 'BULLISH' else ('🔴' if direction == 'BEARISH' else '🟡')
        print(f"  {emoji} {name:30s} {direction:10s} wt:{weight:3d} | {detail[:50]}")

    total = bullish_score + bearish_score + volatile_score
    if total > 0:
        bull_pct = (bullish_score / total) * 100
        bear_pct = (bearish_score / total) * 100
        vol_pct = (volatile_score / total) * 100
    else:
        bull_pct = bear_pct = vol_pct = 33.3

    print(f"\n  Bullish:  {bullish_score:4d} ({bull_pct:.0f}%)")
    print(f"  Bearish:  {bearish_score:4d} ({bear_pct:.0f}%)")
    print(f"  Volatile: {volatile_score:4d} ({vol_pct:.0f}%)")

    # Final projection
    print(f"\n{'='*70}")

    if bullish_score > bearish_score * 1.3 and bullish_score > volatile_score:
        gap_proj = "📈 GAP UP EXPECTED"
        bias = "BULLISH"
        confidence = min(bull_pct, 75)
    elif bearish_score > bullish_score * 1.3 and bearish_score > volatile_score:
        gap_proj = "📉 GAP DOWN EXPECTED"
        bias = "BEARISH"
        confidence = min(bear_pct, 75)
    elif volatile_score > max(bullish_score, bearish_score):
        gap_proj = "🔀 VOLATILE / FLAT"
        bias = "SIDEWAYS WITH WHIPSAWS"
        confidence = 45
    else:
        gap_proj = "➡️ FLAT / UNCERTAIN"
        bias = "NO CLEAR EDGE"
        confidence = 35

    print(f"  🎯 GAP PROJECTION:    {gap_proj}")
    print(f"  📊 DAY BIAS:          {bias}")
    print(f"  🔮 CONFIDENCE:        ~{confidence:.0f}%")
    print(f"{'='*70}")

    print(f"\n⚠️  DISCLAIMER:")
    print(f"  This is for RESEARCH & EDUCATION only.")
    print(f"  Astro signals are probabilistic, not deterministic.")
    print(f"  Always combine with technical analysis & risk management.")
    print(f"  Never risk capital solely on astrological signals.")

    return {
        'date': target_date,
        'symbol': symbol,
        'gap_projection': gap_proj,
        'bias': bias,
        'confidence': confidence,
        'signals': signals,
        'bullish_score': bullish_score,
        'bearish_score': bearish_score,
        'volatile_score': volatile_score,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    generate_full_projection(today, 'nifty')