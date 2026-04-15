"""
=============================================================
FIN ASTRO BOT v2.0 — Sector Rotation Mapper
=============================================================
Maps planetary strength to market sectors and commodities.
Generates "which sectors to focus on THIS week" signals.
=============================================================
"""

from core.astro_engine import get_planetary_positions
from core.divisional import get_all_divisional_positions
from datetime import datetime

# ── Planet → Sector Mapping ───────────────────────────────

PLANET_SECTORS = {
    'Sun': {
        'sectors': ['Power & Energy', 'Pharma', 'Government/PSU', 'Gold Mining'],
        'commodities': ['Gold', 'Wheat'],
        'stocks_nse': ['NTPC', 'POWERGRID', 'SUNPHARMA', 'COALINDIA'],
        'theme': 'Authority, governance, vitality',
    },
    'Moon': {
        'sectors': ['FMCG', 'Hospitality', 'Water/Irrigation', 'Silver'],
        'commodities': ['Silver', 'Water', 'Dairy', 'Rice'],
        'stocks_nse': ['HINDUNILVR', 'ITC', 'TATACONSUM', 'DABUR'],
        'theme': 'Sentiment, liquidity, consumer mood',
    },
    'Mars': {
        'sectors': ['Real Estate', 'Defense', 'Steel & Iron', 'Energy (Oil)'],
        'commodities': ['Iron', 'Copper', 'Crude Oil'],
        'stocks_nse': ['TATASTEEL', 'JSWSTEEL', 'HAL', 'BEL', 'DLF'],
        'theme': 'Aggression, construction, conflict',
    },
    'Mercury': {
        'sectors': ['IT & Software', 'Telecom', 'E-commerce', 'Banking (Trading)'],
        'commodities': ['Cotton', 'Spices'],
        'stocks_nse': ['TCS', 'INFY', 'WIPRO', 'BHARTIARTL', 'HDFCBANK'],
        'theme': 'Communication, intelligence, commerce',
    },
    'Jupiter': {
        'sectors': ['Banking (Institutional)', 'Finance', 'Education', 'Legal'],
        'commodities': ['Gold', 'Tin', 'Saffron'],
        'stocks_nse': ['SBIN', 'ICICIBANK', 'BAJFINANCE', 'HDFCLIFE'],
        'theme': 'Expansion, wisdom, prosperity',
    },
    'Venus': {
        'sectors': ['Auto', 'Luxury & Fashion', 'Entertainment', 'Sugar & Textiles'],
        'commodities': ['Sugar', 'Diamond', 'Platinum', 'Silk'],
        'stocks_nse': ['MARUTI', 'TATAMOTORS', 'TITAN', 'ZEEL', 'BALRAMCHIN'],
        'theme': 'Luxury, beauty, consumer spending',
    },
    'Saturn': {
        'sectors': ['Infrastructure', 'Mining', 'Oil & Gas', 'Agriculture'],
        'commodities': ['Lead', 'Coal', 'Iron Ore', 'Crude Oil'],
        'stocks_nse': ['RELIANCE', 'ONGC', 'ADANIPORTS', 'ULTRACEMCO', 'LT'],
        'theme': 'Structure, restriction, endurance',
    },
    'Rahu': {
        'sectors': ['Technology Disruption', 'Crypto', 'Foreign Investment', 'Aviation'],
        'commodities': ['Cryptocurrency', 'Rare Metals', 'Uranium'],
        'stocks_nse': ['IRCTC', 'INDIGO', 'ZOMATO', 'PAYTM'],
        'theme': 'Disruption, foreign influence, speculation',
    },
    'Ketu': {
        'sectors': ['Pharma R&D', 'IT Backend', 'Spiritual/Alt Medicine', 'Mining (hidden)'],
        'commodities': ['Herbs', 'Nuclear materials'],
        'stocks_nse': ['DIVISLAB', 'LALPATHLAB', 'MPHASIS'],
        'theme': 'Detachment, sudden events, hidden value',
    },
}

