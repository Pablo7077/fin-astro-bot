"""
=============================================================
FIN ASTRO BOT v2.0 — Symbol Registry & Presets
=============================================================
Supports ANY symbol from Yahoo Finance:
  - Indian indices/stocks (NSE/BSE)
  - US indices/stocks (NASDAQ/NYSE)
  - Crypto (BTC, ETH, etc.)
  - Global indices (DAX, FTSE, Nikkei, etc.)
  - Commodities (Gold, Crude, etc.)
=============================================================
"""


# ── Symbol Format Rules ───────────────────────────────────
# Yahoo Finance symbol formats:
#   NSE stocks:     SYMBOL.NS (e.g., TATAPOWER.NS, RELIANCE.NS)
#   BSE stocks:     SYMBOL.BO (e.g., TATAPOWER.BO)
#   NSE Index:      ^NSEI (Nifty), ^NSEBANK (Bank Nifty)
#   US stocks:      AAPL, MSFT, TSLA (no suffix)
#   US indices:     ^GSPC (S&P500), ^IXIC (NASDAQ), ^DJI (Dow)
#   Crypto:         BTC-USD, ETH-USD, SOL-USD
#   Global indices: ^GDAXI (DAX), ^FTSE, ^N225 (Nikkei)
#   Commodities:    GC=F (Gold), CL=F (Crude), SI=F (Silver)


# ── Preset Symbol Groups ─────────────────────────────────

INDIAN_INDICES = {
    'nifty': {'symbol': '^NSEI', 'name': 'Nifty 50', 'currency': 'INR'},
    'banknifty': {'symbol': '^NSEBANK', 'name': 'Bank Nifty', 'currency': 'INR'},
    'sensex': {'symbol': '^BSESN', 'name': 'BSE Sensex', 'currency': 'INR'},
    'niftyit': {'symbol': '^CNXIT', 'name': 'Nifty IT', 'currency': 'INR'},
    'niftypharma': {'symbol': '^CNXPHARMA', 'name': 'Nifty Pharma', 'currency': 'INR'},
    'finnifty': {'symbol': 'NIFTY_FIN_SERVICE.NS', 'name': 'Fin Nifty', 'currency': 'INR'},
}

US_INDICES = {
    'sp500': {'symbol': '^GSPC', 'name': 'S&P 500', 'currency': 'USD'},
    'nasdaq': {'symbol': '^IXIC', 'name': 'NASDAQ Composite', 'currency': 'USD'},
    'dow': {'symbol': '^DJI', 'name': 'Dow Jones', 'currency': 'USD'},
    'russell': {'symbol': '^RUT', 'name': 'Russell 2000', 'currency': 'USD'},
    'vix': {'symbol': '^VIX', 'name': 'VIX (Fear Index)', 'currency': 'USD'},
}

GLOBAL_INDICES = {
    'dax': {'symbol': '^GDAXI', 'name': 'DAX (Germany)', 'currency': 'EUR'},
    'ftse': {'symbol': '^FTSE', 'name': 'FTSE 100 (UK)', 'currency': 'GBP'},
    'nikkei': {'symbol': '^N225', 'name': 'Nikkei 225 (Japan)', 'currency': 'JPY'},
    'hangseng': {'symbol': '^HSI', 'name': 'Hang Seng (HK)', 'currency': 'HKD'},
    'shanghai': {'symbol': '000001.SS', 'name': 'Shanghai Composite', 'currency': 'CNY'},
    'kospi': {'symbol': '^KS11', 'name': 'KOSPI (Korea)', 'currency': 'KRW'},
    'asx200': {'symbol': '^AXJO', 'name': 'ASX 200 (Australia)', 'currency': 'AUD'},
}

CRYPTO = {
    'bitcoin': {'symbol': 'BTC-USD', 'name': 'Bitcoin', 'currency': 'USD'},
    'ethereum': {'symbol': 'ETH-USD', 'name': 'Ethereum', 'currency': 'USD'},
    'solana': {'symbol': 'SOL-USD', 'name': 'Solana', 'currency': 'USD'},
    'xrp': {'symbol': 'XRP-USD', 'name': 'XRP', 'currency': 'USD'},
    'bnb': {'symbol': 'BNB-USD', 'name': 'BNB', 'currency': 'USD'},
    'dogecoin': {'symbol': 'DOGE-USD', 'name': 'Dogecoin', 'currency': 'USD'},
    'cardano': {'symbol': 'ADA-USD', 'name': 'Cardano', 'currency': 'USD'},
}

COMMODITIES = {
    'gold': {'symbol': 'GC=F', 'name': 'Gold Futures', 'currency': 'USD'},
    'silver': {'symbol': 'SI=F', 'name': 'Silver Futures', 'currency': 'USD'},
    'crude': {'symbol': 'CL=F', 'name': 'Crude Oil WTI', 'currency': 'USD'},
    'naturalgas': {'symbol': 'NG=F', 'name': 'Natural Gas', 'currency': 'USD'},
    'copper': {'symbol': 'HG=F', 'name': 'Copper Futures', 'currency': 'USD'},
}

