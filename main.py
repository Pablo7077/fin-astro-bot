"""
=============================================================
🔮 FIN ASTRO BOT v2.0 — Main CLI Runner
=============================================================
Usage:
    python main.py                          # Interactive menu
    python main.py --quick                  # Quick today analysis
    python main.py --quick 2025-01-15       # Quick specific date
    python main.py --project nifty          # Full projection today
    python main.py --project bitcoin 2025-03-20  # Any symbol, any date
    python main.py --weekly nifty           # Weekly report
    python main.py --monthly nifty          # Monthly report
    python main.py --build nifty            # Build historical dataset
    python main.py --backtest nifty         # Full backtest
    python main.py --hora                   # Today's hora timing
    python main.py --sectors                # Sector rotation
    python main.py --dasha nifty            # Dasha analysis
    python main.py --symbols                # List all symbols
    python main.py --dashboard              # Launch web dashboard
=============================================================
"""

import sys
import os
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔮  FIN ASTRO BOT  v2.0  🔮                               ║
║                                                              ║
║   Financial Astrology Research Engine                        ║
║   Vedic Jyotish ←→ Market Correlation                       ║
║                                                              ║
║   Supports: Nifty, Bank Nifty, Bitcoin, NASDAQ, Gold,       ║
║             Any stock (TATAPOWER, AAPL, TSLA...) & more     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def mode_quick(date_str=None):
    """Quick planetary analysis."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    from core.astro_engine import full_astro_analysis
    from core.yogas import detect_all_yogas
    from core.panchang import get_full_panchang

    print(f"\n⚡ QUICK ASTRO ANALYSIS — {date_str}")
    print("=" * 60)

    analysis = full_astro_analysis(date_str)

    print(f"\n📍 PLANETARY POSITIONS:")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':16s} {'Dignity':12s} {'R':3s}")
    print("-" * 67)
    for name, d in analysis['positions'].items():
        r = '℞' if d['retrograde'] else ''
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:13s} P{d['pada']}  {d['dignity']:12s} {r}")

    yogas = detect_all_yogas(analysis['positions'])
    if yogas:
        print(f"\n⭐ YOGAS:")
        for y in yogas:
            emoji = '🟢' if 'bullish' in y['market_bias'] else ('🔴' if 'bearish' in y['market_bias'] else '🟡')
            print(f"  {emoji} {y['name']}: {y['description'][:60]}")

    panchang = get_full_panchang(date_str)
    t = panchang['tithi']
    k = panchang['karana']
    ny = panchang['nitya_yoga']
    print(f"\n📅 PANCHANG:")
    print(f"  Tithi: {t['paksha']} {t['name']} | Karana: {k['name']} | Yoga: {ny['name']}")
    print(f"  Moon: {panchang['moon_phase']['phase']}")
    if t['is_critical']:
        print(f"  ⚠️ CRITICAL TITHI!")
    if k['is_vishti']:
        print(f"  🚫 VISHTI KARANA — Avoid new trades!")


def mode_projection(symbol='nifty', date_str=None):
    """Full projection."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    from analysis.correlator import get_or_build_dataset
    from analysis.projector import generate_full_projection

    # Try to load dataset, run projection without if not available
    try:
        dataset, name = get_or_build_dataset(symbol, start_date='2020-01-01')
    except Exception:
        dataset = None

    generate_full_projection(date_str, symbol, dataset)


