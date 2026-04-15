"""
=============================================================
FIN ASTRO BOT — Market Data Module
=============================================================
Downloads Nifty / Bank Nifty historical data from Yahoo Finance.
Calculates gaps, returns, and prepares data for astro correlation.
=============================================================
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def download_market_data(symbol='^NSEI', start='2010-01-01', end=None):
    """
    Download historical daily OHLCV data for given symbol.
    ^NSEI = Nifty 50, ^NSEBANK = Bank Nifty
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')

    print(f"📊 Downloading {symbol} data from {start} to {end}...")
    data = yf.download(symbol, start=start, end=end, interval='1d',
                       progress=False)

    if data.empty:
        print(f"⚠️  No data received for {symbol}. Check symbol/internet.")
        return pd.DataFrame()

    # Flatten multi-level columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Ensure index is datetime and timezone-naive
    data.index = pd.to_datetime(data.index)
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    print(f"✅ Downloaded {len(data)} trading days.")
    return data


def calculate_gaps(data):
    """
    Calculate opening gaps and classify them.
    Gap = Today's Open - Yesterday's Close
    """
    df = data.copy()

    # Gap calculation
    df['Prev_Close'] = df['Close'].shift(1)
    df['Gap'] = df['Open'] - df['Prev_Close']
    df['Gap_Pct'] = (df['Gap'] / df['Prev_Close']) * 100

    # Classify gaps
    df['Gap_Type'] = pd.cut(
        df['Gap_Pct'],
        bins=[-float('inf'), -0.3, -0.1, 0.1, 0.3, float('inf')],
        labels=['Strong Gap Down', 'Gap Down', 'Flat', 'Gap Up', 'Strong Gap Up']
    )

    # Daily return
    df['Daily_Return'] = df['Close'].pct_change() * 100

    # Intraday range
    df['Intraday_Range'] = ((df['High'] - df['Low']) / df['Open']) * 100

    # Day direction: did price close above or below open?
    df['Day_Direction'] = np.where(df['Close'] > df['Open'], 'Bullish',
                                    np.where(df['Close'] < df['Open'], 'Bearish', 'Neutral'))

    # First half proxy: did price go up from open to mid (using high/low)
    df['Open_to_High'] = ((df['High'] - df['Open']) / df['Open']) * 100
    df['Open_to_Low'] = ((df['Low'] - df['Open']) / df['Open']) * 100

    df.dropna(subset=['Gap'], inplace=True)

    return df


def get_nifty_data(start='2010-01-01', end=None):
    """Get Nifty 50 data with gap analysis."""
    raw = download_market_data('^NSEI', start, end)
    if raw.empty:
        return pd.DataFrame()
    return calculate_gaps(raw)


def get_banknifty_data(start='2010-01-01', end=None):
    """Get Bank Nifty data with gap analysis."""
    raw = download_market_data('^NSEBANK', start, end)
    if raw.empty:
        return pd.DataFrame()
    return calculate_gaps(raw)


def get_gap_statistics(data, column='Gap_Type'):
    """Print overall gap distribution statistics."""
    if data.empty:
        print("No data to analyze.")
        return

    print("\n📈 GAP DISTRIBUTION:")
    print("-" * 40)
    counts = data[column].value_counts()
    total = len(data)
    for gap_type, count in counts.items():
        pct = (count / total) * 100
        bar = '█' * int(pct / 2)
        print(f"  {str(gap_type):20s} {count:5d} ({pct:5.1f}%) {bar}")

    print(f"\n  Average Gap: {data['Gap_Pct'].mean():.3f}%")
    print(f"  Gap Std Dev: {data['Gap_Pct'].std():.3f}%")
    print(f"  Max Gap Up:  {data['Gap_Pct'].max():.2f}%")
    print(f"  Max Gap Down:{data['Gap_Pct'].min():.2f}%")


# ── Quick Test ────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("🏦 FIN ASTRO — Market Data Module Test")
    print("=" * 50)

    # Test with last 2 years of data for quick download
    two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')

    nifty = get_nifty_data(start=two_years_ago)
    if not nifty.empty:
        get_gap_statistics(nifty)
        print(f"\n📅 Last 5 trading days:")
        print(nifty[['Open', 'Close', 'Gap_Pct', 'Gap_Type',
                      'Day_Direction']].tail())