POPULAR_INDIAN_STOCKS = {
    'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infy': 'INFY.NS',
    'hdfcbank': 'HDFCBANK.NS', 'icicibank': 'ICICIBANK.NS',
    'sbin': 'SBIN.NS', 'tatapower': 'TATAPOWER.NS',
    'tatamotors': 'TATAMOTORS.NS', 'tatasteel': 'TATASTEEL.NS',
    'adanient': 'ADANIENT.NS', 'bajfinance': 'BAJFINANCE.NS',
    'maruti': 'MARUTI.NS', 'wipro': 'WIPRO.NS', 'sunpharma': 'SUNPHARMA.NS',
    'titan': 'TITAN.NS', 'lt': 'LT.NS', 'coalindia': 'COALINDIA.NS',
    'ntpc': 'NTPC.NS', 'powergrid': 'POWERGRID.NS', 'ongc': 'ONGC.NS',
    'hindalco': 'HINDALCO.NS', 'bhartiartl': 'BHARTIARTL.NS',
    'asianpaint': 'ASIANPAINT.NS', 'axisbank': 'AXISBANK.NS',
    'kotakbank': 'KOTAKBANK.NS', 'drreddy': 'DRREDDY.NS',
    'irctc': 'IRCTC.NS', 'zomato': 'ZOMATO.NS', 'paytm': 'PAYTM.NS',
}

POPULAR_US_STOCKS = {
    'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL',
    'amazon': 'AMZN', 'tesla': 'TSLA', 'nvidia': 'NVDA',
    'meta': 'META', 'netflix': 'NFLX', 'amd': 'AMD',
}

# All presets combined
ALL_PRESETS = {
    **INDIAN_INDICES, **US_INDICES, **GLOBAL_INDICES,
    **CRYPTO, **COMMODITIES,
}


def resolve_symbol(user_input):
    """
    Resolve user-friendly input to Yahoo Finance symbol.

    Examples:
        'nifty'       → '^NSEI'
        'bitcoin'     → 'BTC-USD'
        'tatapower'   → 'TATAPOWER.NS'
        'AAPL'        → 'AAPL'
        'RELIANCE.NS' → 'RELIANCE.NS' (pass-through)
        'nasdaq'      → '^IXIC'
        'gold'        → 'GC=F'
    """
    user_lower = user_input.strip().lower().replace(' ', '').replace('-', '').replace('_', '')

    # Check presets
    if user_lower in ALL_PRESETS:
        return ALL_PRESETS[user_lower]['symbol'], ALL_PRESETS[user_lower]['name']

    # Check Indian stocks
    if user_lower in POPULAR_INDIAN_STOCKS:
        return POPULAR_INDIAN_STOCKS[user_lower], user_input.upper()

    # Check US stocks
    if user_lower in POPULAR_US_STOCKS:
        return POPULAR_US_STOCKS[user_lower], user_input.upper()

    # If already has suffix (.NS, .BO, -USD, =F, ^), pass through
    if any(x in user_input for x in ['.NS', '.BO', '-USD', '=F', '^']):
        return user_input, user_input

    # Try as NSE stock (most common for Indian users)
    if user_input.upper().isalpha() and len(user_input) <= 20:
        nse_symbol = f"{user_input.upper()}.NS"
        return nse_symbol, user_input.upper()

    # Fallback: return as-is
    return user_input, user_input


def list_all_presets():
    """List all available preset symbols."""
    categories = {
        '🇮🇳 Indian Indices': INDIAN_INDICES,
        '🇺🇸 US Indices': US_INDICES,
        '🌍 Global Indices': GLOBAL_INDICES,
        '₿ Crypto': CRYPTO,
        '🪙 Commodities': COMMODITIES,
    }

    for cat_name, presets in categories.items():
        print(f"\n{cat_name}:")
        for key, info in presets.items():
            print(f"  {key:15s} → {info['symbol']:15s} ({info['name']})")

    print(f"\n🇮🇳 Popular Indian Stocks:")
    for key, sym in list(POPULAR_INDIAN_STOCKS.items())[:10]:
        print(f"  {key:15s} → {sym}")
    print(f"  ... and {len(POPULAR_INDIAN_STOCKS) - 10} more")

    print(f"\n💡 Or type any symbol directly: AAPL, TSLA, RELIANCE.NS, BTC-USD, etc.")


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    print("📋 SYMBOL REGISTRY")
    print("=" * 50)
    list_all_presets()

    print("\n\n🔍 RESOLUTION TESTS:")
    test_inputs = ['nifty', 'bitcoin', 'tatapower', 'AAPL', 'nasdaq',
                   'gold', 'RELIANCE.NS', 'sensex', 'ethereum']
    for inp in test_inputs:
        sym, name = resolve_symbol(inp)
        print(f"  '{inp}' → {sym} ({name})")