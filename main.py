"""
=============================================================
🔮 FIN ASTRO BOT v2.5 — Main CLI Runner
=============================================================
Usage:
    python main.py
    python main.py --quick [YYYY-MM-DD]
    python main.py --project [symbol] [YYYY-MM-DD]
    python main.py --weekly [symbol]
    python main.py --monthly [symbol]
    python main.py --build [symbol] [start_date]
    python main.py --backtest [symbol]
    python main.py --projection-backtest [symbol] [start_date] [end_date]
    python main.py --hora [YYYY-MM-DD]
    python main.py --sectors
    python main.py --dasha [symbol]
    python main.py --symbols
    python main.py --dashboard
    python main.py --health
=============================================================
"""

import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔮  FIN ASTRO BOT  v2.5  🔮                               ║
║                                                              ║
║   Financial Astrology Research Engine                        ║
║   Vedic Jyotish ←→ Market Correlation                       ║
║                                                              ║
║   Supports: Nifty, Bank Nifty, Bitcoin, NASDAQ, Gold,       ║
║             Any stock (TATAPOWER, AAPL, TSLA...) & more     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def _today():
    return datetime.now().strftime("%Y-%m-%d")


def _validate_date_or_none(date_str):
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print(f"❌ Invalid date: {date_str}. Use YYYY-MM-DD, for example 2026-04-28.")
        return None


def mode_quick(date_str=None):
    if date_str is None:
        date_str = _today()
    from core.astro_engine import full_astro_analysis
    from core.yogas import detect_all_yogas
    from core.panchang import get_full_panchang

    print(f"\n⚡ QUICK ASTRO ANALYSIS — {date_str}")
    print("=" * 60)
    analysis = full_astro_analysis(date_str)

    print("\n📍 PLANETARY POSITIONS:")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':16s} {'Dignity':12s} {'R':3s}")
    print("-" * 67)
    for name, d in analysis["positions"].items():
        r = "℞" if d.get("retrograde") else ""
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:13s} P{d['pada']}  {d['dignity']:12s} {r}")

    yogas = detect_all_yogas(analysis["positions"])
    if yogas:
        print("\n⭐ YOGAS:")
        for y in yogas:
            mb = str(y.get("market_bias", "")).lower()
            emoji = "🟢" if "bullish" in mb else ("🔴" if "bearish" in mb else "🟡")
            print(f"  {emoji} {y['name']}: {str(y.get('description', ''))[:70]}")

    panchang = get_full_panchang(date_str)
    t = panchang["tithi"]
    k = panchang["karana"]
    ny = panchang["nitya_yoga"]
    print("\n📅 PANCHANG:")
    print(f"  Tithi: {t['paksha']} {t['name']} | Karana: {k['name']} | Yoga: {ny['name']}")
    print(f"  Moon: {panchang['moon_phase']['phase']}")
    if t.get("is_critical"):
        print("  ⚠️ CRITICAL TITHI!")
    if k.get("is_vishti"):
        print("  🚫 VISHTI KARANA — Avoid new trades!")


def mode_projection(symbol="nifty", date_str=None):
    if date_str is None:
        date_str = _today()
    from analysis.correlator import get_or_build_dataset
    from analysis.projector import generate_full_projection
    try:
        dataset, _ = get_or_build_dataset(symbol, start_date="2010-01-01")
    except Exception as e:
        print(f"⚠️ Could not load/build dataset. Projection will run without historical context. Reason: {e}")
        dataset = None
    generate_full_projection(date_str, symbol, dataset, return_result=True, verbose=True)


def mode_hora(date_str=None):
    if date_str is None:
        date_str = _today()
    from core.hora import get_trading_hora_summary
    summary = get_trading_hora_summary(date_str)
    print(f"\n⏰ HORA TIMING — {date_str} ({summary['weekday']})")
    print(f"  Day Ruler: {summary['day_ruler']} | Sunrise: {summary['sunrise']} | Sunset: {summary['sunset']}")
    print(f"\n{'Time':15s} {'Planet':10s} {'Bias':10s} {'Action'}")
    print("-" * 70)
    for h in summary["market_horas"]:
        emoji = "🟢" if h["bias"] == "bullish" else ("🔴" if h["bias"] == "bearish" else "🟡")
        print(f"{h['start']}-{h['end']}    {emoji} {h['planet']:10s} {h['bias']:10s} {h['action']}")
    print("\n⚠️ KEY PERIODS:")
    for name, period in summary["inauspicious"].items():
        print(f"  {name}: {period['start']} - {period['end']}")


def mode_sectors(date_str=None):
    if date_str is None:
        date_str = _today()
    from core.sector_map import get_top_sectors, get_commodity_signals
    result = get_top_sectors(date_str)
    print(f"\n🏭 SECTOR ROTATION — {date_str}")
    print("=" * 60)
    print("\n📈 TOP BULLISH:")
    for s in result["bullish_sectors"]:
        print(f"  {s['recommendation']} {s['sector']:25s} ({s['ruling_planet']}, score: {s['score']})")
    print("\n📉 TOP BEARISH:")
    for s in result["bearish_sectors"]:
        print(f"  {s['recommendation']} {s['sector']:25s} ({s['ruling_planet']}, score: {s['score']})")
    print("\n🪙 COMMODITIES:")
    for name, data in get_commodity_signals(date_str).items():
        print(f"  {data['bias']} {name:20s} (score: {data['score']})")


