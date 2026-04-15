"""
=============================================================
🔮 FIN ASTRO BOT — Main Runner
=============================================================
Your daily financial astrology research assistant.

Usage:
    python main.py                  # Today's analysis
    python main.py 2025-01-15       # Specific date
    python main.py --build          # Build full historical dataset
    python main.py --backtest       # Run historical back-test
=============================================================
"""

import sys
import os
import pickle
from datetime import datetime

from astro_engine import full_astro_analysis
from market_data import get_nifty_data, get_gap_statistics
from insights import (
    build_astro_market_dataset,
    analyze_moon_sign_gaps,
    analyze_moon_nakshatra_gaps,
    analyze_retrograde_impact,
    analyze_retro_count_impact,
    generate_today_projection,
)

DATASET_FILE = 'astro_market_dataset.pkl'


def print_banner():
    """Print the bot banner."""
    print("""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🔮  FIN ASTRO BOT  🔮                             ║
║                                                      ║
║   Financial Astrology Research for Nifty/BankNifty   ║
║   Vedic (Jyotish) ← → Market Correlation Engine     ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    """)


def load_or_build_dataset(force_rebuild=False):
    """Load cached dataset or build from scratch."""
    if os.path.exists(DATASET_FILE) and not force_rebuild:
        print(f"📂 Loading cached dataset from {DATASET_FILE}...")
        with open(DATASET_FILE, 'rb') as f:
            dataset = pickle.load(f)
        print(f"✅ Loaded {len(dataset)} trading days.")
        return dataset

    print("🔨 Building dataset from scratch (this takes 5-15 minutes)...")
    print("   (Calculating planetary positions for each trading day)\n")

    dataset = build_astro_market_dataset(start_date='2015-01-01')

    if not dataset.empty:
        with open(DATASET_FILE, 'wb') as f:
            pickle.dump(dataset, f)
        print(f"\n💾 Dataset saved to {DATASET_FILE} for future use.")

    return dataset


def mode_quick_analysis(date_str):
    """Quick astro analysis without historical correlation."""
    print(f"\n⚡ QUICK ASTRO ANALYSIS FOR {date_str}")
    print("=" * 55)
    print("(No historical correlation — just planetary positions)\n")

    analysis = full_astro_analysis(date_str)

    print("📍 PLANETARY POSITIONS (Sidereal/Lahiri):")
    print("-" * 55)
    for name, data in analysis['positions'].items():
        retro_mark = ' ℞' if data['retrograde'] else ''
        print(f"  {name:10s} → {data['sign']:13s} "
              f"{data['sign_degree']:6.2f}° "
              f"| {data['nakshatra']} Pada-{data['pada']}"
              f"{retro_mark}")

    if analysis['retrogrades']:
        print(f"\n🔄 RETROGRADES: {', '.join(analysis['retrogrades'])}")

    if analysis['combustions']:
        print(f"\n🔥 COMBUSTIONS:")
        for c in analysis['combustions']:
            print(f"  {c['planet']} — {c['severity']} "
                  f"({c['distance_from_sun']}° from Sun)")

    mp = analysis['moon_phase']
    print(f"\n🌙 Moon Phase: {mp['phase']}")
    print(f"   Tithi: {mp['paksha']} {mp['tithi_name']}")
    print(f"   Market Note: {mp['market_note']}")

    if analysis['yogas']:
        print(f"\n⭐ ACTIVE YOGAS:")
        for y in analysis['yogas']:
            print(f"  {y['name']}")
            print(f"    Effect: {y['effect']}")
            print(f"    Market Bias: {y['market_bias'].upper()}")

    if analysis['ingresses']:
        print(f"\n🚀 SIGN CHANGES TODAY:")
        for ing in analysis['ingresses']:
            print(f"  {ing['event']}")

    tight_aspects = [a for a in analysis['aspects'] if a['tight']]
    if tight_aspects:
        print(f"\n🎯 TIGHT ASPECTS (within 2°):")
        for a in tight_aspects:
            print(f"  {a['planet1']} {a['aspect']} {a['planet2']} "
                  f"(orb: {a['orb']}°)")


def mode_full_projection(date_str):
    """Full analysis with historical correlation."""
    dataset = load_or_build_dataset()
    if dataset.empty:
        print("❌ Could not build dataset. Running quick analysis instead.")
        mode_quick_analysis(date_str)
        return

    generate_today_projection(dataset, target_date=date_str)


def mode_build_dataset():
    """Force rebuild the historical dataset."""
    dataset = load_or_build_dataset(force_rebuild=True)
    if not dataset.empty:
        analyze_moon_sign_gaps(dataset)
        analyze_moon_nakshatra_gaps(dataset)
        analyze_retrograde_impact(dataset)
        analyze_retro_count_impact(dataset)


def mode_backtest():
    """Run back-test analysis."""
    dataset = load_or_build_dataset()
    if dataset.empty:
        print("❌ No dataset available for back-testing.")
        return

    print("\n📊 FULL BACK-TEST ANALYSIS")
    print("=" * 65)

    analyze_moon_sign_gaps(dataset)
    analyze_moon_nakshatra_gaps(dataset)
    analyze_retrograde_impact(dataset)
    analyze_retro_count_impact(dataset)

    # Show overall market stats
    print("\n\n📈 NIFTY OVERALL STATISTICS:")
    get_gap_statistics(dataset)


def main():
    """Main entry point."""
    print_banner()

    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == '--build':
            mode_build_dataset()
        elif arg == '--backtest':
            mode_backtest()
        elif arg == '--quick':
            date_str = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime('%Y-%m-%d')
            mode_quick_analysis(date_str)
        elif arg.count('-') == 2:  # Looks like a date
            try:
                datetime.strptime(arg, '%Y-%m-%d')
                mode_full_projection(arg)
            except ValueError:
                print(f"❌ Invalid date format: {arg}. Use YYYY-MM-DD")
        else:
            print("Usage:")
            print("  python main.py                  # Today's full projection")
            print("  python main.py 2025-01-15       # Specific date projection")
            print("  python main.py --quick           # Quick (no history) today")
            print("  python main.py --quick 2025-03-20 # Quick for specific date")
            print("  python main.py --build           # Build historical dataset")
            print("  python main.py --backtest        # Run full back-test")
    else:
        # Default: today's projection
        today = datetime.now().strftime('%Y-%m-%d')

        print(f"📅 Date: {today}")
        print(f"\nChoose mode:")
        print(f"  1. Quick Analysis (fast, planets only)")
        print(f"  2. Full Projection (slower, includes historical correlation)")
        print(f"  3. Build/Rebuild Dataset")
        print(f"  4. Full Back-test Report")

        choice = input(f"\nEnter choice (1-4) [default: 1]: ").strip()

        if choice == '2':
            mode_full_projection(today)
        elif choice == '3':
            mode_build_dataset()
        elif choice == '4':
            mode_backtest()
        else:
            mode_quick_analysis(today)


if __name__ == '__main__':
    main()