def mode_hora(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    from core.hora import get_trading_hora_summary
    summary = get_trading_hora_summary(date_str)

    print(f"\n⏰ HORA TIMING — {date_str} ({summary['weekday']})")
    print(f"  Day Ruler: {summary['day_ruler']} | Sunrise: {summary['sunrise']} | Sunset: {summary['sunset']}")
    print(f"\n{'Time':15s} {'Planet':10s} {'Bias':10s} {'Action'}")
    print("-" * 70)
    for h in summary['market_horas']:
        emoji = '🟢' if h['bias'] == 'bullish' else ('🔴' if h['bias'] == 'bearish' else '🟡')
        print(f"{h['start']}-{h['end']}    {emoji} {h['planet']:10s} {h['bias']:10s} {h['action']}")

    print(f"\n⚠️ KEY PERIODS:")
    for name, period in summary['inauspicious'].items():
        print(f"  {name}: {period['start']} - {period['end']}")


def mode_sectors(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    from core.sector_map import get_top_sectors, get_commodity_signals
    result = get_top_sectors(date_str)

    print(f"\n🏭 SECTOR ROTATION — {date_str}")
    print("=" * 60)
    print(f"\n📈 TOP BULLISH:")
    for s in result['bullish_sectors']:
        print(f"  {s['recommendation']} {s['sector']:25s} ({s['ruling_planet']}, score: {s['score']})")

    print(f"\n📉 TOP BEARISH:")
    for s in result['bearish_sectors']:
        print(f"  {s['recommendation']} {s['sector']:25s} ({s['ruling_planet']}, score: {s['score']})")

    print(f"\n🪙 COMMODITIES:")
    for name, data in get_commodity_signals(date_str).items():
        print(f"  {data['bias']} {name:20s} (score: {data['score']})")


def mode_dasha(symbol='nifty', date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    from core.dasha import get_index_dasha
    result = get_index_dasha(symbol, date_str)

    print(f"\n🔮 DASHA — {symbol.upper()} (as of {date_str})")
    print("=" * 60)

    if result['current']:
        maha = result['current']['mahadasha']
        print(f"  Mahadasha: {maha['lord']} ({maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')})")

        antar = result['current'].get('antardasha')
        if antar:
            print(f"  Antardasha: {antar['antardasha_lord']} ({antar['start'].strftime('%Y-%m-%d')} to {antar['end'].strftime('%Y-%m-%d')})")

        interp = maha.get('interpretation', {})
        if interp:
            print(f"\n  {interp.get('overall', '')}")
            print(f"  Bullish: {', '.join(interp.get('bullish_sectors', []))}")

        print(f"\n  ALL MAHADASHAS:")
        for d in result['all_dashas']['dashas']:
            marker = ' ◀' if d['lord'] == maha['lord'] else ''
            print(f"    {d['lord']:10s} {d['start'].strftime('%Y-%m-%d')} to {d['end'].strftime('%Y-%m-%d')} ({d['years']}y){marker}")


def mode_symbols():
    from market.symbols import list_all_presets
    list_all_presets()


def mode_dashboard():
    print("🌐 Launching Streamlit Dashboard...")
    print("   (This will open a browser tab)")
    os.system("streamlit run dashboard/app.py")


def interactive_menu():
    """Interactive menu for beginners."""
    today = datetime.now().strftime('%Y-%m-%d')

    print(f"📅 Today: {today}\n")
    print("Choose what to do:")
    print("  1. ⚡ Quick Analysis (today)")
    print("  2. 🔮 Full Projection (today, Nifty)")
    print("  3. 🔮 Full Projection (custom symbol/date)")
    print("  4. ⏰ Hora Timing (today)")
    print("  5. 🏭 Sector Rotation")
    print("  6. 🔮 Dasha Analysis")
    print("  7. 📅 Weekly Report")
    print("  8. 📆 Monthly Report")
    print("  9. 📊 Build Historical Dataset")
    print(" 10. 📈 Full Backtest")
    print(" 11. 🌐 Launch Web Dashboard")
    print(" 12. 📋 List All Symbols")

    choice = input("\nEnter choice (1-12): ").strip()

    if choice == '1':
        mode_quick()
    elif choice == '2':
        mode_projection('nifty')
    elif choice == '3':
        sym = input("Symbol (e.g., nifty, bitcoin, tatapower, AAPL): ").strip() or 'nifty'
        date = input(f"Date (YYYY-MM-DD) [default: {today}]: ").strip() or today
        mode_projection(sym, date)
    elif choice == '4':
        mode_hora()
    elif choice == '5':
        mode_sectors()
    elif choice == '6':
        sym = input("Index (nifty/banknifty/sensex): ").strip() or 'nifty'
        mode_dasha(sym)
    elif choice == '7':
        sym = input("Symbol [default: nifty]: ").strip() or 'nifty'
        from reports.weekly_report import generate_weekly_report
        generate_weekly_report(symbol=sym)
    elif choice == '8':
        sym = input("Symbol [default: nifty]: ").strip() or 'nifty'
        from reports.monthly_report import generate_monthly_report
        generate_monthly_report(symbol=sym)
    elif choice == '9':
        sym = input("Symbol [default: nifty]: ").strip() or 'nifty'
        from analysis.correlator import build_astro_market_dataset
        build_astro_market_dataset(sym, start_date='2018-01-01')
    elif choice == '10':
        sym = input("Symbol [default: nifty]: ").strip() or 'nifty'
        from analysis.correlator import get_or_build_dataset
        from analysis.backtester import run_full_backtest
        data, name = get_or_build_dataset(sym)
        if not data.empty:
            run_full_backtest(data, name)
    elif choice == '11':
        mode_dashboard()
    elif choice == '12':
        mode_symbols()
    else:
        print("Invalid choice.")


def main():
    print_banner()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == '--quick':
            date = sys.argv[2] if len(sys.argv) > 2 else None
            mode_quick(date)
        elif cmd == '--project':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            date = sys.argv[3] if len(sys.argv) > 3 else None
            mode_projection(sym, date)
        elif cmd == '--hora':
            date = sys.argv[2] if len(sys.argv) > 2 else None
            mode_hora(date)
        elif cmd == '--sectors':
            mode_sectors()
        elif cmd == '--dasha':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            mode_dasha(sym)
        elif cmd == '--weekly':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            from reports.weekly_report import generate_weekly_report
            generate_weekly_report(symbol=sym)
        elif cmd == '--monthly':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            from reports.monthly_report import generate_monthly_report
            generate_monthly_report(symbol=sym)
        elif cmd == '--build':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            from analysis.correlator import build_astro_market_dataset
            build_astro_market_dataset(sym, start_date='2018-01-01')
        elif cmd == '--backtest':
            sym = sys.argv[2] if len(sys.argv) > 2 else 'nifty'
            from analysis.correlator import get_or_build_dataset
            from analysis.backtester import run_full_backtest
            data, name = get_or_build_dataset(sym)
            if not data.empty:
                run_full_backtest(data, name)
        elif cmd == '--symbols':
            mode_symbols()
        elif cmd == '--dashboard':
            mode_dashboard()
        else:
            print("Unknown command. Use --quick, --project, --hora, --sectors, etc.")
    else:
        interactive_menu()


if __name__ == '__main__':
    main()