# ── Sign → Sector Mapping (supplementary) ────────────────

SIGN_SECTORS = {
    'Aries': ['Defense', 'Steel', 'Sports', 'Surgery/Pharma'],
    'Taurus': ['Banking', 'Agriculture', 'Luxury', 'Real Estate'],
    'Gemini': ['IT', 'Media', 'Telecom', 'Education'],
    'Cancer': ['FMCG', 'Hospitality', 'Water', 'Shipping'],
    'Leo': ['Power', 'Government', 'Entertainment', 'Gold'],
    'Virgo': ['Healthcare', 'IT Services', 'Textiles', 'Accounting'],
    'Libra': ['Auto', 'Fashion', 'Legal', 'Sugar'],
    'Scorpio': ['Insurance', 'Mining', 'Oil & Gas', 'Research'],
    'Sagittarius': ['Finance', 'Education', 'Law', 'Travel'],
    'Capricorn': ['Infrastructure', 'Mining', 'Government', 'Old Economy'],
    'Aquarius': ['Technology', 'Innovation', 'Networking', 'Renewable Energy'],
    'Pisces': ['Pharma', 'Shipping', 'Oil', 'Spiritual/Wellness'],
}


def get_sector_rotation_signals(date_str):
    """
    Analyze planetary strength and generate sector rotation signals.
    Returns ranked list of sectors with buy/sell/hold recommendations.
    """
    positions = get_planetary_positions(date_str)

    # Try divisional, fall back gracefully
    try:
        div = get_all_divisional_positions(date_str)
    except Exception:
        div = {}

    sector_scores = {}

    for planet_name, sector_info in PLANET_SECTORS.items():
        if planet_name not in positions:
            continue

        pos = positions[planet_name]
        div_data = div.get(planet_name, {})

        # Calculate planet strength score
        score = 0

        # 1. Dignity score (from D-1)
        score += pos.get('dignity_score', 0) * 10

        # 2. Retrograde penalty
        if pos['retrograde'] and planet_name not in ['Rahu', 'Ketu']:
            score -= 8

        # 3. Navamsha strength
        nav_score = div_data.get('navamsha_score', 0)
        score += nav_score * 6

        # 4. Vargottama bonus
        if div_data.get('is_vargottama', False):
            score += 15

        # 5. Speed bonus
        speed = abs(pos.get('speed', 0))
        if speed > 0.5:
            score += 3

        # 6. Composite strength
        composite = div_data.get('composite_strength', 0)
        score += composite * 5

        # Determine recommendation
        if score >= 25:
            recommendation = '🟢 STRONG BUY'
            action = 'Accumulate positions in these sectors'
        elif score >= 10:
            recommendation = '🟡 BUY'
            action = 'Moderate buying, watch for dips'
        elif score >= -5:
            recommendation = '⚪ HOLD/NEUTRAL'
            action = 'No clear signal, wait'
        elif score >= -15:
            recommendation = '🟠 REDUCE'
            action = 'Book partial profits, avoid new entries'
        else:
            recommendation = '🔴 AVOID/SELL'
            action = 'Exit positions, stay away'

        for sector in sector_info['sectors']:
            sector_scores[sector] = {
                'ruling_planet': planet_name,
                'score': score,
                'recommendation': recommendation,
                'action': action,
                'dignity': pos['dignity'],
                'retrograde': pos['retrograde'],
                'theme': sector_info['theme'],
                'sample_stocks': sector_info.get('stocks_nse', []),
                'commodities': sector_info.get('commodities', []),
            }

    # Sort by score
    sorted_sectors = dict(sorted(sector_scores.items(),
                                  key=lambda x: x[1]['score'], reverse=True))

    return sorted_sectors


