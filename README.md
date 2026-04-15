# 🔮 FIN ASTRO BOT v2.0

**The Most Comprehensive Financial Astrology Research Engine**

Combines 12+ Vedic (Jyotish) astrological techniques with historical market data
to generate research insights, gap projections, intraday timing, and sector signals.

Works with **ANY market** — Nifty, Bank Nifty, Bitcoin, NASDAQ, Gold, individual stocks, and more.

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 📍 Planetary Positions | Vedic sidereal (Lahiri) with dignity, nakshatra, pada |
| ⭐ 20+ Yogas | Gaja-Kesari, Guru-Chandala, Kala Sarpa, Veshi, Vashi, Ubhayachari... |
| 📅 Full Panchang | Tithi, Karana, Nitya Yoga, Vara, Gandanta, Void of Course |
| ⏰ Planetary Hours | Hora table + Rahu Kaal + Abhijit Muhurta for intraday timing |
| 🔮 Vimshottari Dasha | Mahadasha/Antardasha for Nifty, Bank Nifty, Sensex |
| 📊 Ashtakavarga | Bindu-based transit scoring (astro → numbers) |
| 📐 Divisional Charts | Navamsha (D-9), Dashamsha (D-10), Vargottama detection |
| 📈 Bradley Siderograph | Composite turning-point indicator |
| 🌑 Eclipse Detection | Solar/lunar eclipses + corridor analysis |
| 🏛️ Mundane Astrology | Transits to India/Nifty birth charts |
| 🎯 KP System | Sub-lord analysis + Ruling Planets |
| 🏭 Sector Rotation | Planet → sector/commodity mapping with signals |
| 🌐 Any Symbol | Nifty, Bitcoin, TATAPOWER, AAPL, Gold, NASDAQ — anything |
| 📊 Historical Backtest | Moon sign, nakshatra, tithi, karana, retrograde hit rates |
| 📅 Reports | Daily, Weekly, Monthly auto-generated reports |
| 🖥️ Web Dashboard | Streamlit-powered browser interface |

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Quick planetary analysis (today)
python main.py --quick

# Full projection for any symbol
python main.py --project nifty
python main.py --project bitcoin 2025-03-20
python main.py --project tatapower

# Intraday hora timing
python main.py --hora

# Sector rotation signals
python main.py --sectors

# Dasha analysis
python main.py --dasha nifty

# Weekly/Monthly reports
python main.py --weekly nifty
python main.py --monthly nifty

# Build historical dataset & backtest
python main.py --build nifty
python main.py --backtest nifty

# Web dashboard
python main.py --dashboard

# Interactive menu
python main.py