def mode_dasha(symbol="nifty", date_str=None):
    if date_str is None:
        date_str = _today()
    from core.dasha import get_index_dasha
    result = get_index_dasha(symbol, date_str)
    print(f"\n🔮 DASHA — {symbol.upper()} (as of {date_str})")
    print("=" * 60)
    if result.get("current"):
        maha = result["current"]["mahadasha"]
        print(f"  Mahadasha: {maha['lord']} ({maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')})")
        antar = result["current"].get("antardasha")
        if antar:
            print(f"  Antardasha: {antar['antardasha_lord']} ({antar['start'].strftime('%Y-%m-%d')} to {antar['end'].strftime('%Y-%m-%d')})")
        interp = maha.get("interpretation", {})
        if interp:
            print(f"\n  {interp.get('overall', '')}")
            print(f"  Bullish: {', '.join(interp.get('bullish_sectors', []))}")


def mode_symbols():
    from market.symbols import list_all_presets
    list_all_presets()


def mode_dashboard():
    print("🌐 Launching Streamlit Dashboard...")
    os.system("streamlit run dashboard/app.py")


def interactive_menu():
    today = _today()
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
    print(" 10. 📈 Factor Backtest")
    print(" 11. 🎯 Projection Backtest")
    print(" 12. 🌐 Launch Web Dashboard")
    print(" 13. 📋 List All Symbols")
    print(" 14. 🧪 Health Check")
    choice = input("\nEnter choice (1-14): ").strip()

    if choice == "1":
        mode_quick()
    elif choice == "2":
        mode_projection("nifty")
    elif choice == "3":
        sym = input("Symbol (e.g., nifty, bitcoin, tatapower, AAPL): ").strip() or "nifty"
        date = input(f"Date (YYYY-MM-DD) [default: {today}]: ").strip() or today
        mode_projection(sym, _validate_date_or_none(date) or today)
    elif choice == "4":
        mode_hora()
    elif choice == "5":
        mode_sectors()
    elif choice == "6":
        sym = input("Index (nifty/banknifty/sensex): ").strip() or "nifty"
        mode_dasha(sym)
    elif choice == "7":
        sym = input("Symbol [default: nifty]: ").strip() or "nifty"
        from reports.weekly_report import generate_weekly_report
        generate_weekly_report(symbol=sym)
    elif choice == "8":
        sym = input("Symbol [default: nifty]: ").strip() or "nifty"
        from reports.monthly_report import generate_monthly_report
        generate_monthly_report(symbol=sym)
    elif choice == "9":
        sym = input("Symbol [default: nifty]: ").strip() or "nifty"
        start = input("Start date [default: 2010-01-01]: ").strip() or "2010-01-01"
        from analysis.correlator import build_astro_market_dataset
        build_astro_market_dataset(sym, start_date=start)
    elif choice == "10":
        sym = input("Symbol [default: nifty]: ").strip() or "nifty"
        from analysis.correlator import get_or_build_dataset
        from analysis.backtester import run_full_backtest
        data, name = get_or_build_dataset(sym)
        if not data.empty:
            run_full_backtest(data, name)
    elif choice == "11":
        sym = input("Symbol [default: nifty]: ").strip() or "nifty"
        from analysis.projection_backtester import run_projection_backtest
        run_projection_backtest(sym)
    elif choice == "12":
        mode_dashboard()
    elif choice == "13":
        mode_symbols()
    elif choice == "14":
        import bot_health_check
        bot_health_check.main()
    else:
        print("Invalid choice.")


def main():
    print_banner()
    if len(sys.argv) <= 1:
        interactive_menu()
        return

    cmd = sys.argv[1].lower()
    try:
        if cmd == "--quick":
            mode_quick(_validate_date_or_none(sys.argv[2]) if len(sys.argv) > 2 else None)
        elif cmd == "--project":
            sym = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            date = _validate_date_or_none(sys.argv[3]) if len(sys.argv) > 3 else None
            mode_projection(sym, date)
        elif cmd == "--hora":
            mode_hora(_validate_date_or_none(sys.argv[2]) if len(sys.argv) > 2 else None)
        elif cmd == "--sectors":
            mode_sectors()
        elif cmd == "--dasha":
            mode_dasha(sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--weekly":
            from reports.weekly_report import generate_weekly_report
            generate_weekly_report(symbol=sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--monthly":
            from reports.monthly_report import generate_monthly_report
            generate_monthly_report(symbol=sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--build":
            sym = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            start = sys.argv[3] if len(sys.argv) > 3 else "2010-01-01"
            from analysis.correlator import build_astro_market_dataset
            build_astro_market_dataset(sym, start_date=start)
        elif cmd == "--backtest":
            sym = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            from analysis.correlator import get_or_build_dataset
            from analysis.backtester import run_full_backtest
            data, name = get_or_build_dataset(sym)
            if not data.empty:
                run_full_backtest(data, name)
        elif cmd == "--projection-backtest":
            sym = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            start_date = sys.argv[3] if len(sys.argv) > 3 else None
            end_date = sys.argv[4] if len(sys.argv) > 4 else None
            from analysis.projection_backtester import run_projection_backtest
            run_projection_backtest(sym, start_date=start_date, end_date=end_date)
        elif cmd == "--symbols":
            mode_symbols()
        elif cmd == "--dashboard":
            mode_dashboard()
        elif cmd == "--health":
            import bot_health_check
            bot_health_check.main()
        else:
            print("Unknown command. Try: --quick, --project, --weekly, --build, --backtest, --projection-backtest, --health")
    except ModuleNotFoundError as e:
        print(f"❌ Missing module/file: {e}")
        print("Run: python main.py --health")
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()