def get_top_sectors(date_str, top_n=5):
    """Get top N bullish and bearish sectors."""
    all_sectors = get_sector_rotation_signals(date_str)
    items = list(all_sectors.items())

    top_bullish = items[:top_n]
    top_bearish = items[-top_n:]
    top_bearish.reverse()

    return {
        'date': date_str,
        'bullish_sectors': [{'sector': k, **v} for k, v in top_bullish],
        'bearish_sectors': [{'sector': k, **v} for k, v in top_bearish],
        'all_sectors': all_sectors,
    }


def get_stock_planet_mapping(stock_symbol):
    """Find which planet(s) rule a given stock based on sector mapping."""
    stock_upper = stock_symbol.upper()
    results = []

    for planet, info in PLANET_SECTORS.items():
        for stock in info.get('stocks_nse', []):
            if stock_upper in stock.upper() or stock.upper() in stock_upper:
                results.append({
                    'stock': stock,
                    'ruling_planet': planet,
                    'sectors': info['sectors'],
                    'theme': info['theme'],
                })

    return results


def get_commodity_signals(date_str):
    """Generate commodity-specific signals based on planetary strength."""
    positions = get_planetary_positions(date_str)
    signals = {}

    commodity_rulers = {
        'Gold': ['Sun', 'Jupiter'],
        'Silver': ['Moon'],
        'Crude Oil': ['Saturn', 'Mars'],
        'Copper': ['Mars'],
        'Iron/Steel': ['Mars'],
        'Sugar': ['Venus'],
        'Cotton': ['Mercury'],
        'Lead/Zinc': ['Saturn'],
        'Diamond/Platinum': ['Venus'],
        'Cryptocurrency': ['Rahu'],
        'Wheat/Rice': ['Sun', 'Moon'],
    }

    for commodity, rulers in commodity_rulers.items():
        total_score = 0
        details = []

        for ruler in rulers:
            if ruler in positions:
                pos = positions[ruler]
                planet_score = pos.get('dignity_score', 0) * 10
                if pos['retrograde'] and ruler not in ['Rahu', 'Ketu']:
                    planet_score -= 5
                total_score += planet_score
                details.append(f"{ruler}: {pos['dignity']}{'(R)' if pos['retrograde'] else ''}")

        avg_score = total_score / len(rulers) if rulers else 0

        if avg_score >= 15:
            bias = '🟢 BULLISH'
        elif avg_score >= 0:
            bias = '🟡 NEUTRAL'
        else:
            bias = '🔴 BEARISH'

        signals[commodity] = {
            'rulers': rulers,
            'score': round(avg_score, 1),
            'bias': bias,
            'details': details,
        }

    return dict(sorted(signals.items(), key=lambda x: x[1]['score'], reverse=True))


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🏭 SECTOR ROTATION SIGNALS — {today}")
    print("=" * 70)

    result = get_top_sectors(today)

    print(f"\n📈 TOP 5 BULLISH SECTORS:")
    print(f"{'Sector':25s} {'Planet':10s} {'Score':>6s} {'Signal'}")
    print("-" * 65)
    for s in result['bullish_sectors']:
        print(f"{s['sector']:25s} {s['ruling_planet']:10s} "
              f"{s['score']:5d}   {s['recommendation']}")
        if s['sample_stocks']:
            print(f"{'':25s} Stocks: {', '.join(s['sample_stocks'][:3])}")

    print(f"\n📉 TOP 5 BEARISH SECTORS:")
    print(f"{'Sector':25s} {'Planet':10s} {'Score':>6s} {'Signal'}")
    print("-" * 65)
    for s in result['bearish_sectors']:
        print(f"{s['sector']:25s} {s['ruling_planet']:10s} "
              f"{s['score']:5d}   {s['recommendation']}")

    print(f"\n🪙 COMMODITY SIGNALS:")
    print(f"{'Commodity':20s} {'Rulers':20s} {'Score':>6s} {'Bias'}")
    print("-" * 60)
    commodities = get_commodity_signals(today)
    for name, data in commodities.items():
        rulers_str = ', '.join(data['rulers'])
        print(f"{name:20s} {rulers_str:20s} {data['score']:5.1f}   {data['bias']}")