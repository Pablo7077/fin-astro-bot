"""
=============================================================
FIN ASTRO BOT v2.0 — Monthly Report Generator
=============================================================
"""

import os
from datetime import datetime, timedelta
import calendar
from core.astro_engine import full_astro_analysis
from core.yogas import detect_all_yogas
from core.panchang import get_full_panchang
from core.eclipses import get_eclipse_analysis
from core.dasha import get_index_dasha

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def generate_monthly_report(year=None, month=None, symbol='nifty'):
    """Generate monthly astrological overview."""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    os.makedirs(REPORT_DIR, exist_ok=True)

    month_name = calendar.month_name[month]
    num_days = calendar.monthrange(year, month)[1]

    print(f"\n📅 MONTHLY ASTRO OVERVIEW — {month_name} {year}")
    print(f"📊 Symbol: {symbol.upper()}")
    print(f"{'='*65}")

    # Collect key events for the month
    key_events = []
    critical_dates = []

    first_day = f"{year}-{month:02d}-01"
    last_day = f"{year}-{month:02d}-{num_days:02d}"

    # Check each day for major events
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"

        try:
            analysis = full_astro_analysis(date_str)
            panchang = get_full_panchang(date_str)

            # Ingresses
            for ing in analysis['ingresses']:
                key_events.append((date_str, f"🚀 {ing['planet']} enters {ing['to_sign']}"))
                critical_dates.append(date_str)

            # Stations
            for s in analysis['stations']:
                if s['type'] != 'Near Stationary':
                    key_events.append((date_str, f"🛑 {s['planet']} {s['type']}"))
                    critical_dates.append(date_str)

            # Full/New Moon
            if panchang['tithi']['name'] in ['Purnima', 'Amavasya']:
                emoji = '🌕' if panchang['tithi']['name'] == 'Purnima' else '🌑'
                key_events.append((date_str, f"{emoji} {panchang['tithi']['name']}"))
                critical_dates.append(date_str)

        except Exception:
            continue

    # Eclipses
    try:
        eclipses = get_eclipse_analysis(first_day)
        for e in eclipses['year_eclipses']:
            e_month = int(e['date'].split('-')[1])
            if e_month == month:
                key_events.append((e['date'], f"🌑 {e['type']}"))
                critical_dates.append(e['date'])
    except Exception:
        pass

    # Print events
    print(f"\n🔮 KEY ASTROLOGICAL EVENTS:")
    print(f"{'─'*50}")
    for date, event in sorted(key_events):
        print(f"  {date}: {event}")

    if critical_dates:
        print(f"\n⚠️ CRITICAL DATES (expect high volatility):")
        print(f"  {', '.join(sorted(set(critical_dates)))}")

    # Dasha info
    try:
        if symbol.lower() in ['nifty', 'banknifty', 'sensex']:
            mid_month = f"{year}-{month:02d}-15"
            dasha = get_index_dasha(symbol.lower(), mid_month)
            if dasha['current']:
                maha = dasha['current']['mahadasha']
                print(f"\n🔮 DASHA: {symbol.upper()} in {maha['lord']} Mahadasha")
                interp = maha.get('interpretation', {})
                if interp:
                    print(f"  {interp.get('overall', '')}")
    except Exception:
        pass

    # Save
    safe_sym = symbol.replace(' ', '_').replace('^', '')
    filename = os.path.join(REPORT_DIR, f'monthly_{safe_sym}_{year}_{month:02d}.txt')
    with open(filename, 'w') as f:
        f.write(f"FIN ASTRO BOT — MONTHLY REPORT\n")
        f.write(f"{month_name} {year} | {symbol}\n\n")
        f.write(f"KEY EVENTS:\n")
        for date, event in sorted(key_events):
            f.write(f"  {date}: {event}\n")
        if critical_dates:
            f.write(f"\nCRITICAL DATES: {', '.join(sorted(set(critical_dates)))}\n")

    print(f"\n💾 Monthly report saved to: {filename}")

    return {'key_events': key_events, 'critical_dates': critical_dates}


if __name__ == '__main__':
    generate_monthly_report()