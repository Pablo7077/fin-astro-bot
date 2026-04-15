"""
=============================================================
FIN ASTRO BOT v2.0 — Universal Market Data Fetcher
=============================================================
Downloads data for ANY Yahoo Finance symbol.
Works for Indian stocks, US stocks, crypto, commodities, etc.
=============================================================
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from market.symbols import resolve_symbol
import warnings
warnings.filterwarnings('ignore')


def fetch_market_data(user_input, start='2015-01-01', end=None, interval='1d'):
    """
    Universal data fetcher. Accepts:
      - Preset names: 'nifty', 'bitcoin', 'nasdaq', 'gold'
      - Stock names: 'tatapower', 'reliance', 'AAPL'
      - Direct symbols: 'RELIANCE.NS', 'BTC-USD', '^GSPC'

    Returns DataFrame with OHLCV + calculated fields.
    """
    symbol, display_name = resolve_symbol(user_input)

    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')

    print(f"📊 Fetching {display_name} ({symbol}) from {start} to {end}...")

    try:
        data = yf.download(symbol, start=start, end=end, interval=interval,
                           progress=False)
    except Exception as e:
        print(f"❌ Error downloading {symbol}: {e}")
        return pd.DataFrame(), display_name

    if data.empty:
        print(f"⚠️  No data for {symbol}. Check symbol or internet.")
        return pd.DataFrame(), display_name

    # Flatten multi-level columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Timezone cleanup
    data.index = pd.to_datetime(data.index)
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    # Add symbol metadata
    data.attrs['symbol'] = symbol
    data.attrs['name'] = display_name

    print(f"✅ Fetched {len(data)} bars for {display_name}.")
    return data, display_name


def add_gap_analysis(data):
    """Add gap calculations and classifications to market data."""
    if data.empty:
        return data

    df = data.copy()

    # Gaps
    df['Prev_Close'] = df['Close'].shift(1)
    df['Gap'] = df['Open'] - df['Prev_Close']
    df['Gap_Pct'] = (df['Gap'] / df['Prev_Close']) * 100

    # Gap classification
    df['Gap_Type'] = pd.cut(
        df['Gap_Pct'],
        bins=[-float('inf'), -0.5, -0.15, 0.15, 0.5, float('inf')],
        labels=['Strong Gap Down', 'Gap Down', 'Flat', 'Gap Up', 'Strong Gap Up']
    )

    # Daily metrics
    df['Daily_Return'] = df['Close'].pct_change() * 100
    df['Intraday_Range'] = ((df['High'] - df['Low']) / df['Open']) * 100
    df['Day_Direction'] = np.where(
        df['Close'] > df['Open'], 'Bullish',
        np.where(df['Close'] < df['Open'], 'Bearish', 'Neutral')
    )

    # Volatility (20-day rolling)
    df['Volatility_20d'] = df['Daily_Return'].rolling(20).std()

    # Trend (20-day SMA)
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['Above_SMA20'] = df['Close'] > df['SMA_20']

    df.dropna(subset=['Gap'], inplace=True)
    return df


def get_market_data_with_gaps(user_input, start='2015-01-01', end=None):
    """Convenience: fetch + add gap analysis in one call."""
    data, name = fetch_market_data(user_input, start, end)
    if not data.empty:
        data = add_gap_analysis(data)
    return data, name


def get_gap_statistics(data, display_name=''):
    """Print and return gap distribution statistics."""
    if data.empty or 'Gap_Type' not in data.columns:
        print("No gap data available.")
        return {}

    print(f"\n📈 GAP STATISTICS{' — ' + display_name if display_name else ''}:")
    print("-" * 50)

    counts = data['Gap_Type'].value_counts()
    total = len(data)

    stats = {}
    for gap_type in ['Strong Gap Up', 'Gap Up', 'Flat', 'Gap Down', 'Strong Gap Down']:
        if gap_type in counts:
            count = counts[gap_type]
            pct = (count / total) * 100
            bar = '█' * int(pct / 2)
            print(f"  {gap_type:20s} {count:5d} ({pct:5.1f}%) {bar}")
            stats[gap_type] = {'count': count, 'pct': round(pct, 1)}

    print(f"\n  Average Gap:    {data['Gap_Pct'].mean():.4f}%")
    print(f"  Gap Std Dev:    {data['Gap_Pct'].std():.4f}%")
    print(f"  Max Gap Up:     {data['Gap_Pct'].max():.2f}%")
    print(f"  Max Gap Down:   {data['Gap_Pct'].min():.2f}%")
    print(f"  Bullish Days:   {(data['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
    print(f"  Avg Daily Range:{data['Intraday_Range'].mean():.3f}%")

    return stats


def fetch_multiple(symbols_list, start='2020-01-01'):
    """Fetch data for multiple symbols at once."""
    results = {}
    for sym in symbols_list:
        data, name = get_market_data_with_gaps(sym, start=start)
        if not data.empty:
            results[name] = data
    return results


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    print("🌐 UNIVERSAL MARKET DATA FETCHER")
    print("=" * 50)

    # Test with different symbol types
    test_symbols = ['nifty', 'bitcoin', 'gold']

    for sym in test_symbols:
        data, name = get_market_data_with_gaps(sym, start='2024-01-01')
        if not data.empty:
            get_gap_statistics(data, name)
            print(f"\n  Last 3 days:")
            print(data[['Open', 'Close', 'Gap_Pct', 'Day_Direction']].tail(3))
            print()