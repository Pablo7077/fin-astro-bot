# 🔮 FIN ASTRO Bot

**Financial Astrology Research Bot for Nifty & Bank Nifty**

Uses Vedic (Jyotish) planetary calculations correlated with historical 
market data to generate research insights, gap projections, and 
intraday timing ideas.

## Features
- 📍 Accurate Vedic (Lahiri ayanamsha) planetary positions
- 🌙 Moon sign, nakshatra, tithi, and phase analysis
- 🔄 Retrograde detection and market impact analysis
- 🔥 Combustion detection
- ⭐ Yoga identification (Guru-Chandala, Gaja-Kesari, etc.)
- 📊 Historical correlation with Nifty gap patterns
- 🎯 Astro Gap Projections with confidence levels

## Quick Start
```bash
pip install -r requirements.txt
python main.py --quick              # Today's planetary analysis
python main.py --quick 2025-01-15   # Specific date
python main.py --build              # Build historical dataset (first time)
python main.py 2025-01-15           # Full projection with history
python main.py --backtest           # Full back-test report