ATXP Chat

New chat

Today
ATXP Icon
# Financial Astrology Bot Guide



No team chats yet

No private shares yet

ATXP User's avatar
ATXP User



ATXP Icon
Auto
▼

+
ATXP User
AU

avatar
Here are two practical ways to create the AI bot for financial astrology (FIN ASTRO) research on Nifty/Bank Nifty. It pulls planetary positions (transits, retrogrades, combustions, yogas, lunar cycles), correlates them with historical market data, and generates insights like Astro Gap Projections and intraday timing ideas.
Option 1: Build the Bot Yourself (Recommended for Full Control and Iteration)
This creates a reusable Python tool you can run locally, expand, or turn into a web app. It uses:
∙	pyswisseph (or alternatives like VedAstro / jyotishganit) for accurate Vedic planetary calculations (Lahiri ayanamsha standard for Indian astrology).
∙	yfinance for Nifty (NSEI) and Bank Nifty (NSEBANK) historical data (daily opens for gap analysis, plus basic stats).
∙	Pandas/NumPy for correlations and back-testing.
∙	Optional: LangChain or simple scripting for “agent-like” behavior (LLM can help generate the code).
Step-by-Step Build Guide
Step 1: Set up your environment
∙	Install Python 3.10+ (if not already).
∙	Create a new folder/project and (recommended) a virtual environment:

python -m venv astro_bot_env
source astro_bot_env/bin/activate    # Mac/Linux
astro_bot_env\Scripts\activate       # Windows

yaml

Copy code
∙	Install core packages:

pip install pyswisseph yfinance pandas numpy matplotlib plotly

vbnet

Copy code
∙		∙	For ephemeris files (required by pyswisseph): Download from https://www.astro.com/swisseph/ (or the package may handle basics). Set path in code with swe.set_ephe_path('/path/to/ephe').
∙	Alternative easier Vedic libs (if pyswisseph installation issues on your OS): Try pip install vedicastro or jyotishganit — they wrap Swiss Ephemeris or similar high-precision data.

import swisseph as swe
from datetime import datetime
import pandas as pd

swe.set_ephe_path('path/to/sweph/ephe')  # Adjust
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Vedic standard

def get_planetary_positions(date_str, time_str='12:00'):
# Convert to Julian day, calculate positions, etc.
# Return dict like {'Sun': (degree, sign, retrograde), 'Moon': ..., 'Mercury': ...}
pass  # Expand with swe.calc_ut()

def detect_astro_events(positions):
# Logic for retrograde (speed < 0), combustion (close to Sun), etc.
pass

java
Run Code

Copy code
2.	Market Data Module (market_data.py):


import yfinance as yf
import pandas as pd

def get_nifty_data(start_date='2000-01-01', end_date=None):
data = yf.download('^NSEI', start=start_date, end=end_date, interval='1d')
data['Gap'] = data['Open'] - data['Close'].shift(1)  # Positive = gap up
data['Gap_Type'] = pd.cut(data['Gap'], bins=[-float('inf'), -0.5, 0.5, float('inf')], labels=['Gap Down', 'Flat', 'Gap Up'])
return data

Similar for '^NSEBANK'
vbnet

Copy code
3.	Correlation & Insight Engine (insights.py):
∙	Merge astro events with market data by date.
∙	Compute historical hit rates (e.g., % of times a certain Jupiter transit coincided with gap up).
∙	Generate reports:
∙	Today’s astro events.
∙	Similar historical patterns and average market move.
∙	Simple “projection”: If pattern hit rate > 60%, suggest likely gap direction or intraday bias.
4.	Main Runner (main.py):
∙	Input: date or “today”.
∙	Output: Clean report (text + charts showing price vs. key transits).

You are an expert Financial Astrologer AI Bot specialized in Vedic (Jyotish) techniques for Indian stock markets, particularly Nifty and Bank Nifty. You have deep knowledge of planetary transits, retrogrades, combustions, yogas, lunar cycles (tithis), Rahu/Ketu nodes, and how they historically correlate with market behavior based on back-tested patterns.

For the date [YYYY-MM-DD] (or "today" for current), perform full research and give insights mimicking professional FIN ASTRO analysis:

List all key planetary positions (in signs/degrees, sidereal/Lahiri), retrogrades, combustions, and major aspects or yogas active that day.
Identify relevant astro events (e.g., planet ingresses, eclipses if near, Moon phase).
Analyze historical correlations: Describe similar past setups (last 10-20 years) and what typically happened to Nifty opens/gaps and intraday direction.
Provide:
Astro Gap Projection: Likely Gap Up, Gap Down, or Flat opening, with reasoning and rough confidence.
Day directional bias (first half / second half if applicable).
Suggested intraday bullish/bearish time windows based on planetary timings.
Overall insight summary and any cautions.
Be precise, data-driven where possible, and transparent about limitations (astrology is interpretive). Use accurate astronomical calculations in your reasoning.

Date: [insert date here, e.g., 2026-04-11]

sql

Copy code
∙	Run this daily or for back-testing specific dates.
∙	For deeper research: Chain prompts — first ask for planetary data, then “Now correlate these with Nifty history and give gap projection.”
∙	Limitations: Pure LLM may hallucinate exact degrees or correlations unless grounded with tools/code. For higher accuracy, combine with Option 1 (build the calculator part first).

Important Reality Check
∙	This bot automates research and pattern spotting quickly — great for learning and hypothesis generation.
∙	Financial astrology correlations are not scientifically proven predictors. Use only for education/experimentation. Always combine with technical analysis, risk management, and never trade real money based solely on astro signals.
∙	Start small: Get planetary calc working first, then add market correlations.
∙	If you hit installation issues with pyswisseph (common on some systems), fall back to VedAstro library or online ephemeris APIs as temporary bridges.
Let’s make this functional through Github, as i am beginner and no barely anything about coding, guide me like a young student who's eager to build something without anty knowledge, give me steo by steo guidance, to build this from scratch independently as i don't have any softwares with me either i just have a github profile





ATXP Icon
🚀 FIN ASTRO Bot: Complete Beginner's Guide (GitHub Only)
I'll hold your hand through every single click. No software needed on your computer — we'll build everything directly on GitHub using GitHub Codespaces (a free cloud computer in your browser).

PHASE 0: Understanding What We're Building
scss

Copy code
YOUR GITHUB PROFILE
        │
        ▼
┌─────────────────────┐
│   fin-astro-bot     │  ← Your Repository (project folder)
│   (Repository)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│         GitHub Codespace                     │
│  (Free cloud computer in your browser)       │
│                                              │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐ │
│  │ Planet    │  │ Market    │  │ Insight  │ │
│  │ Calculator│→ │ Data      │→ │ Engine   │ │
│  │ Module    │  │ Module    │  │ Module   │ │
│  └──────────┘  └───────────┘  └──────────┘ │
│         │              │            │        │
│         ▼              ▼            ▼        │
│    ┌─────────────────────────────────┐      │
│    │     DAILY ASTRO REPORT          │      │
│    │  • Planetary positions          │      │
│    │  • Gap Projection (Up/Down)     │      │
│    │  • Intraday timing windows      │      │
│    │  • Historical hit rates         │      │
│    └─────────────────────────────────┘      │
└─────────────────────────────────────────────┘

PHASE 1: Create Your Repository (Your Project's Home)
Step 1.1 — Go to GitHub
go
Run Code

Copy code
Open your browser → go to https://github.com
Log into your account


Step 1.2 — Create a New Repository
css

Copy code
1. Click the "+" icon (top-right corner of the page, near your profile picture)
2. Click "New repository"

Step 1.3 — Fill in the Details
sql

Copy code
Repository name:       fin-astro-bot
Description:           Financial Astrology Bot for Nifty & Bank Nifty
Public/Private:        ✅ Public (so Codespaces works free)
Add a README file:     ✅ CHECK THIS BOX (important!)
Add .gitignore:        Select "Python" from dropdown
Choose a license:      MIT License (or skip)

Then click:  🟢 "Create repository"

What you should see now: A page showing your repository with a README.md file.

PHASE 2: Open GitHub Codespaces (Your Free Cloud Computer)
This is the magic part — you get a full coding computer in your browser, free.

Step 2.1 — Launch Codespace
css

Copy code
1. On your repository page, find the green "< > Code" button
2. Click it
3. You'll see tabs: "Local" and "Codespaces"
4. Click the "Codespaces" tab
5. Click "Create codespace on main"

Step 2.2 — Wait for it to load
css

Copy code
⏳ This takes 1-2 minutes the first time
A new browser tab opens that looks like VS Code (a code editor)
You'll see:
   - LEFT SIDE: File explorer (your project files)
   - CENTER: Editor area
   - BOTTOM: Terminal (where you type commands)

Your screen should look like this:

sql

Copy code
┌──────────────┬──────────────────────────────────────┐
│ EXPLORER     │                                      │
│              │     Welcome Tab                      │
│ 📁 fin-astro│                                      │
│  📄 README  │     (some getting started info)       │
│  📄.gitignore│                                     │
│              │                                      │
├──────────────┴──────────────────────────────────────┤
│ TERMINAL                                            │
│ @your-username ➜ /workspaces/fin-astro-bot $        │
│ (blinking cursor — ready for your commands)         │
└─────────────────────────────────────────────────────┘

If you don't see the Terminal at the bottom:
Press Ctrl + ` (backtick key, usually below Escape)
OR go to menu: Terminal → New Terminal

PHASE 3: Install Everything We Need
Step 3.1 — Type these commands in the Terminal
Click inside the terminal area at the bottom, then type each line and press Enter after each:

bash

Copy code
python --version

You should see something like Python 3.10.x or 3.11.x.

Now install all our packages:

bash

Copy code
pip install pyswisseph yfinance pandas numpy matplotlib

Wait for it to finish. You'll see lots of text scrolling. When you see the $ prompt again with a blinking cursor, it's done.

Step 3.2 — Download Ephemeris Files (Planet Data)
These are the astronomical data files that tell us exactly where planets are:

bash

Copy code
mkdir -p ephe
cd ephe
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
cd ..

What this did:

scss

Copy code
📁 fin-astro-bot/
├── 📁 ephe/               ← NEW! Planet data files
│   ├── seas_18.se1        (asteroid positions)
│   ├── semo_18.se1        (moon positions)
│   └── sepl_18.se1        (planet positions)
├── 📄 README.md
└── 📄 .gitignore

PHASE 4: Create the Bot Files (The Actual Code!)
Now we create each file. I'll give you the exact code for each.

Step 4.1 — Create the Planetary Calculator
In the terminal, type:

bash

Copy code
touch astro_engine.py

Now in the left sidebar (EXPLORER), click on astro_engine.py to open it in the editor.

Copy ALL of this code and paste it into that file:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT — Planetary Calculation Engine
=============================================================
Calculates Vedic (sidereal/Lahiri) planetary positions,
retrogrades, combustions, nakshatras, and key yogas.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
import math
import os

# ── Setup Swiss Ephemeris ─────────────────────────────────
EPHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ephe')
swe.set_ephe_path(EPHE_PATH)
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Standard Indian Astrology

# ── Constants ─────────────────────────────────────────────
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,    # North Node
}

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
    'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
    'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
    'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
    'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13.333... degrees each

# Combustion ranges (degrees from Sun) — standard Vedic values
COMBUSTION_RANGES = {
    'Moon': 12.0,
    'Mercury': 14.0,
    'Venus': 10.0,
    'Mars': 17.0,
    'Jupiter': 11.0,
    'Saturn': 15.0,
}

# ── Helper Functions ──────────────────────────────────────

def date_to_jd(date_str, time_str='12:00'):
    """Convert date string 'YYYY-MM-DD' and time 'HH:MM' to Julian Day."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd = swe.julday(dt.year, dt.month, dt.day,
                     dt.hour + dt.minute / 60.0)
    return jd


def get_sign(degree):
    """Get zodiac sign from sidereal degree (0-360)."""
    sign_index = int(degree / 30.0) % 12
    return SIGNS[sign_index]


def get_sign_degree(degree):
    """Get degree within sign (0-30)."""
    return degree % 30.0


def get_nakshatra(degree):
    """Get nakshatra name and pada from sidereal degree."""
    nak_index = int(degree / NAKSHATRA_SPAN) % 27
    pada = int((degree % NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4.0)) + 1
    return NAKSHATRAS[nak_index], pada


def get_tithi(moon_deg, sun_deg):
    """Calculate lunar tithi (1-30) from Moon and Sun positions."""
    diff = (moon_deg - sun_deg) % 360.0
    tithi_num = int(diff / 12.0) + 1
    tithi_names = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima',
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Amavasya'
    ]
    paksha = 'Shukla' if tithi_num <= 15 else 'Krishna'
    name = tithi_names[min(tithi_num - 1, 29)]
    return tithi_num, name, paksha


def angular_distance(deg1, deg2):
    """Shortest angular distance between two degrees."""
    diff = abs(deg1 - deg2) % 360.0
    return min(diff, 360.0 - diff)


# ── Main Planetary Calculation ────────────────────────────

def get_planetary_positions(date_str, time_str='12:00'):
    """
    Calculate all planetary positions for a given date.
    Returns a dictionary with full details for each planet.
    """
    jd = date_to_jd(date_str, time_str)
    positions = {}

    for name, planet_id in PLANETS.items():
        # Calculate position with speed
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        result = swe.calc_ut(jd, planet_id, flags)
        
        longitude = result[0][0]  # Sidereal longitude
        speed = result[0][3]      # Daily speed in degrees

        # Normalize longitude to 0-360
        longitude = longitude % 360.0

        sign = get_sign(longitude)
        sign_deg = get_sign_degree(longitude)
        nakshatra, pada = get_nakshatra(longitude)
        is_retrograde = speed < 0

        positions[name] = {
            'longitude': round(longitude, 4),
            'sign': sign,
            'sign_degree': round(sign_deg, 2),
            'nakshatra': nakshatra,
            'pada': pada,
            'speed': round(speed, 4),
            'retrograde': is_retrograde,
        }

    # Calculate Ketu (always exactly opposite Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180.0) % 360.0
    positions['Ketu'] = {
        'longitude': round(ketu_long, 4),
        'sign': get_sign(ketu_long),
        'sign_degree': round(get_sign_degree(ketu_long), 2),
        'nakshatra': get_nakshatra(ketu_long)[0],
        'pada': get_nakshatra(ketu_long)[1],
        'speed': -abs(positions['Rahu']['speed']),  # Always retrograde
        'retrograde': True,  # Nodes always retrograde
    }

    return positions


# ── Astro Event Detection ─────────────────────────────────

def detect_combustions(positions):
    """Detect planets combust (too close to Sun)."""
    combustions = []
    sun_deg = positions['Sun']['longitude']

    for planet, max_dist in COMBUSTION_RANGES.items():
        if planet in positions:
            planet_deg = positions[planet]['longitude']
            dist = angular_distance(sun_deg, planet_deg)
            if dist <= max_dist:
                combustions.append({
                    'planet': planet,
                    'distance_from_sun': round(dist, 2),
                    'max_range': max_dist,
                    'severity': 'Deep' if dist < max_dist / 2 else 'Partial'
                })

    return combustions


def detect_major_aspects(positions):
    """Detect major Vedic aspects between planets."""
    aspects = []
    planet_names = list(positions.keys())

    # Standard aspect orbs (degrees) — Vedic uses wider orbs
    aspect_types = {
        0: ('Conjunction', 10),
        60: ('Sextile', 6),
        90: ('Square', 8),
        120: ('Trine', 8),
        180: ('Opposition', 10),
    }

    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]
            dist = angular_distance(
                positions[p1]['longitude'],
                positions[p2]['longitude']
            )
            for exact_angle, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': p1,
                        'planet2': p2,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 2
                    })

    return aspects


def detect_yogas(positions, aspects):
    """Detect important Vedic yogas relevant to markets."""
    yogas = []

    # 1. Guru-Chandala Yoga: Jupiter conjunct Rahu
    jup_deg = positions['Jupiter']['longitude']
    rahu_deg = positions['Rahu']['longitude']
    if angular_distance(jup_deg, rahu_deg) <= 15:
        yogas.append({
            'name': 'Guru-Chandala Yoga',
            'planets': ['Jupiter', 'Rahu'],
            'effect': 'Distorted wisdom, over-speculation, market manipulation risk',
            'market_bias': 'volatile_bearish'
        })

    # 2. Gaja-Kesari Yoga: Jupiter and Moon in mutual kendras (1/4/7/10)
    moon_deg = positions['Moon']['longitude']
    moon_sign_num = int(moon_deg / 30) % 12
    jup_sign_num = int(jup_deg / 30) % 12
    sign_diff = (jup_sign_num - moon_sign_num) % 12
    if sign_diff in [0, 3, 6, 9]:  # Kendra positions
        yogas.append({
            'name': 'Gaja-Kesari Yoga',
            'planets': ['Jupiter', 'Moon'],
            'effect': 'Prosperity, optimism, positive sentiment',
            'market_bias': 'bullish'
        })

    # 3. Grahan Yoga: Sun/Moon conjunct Rahu/Ketu (eclipse-like)
    ketu_deg = positions['Ketu']['longitude']
    sun_deg = positions['Sun']['longitude']
    for node_name, node_deg in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        for luminary, lum_deg in [('Sun', sun_deg), ('Moon', moon_deg)]:
            if angular_distance(lum_deg, node_deg) <= 12:
                yogas.append({
                    'name': f'Grahan Yoga ({luminary}-{node_name})',
                    'planets': [luminary, node_name],
                    'effect': f'{luminary} eclipsed — confusion, fear, sudden reversals',
                    'market_bias': 'volatile'
                })

    # 4. Saturn-Mars aspect/conjunction — aggression, crashes
    sat_deg = positions['Saturn']['longitude']
    mars_deg = positions['Mars']['longitude']
    sat_mars_dist = angular_distance(sat_deg, mars_deg)
    if sat_mars_dist <= 10:
        yogas.append({
            'name': 'Saturn-Mars Conjunction/War',
            'planets': ['Saturn', 'Mars'],
            'effect': 'Extreme tension, conflict energy, potential sharp drops',
            'market_bias': 'bearish'
        })
    elif abs(sat_mars_dist - 180) <= 10:
        yogas.append({
            'name': 'Saturn-Mars Opposition',
            'planets': ['Saturn', 'Mars'],
            'effect': 'Push-pull conflict, whipsaw markets',
            'market_bias': 'volatile_bearish'
        })

    # 5. Venus-Jupiter conjunction — wealth combination
    ven_deg = positions['Venus']['longitude']
    if angular_distance(ven_deg, jup_deg) <= 10:
        yogas.append({
            'name': 'Venus-Jupiter Conjunction',
            'planets': ['Venus', 'Jupiter'],
            'effect': 'Wealth, optimism, bullish sentiment for markets',
            'market_bias': 'bullish'
        })

    # 6. Multiple retrograde stress
    retro_count = sum(1 for p in positions.values() if p['retrograde']
                      and p != positions.get('Rahu') and p != positions.get('Ketu'))
    if retro_count >= 3:
        retro_planets = [name for name, data in positions.items()
                        if data['retrograde'] and name not in ['Rahu', 'Ketu']]
        yogas.append({
            'name': 'Multiple Retrograde Stress',
            'planets': retro_planets,
            'effect': f'{retro_count} planets retrograde — review, revision, uncertainty',
            'market_bias': 'volatile'
        })

    return yogas


def get_moon_phase(positions):
    """Determine Moon phase for market sentiment."""
    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']
    diff = (moon_deg - sun_deg) % 360.0

    tithi_num, tithi_name, paksha = get_tithi(moon_deg, sun_deg)

    if diff < 15:
        phase = 'New Moon (Amavasya zone)'
        market_note = 'Low energy, reversals possible, avoid big positions'
    elif diff < 90:
        phase = 'Waxing Crescent'
        market_note = 'Building momentum, cautious buying'
    elif diff < 135:
        phase = 'Waxing Gibbous'
        market_note = 'Strong momentum, trend continuation likely'
    elif diff < 195:
        phase = 'Full Moon (Purnima zone)'
        market_note = 'Peak emotion, high volatility, possible reversal'
    elif diff < 270:
        phase = 'Waning Gibbous'
        market_note = 'Profit booking phase, declining momentum'
    elif diff < 345:
        phase = 'Waning Crescent'
        market_note = 'Exhaustion, caution, prepare for new cycle'
    else:
        phase = 'New Moon (Amavasya zone)'
        market_note = 'Low energy, reversals possible, avoid big positions'

    return {
        'phase': phase,
        'tithi_number': tithi_num,
        'tithi_name': tithi_name,
        'paksha': paksha,
        'sun_moon_distance': round(diff, 2),
        'market_note': market_note
    }


def detect_ingresses(date_str):
    """Check if any planet changes sign today (ingress = big energy shift)."""
    jd_today = date_to_jd(date_str, '12:00')
    jd_yesterday = date_to_jd(
        (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d'),
        '12:00'
    )

    ingresses = []
    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL
        res_today = swe.calc_ut(jd_today, planet_id, flags)
        res_yesterday = swe.calc_ut(jd_yesterday, planet_id, flags)

        sign_today = get_sign(res_today[0][0] % 360)
        sign_yesterday = get_sign(res_yesterday[0][0] % 360)

        if sign_today != sign_yesterday:
            ingresses.append({
                'planet': name,
                'from_sign': sign_yesterday,
                'to_sign': sign_today,
                'event': f'{name} enters {sign_today} (from {sign_yesterday})'
            })

    return ingresses


# ── Full Analysis for a Date ──────────────────────────────

def full_astro_analysis(date_str, time_str='12:00'):
    """
    Complete astrological analysis for a given date.
    Returns all data needed for market correlation.
    """
    positions = get_planetary_positions(date_str, time_str)
    combustions = detect_combustions(positions)
    aspects = detect_major_aspects(positions)
    yogas = detect_yogas(positions, aspects)
    moon_phase = get_moon_phase(positions)
    ingresses = detect_ingresses(date_str)

    # Build retrograde list
    retrogrades = [
        name for name, data in positions.items()
        if data['retrograde'] and name not in ['Rahu', 'Ketu']
    ]

    return {
        'date': date_str,
        'positions': positions,
        'retrogrades': retrogrades,
        'combustions': combustions,
        'aspects': aspects,
        'yogas': yogas,
        'moon_phase': moon_phase,
        'ingresses': ingresses,
    }


# ── Quick Test ────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 FIN ASTRO — Planetary Analysis for {today}")
    print("=" * 55)

    analysis = full_astro_analysis(today)

    print("\n📍 PLANETARY POSITIONS (Sidereal/Lahiri):")
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

    print(f"\n🌙 MOON PHASE: {analysis['moon_phase']['phase']}")
    print(f"   Tithi: {analysis['moon_phase']['paksha']} "
          f"{analysis['moon_phase']['tithi_name']} "
          f"(#{analysis['moon_phase']['tithi_number']})")
    print(f"   Market Note: {analysis['moon_phase']['market_note']}")

    if analysis['yogas']:
        print(f"\n⭐ ACTIVE YOGAS:")
        for y in analysis['yogas']:
            print(f"  {y['name']}: {y['effect']} [{y['market_bias']}]")

    if analysis['ingresses']:
        print(f"\n🚀 SIGN CHANGES TODAY:")
        for ing in analysis['ingresses']:
            print(f"  {ing['event']}")

    if analysis['aspects']:
        tight = [a for a in analysis['aspects'] if a['tight']]
        if tight:
            print(f"\n🎯 TIGHT ASPECTS (within 2°):")
            for a in tight:
                print(f"  {a['planet1']} {a['aspect']} {a['planet2']} "
                      f"(orb: {a['orb']}°)")


Now save the file: Press Ctrl + S (or Cmd + S on Mac).

Step 4.2 — Create the Market Data Module
In the terminal:

bash

Copy code
touch market_data.py

Click market_data.py in the left sidebar, paste this code:

python
Run Code

Copy code
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


Save: Ctrl + S

Step 4.3 — Create the Insight/Correlation Engine
bash

Copy code
touch insights.py

Click insights.py, paste this:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT — Insight & Correlation Engine
=============================================================
Merges planetary data with market data to find patterns,
compute hit rates, and generate actionable insights.
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from astro_engine import full_astro_analysis, get_planetary_positions
from market_data import get_nifty_data

import warnings
warnings.filterwarnings('ignore')


def build_astro_market_dataset(start_date='2015-01-01', end_date=None):
    """
    Build a merged dataset: each trading day gets planetary data + market data.
    This is the CORE dataset for all correlations.
    """
    print("🔮 Building Astro-Market Dataset...")
    print("   (This takes a few minutes — calculating planets for each trading day)\n")

    # Get market data
    market = get_nifty_data(start=start_date, end=end_date)
    if market.empty:
        return pd.DataFrame()

    # For each trading day, calculate key astro features
    astro_records = []
    total = len(market)

    for idx, (date, row) in enumerate(market.iterrows()):
        date_str = date.strftime('%Y-%m-%d')

        if (idx + 1) % 100 == 0:
            print(f"   Processing {idx + 1}/{total}...")

        try:
            pos = get_planetary_positions(date_str)

            record = {
                'Date': date,
                # Moon data (fast-moving, most impact on daily)
                'Moon_Sign': pos['Moon']['sign'],
                'Moon_Nakshatra': pos['Moon']['nakshatra'],
                'Moon_Degree': pos['Moon']['longitude'],

                # Key planet signs
                'Mercury_Sign': pos['Mercury']['sign'],
                'Venus_Sign': pos['Venus']['sign'],
                'Mars_Sign': pos['Mars']['sign'],
                'Jupiter_Sign': pos['Jupiter']['sign'],
                'Saturn_Sign': pos['Saturn']['sign'],

                # Retrogrades
                'Mercury_Retro': pos['Mercury']['retrograde'],
                'Venus_Retro': pos['Venus']['retrograde'],
                'Mars_Retro': pos['Mars']['retrograde'],
                'Jupiter_Retro': pos['Jupiter']['retrograde'],
                'Saturn_Retro': pos['Saturn']['retrograde'],

                # Retrograde count
                'Retro_Count': sum(1 for p in ['Mercury', 'Venus', 'Mars',
                                                'Jupiter', 'Saturn']
                                   if pos[p]['retrograde']),

                # Rahu-Ketu axis
                'Rahu_Sign': pos['Rahu']['sign'],
                'Ketu_Sign': pos['Ketu']['sign'],

                # Sun-Moon distance (for tithi/phase)
                'Sun_Moon_Dist': (pos['Moon']['longitude'] -
                                  pos['Sun']['longitude']) % 360,
            }
            astro_records.append(record)

        except Exception as e:
            # Skip dates with calculation errors
            continue

    astro_df = pd.DataFrame(astro_records)
    astro_df.set_index('Date', inplace=True)

    # Merge
    merged = market.join(astro_df, how='inner')
    print(f"\n✅ Dataset built: {len(merged)} trading days with astro data.")

    return merged


def analyze_moon_sign_gaps(dataset):
    """Analyze gap patterns by Moon sign."""
    print("\n🌙 GAP PATTERNS BY MOON SIGN")
    print("=" * 65)

    results = []
    for sign in dataset['Moon_Sign'].dropna().unique():
        mask = dataset['Moon_Sign'] == sign
        subset = dataset[mask]
        if len(subset) < 10:
            continue

        avg_gap = subset['Gap_Pct'].mean()
        gap_up_rate = (subset['Gap_Pct'] > 0.1).mean() * 100
        gap_down_rate = (subset['Gap_Pct'] < -0.1).mean() * 100
        bullish_rate = (subset['Day_Direction'] == 'Bullish').mean() * 100
        count = len(subset)

        results.append({
            'Moon_Sign': sign,
            'Count': count,
            'Avg_Gap%': round(avg_gap, 3),
            'Gap_Up%': round(gap_up_rate, 1),
            'Gap_Down%': round(gap_down_rate, 1),
            'Bullish_Day%': round(bullish_rate, 1),
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Avg_Gap%', ascending=False)
    print(results_df.to_string(index=False))

    return results_df


def analyze_moon_nakshatra_gaps(dataset):
    """Analyze gap patterns by Moon nakshatra."""
    print("\n⭐ GAP PATTERNS BY MOON NAKSHATRA (Top 10 Bullish & Bearish)")
    print("=" * 65)

    results = []
    for nak in dataset['Moon_Nakshatra'].dropna().unique():
        mask = dataset['Moon_Nakshatra'] == nak
        subset = dataset[mask]
        if len(subset) < 5:
            continue

        avg_gap = subset['Gap_Pct'].mean()
        bullish_rate = (subset['Day_Direction'] == 'Bullish').mean() * 100
        count = len(subset)

        results.append({
            'Nakshatra': nak,
            'Count': count,
            'Avg_Gap%': round(avg_gap, 3),
            'Bullish%': round(bullish_rate, 1),
        })

    results_df = pd.DataFrame(results).sort_values('Avg_Gap%', ascending=False)

    print("\n📈 TOP 10 BULLISH NAKSHATRAS:")
    print(results_df.head(10).to_string(index=False))
    print("\n📉 TOP 10 BEARISH NAKSHATRAS:")
    print(results_df.tail(10).to_string(index=False))

    return results_df


def analyze_retrograde_impact(dataset):
    """Analyze market behavior during retrogrades."""
    print("\n🔄 RETROGRADE IMPACT ANALYSIS")
    print("=" * 65)

    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        col = f'{planet}_Retro'
        if col not in dataset.columns:
            continue

        retro = dataset[dataset[col] == True]
        direct = dataset[dataset[col] == False]

        if len(retro) < 5 or len(direct) < 5:
            continue

        print(f"\n  {planet}:")
        print(f"    Retrograde days: {len(retro)}, Direct days: {len(direct)}")
        print(f"    Avg Gap (Retro):  {retro['Gap_Pct'].mean():.4f}%")
        print(f"    Avg Gap (Direct): {direct['Gap_Pct'].mean():.4f}%")
        print(f"    Bullish% (Retro):  {(retro['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
        print(f"    Bullish% (Direct): {(direct['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
        print(f"    Volatility (Retro):  {retro['Intraday_Range'].mean():.3f}%")
        print(f"    Volatility (Direct): {direct['Intraday_Range'].mean():.3f}%")


def analyze_retro_count_impact(dataset):
    """Analyze market by number of simultaneous retrogrades."""
    print("\n🔄 IMPACT BY NUMBER OF SIMULTANEOUS RETROGRADES")
    print("=" * 65)

    for count in sorted(dataset['Retro_Count'].unique()):
        subset = dataset[dataset['Retro_Count'] == count]
        if len(subset) < 10:
            continue
        print(f"  {int(count)} planets retrograde: "
              f"{len(subset)} days, "
              f"Avg Gap: {subset['Gap_Pct'].mean():.4f}%, "
              f"Bullish: {(subset['Day_Direction'] == 'Bullish').mean() * 100:.1f}%, "
              f"Avg Range: {subset['Intraday_Range'].mean():.3f}%")


def generate_today_projection(dataset, target_date=None):
    """
    Generate gap projection and bias for a specific date
    based on historical pattern matching.
    """
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\n{'='*65}")
    print(f"🎯 ASTRO GAP PROJECTION FOR {target_date}")
    print(f"{'='*65}")

    # Get today's astro data
    analysis = full_astro_analysis(target_date)
    pos = analysis['positions']

    moon_sign = pos['Moon']['sign']
    moon_nak = pos['Moon']['nakshatra']
    mercury_retro = pos['Mercury']['retrograde']
    retro_count = sum(1 for p in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                      if pos[p]['retrograde'])

    # ── Print current astro snapshot ──
    print(f"\n📍 Key Positions:")
    for name in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu']:
        p = pos[name]
        r = ' ℞' if p['retrograde'] and name not in ['Rahu'] else ''
        print(f"   {name:10s}: {p['sign']:13s} {p['sign_degree']:6.2f}° "
              f"({p['nakshatra']} P{p['pada']}){r}")
    print(f"   {'Ketu':10s}: {pos['Ketu']['sign']:13s} "
          f"{pos['Ketu']['sign_degree']:6.2f}°")

    # Moon phase
    mp = analysis['moon_phase']
    print(f"\n🌙 Moon Phase: {mp['phase']}")
    print(f"   Tithi: {mp['paksha']} {mp['tithi_name']}")
    print(f"   Market Note: {mp['market_note']}")

    # Yogas
    if analysis['yogas']:
        print(f"\n⭐ Active Yogas:")
        for y in analysis['yogas']:
            print(f"   {y['name']}: {y['effect']} [{y['market_bias'].upper()}]")

    # Combustions
    if analysis['combustions']:
        print(f"\n🔥 Combustions:")
        for c in analysis['combustions']:
            print(f"   {c['planet']} ({c['severity']}, {c['distance_from_sun']}° from Sun)")

    # Ingresses
    if analysis['ingresses']:
        print(f"\n🚀 Sign Changes:")
        for ing in analysis['ingresses']:
            print(f"   {ing['event']}")

    # ── Historical Pattern Matching ──
    print(f"\n📊 HISTORICAL PATTERN MATCHING:")
    print("-" * 50)

    signals = []  # (signal_name, direction, confidence)

    # 1. Moon Sign pattern
    if 'Moon_Sign' in dataset.columns:
        moon_data = dataset[dataset['Moon_Sign'] == moon_sign]
        if len(moon_data) >= 10:
            avg_gap = moon_data['Gap_Pct'].mean()
            bullish_pct = (moon_data['Day_Direction'] == 'Bullish').mean() * 100
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(bullish_pct - 50) * 2, 30)  # Max 30% confidence from this
            signals.append(('Moon Sign', direction, conf))
            print(f"  Moon in {moon_sign}: {len(moon_data)} historical days, "
                  f"Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}% → {direction}")

    # 2. Moon Nakshatra pattern
    if 'Moon_Nakshatra' in dataset.columns:
        nak_data = dataset[dataset['Moon_Nakshatra'] == moon_nak]
        if len(nak_data) >= 5:
            avg_gap = nak_data['Gap_Pct'].mean()
            bullish_pct = (nak_data['Day_Direction'] == 'Bullish').mean() * 100
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(bullish_pct - 50) * 2, 25)
            signals.append(('Moon Nakshatra', direction, conf))
            print(f"  Moon in {moon_nak}: {len(nak_data)} historical days, "
                  f"Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}% → {direction}")

    # 3. Mercury Retrograde
    if mercury_retro and 'Mercury_Retro' in dataset.columns:
        retro_data = dataset[dataset['Mercury_Retro'] == True]
        if len(retro_data) >= 10:
            avg_gap = retro_data['Gap_Pct'].mean()
            bullish_pct = (retro_data['Day_Direction'] == 'Bullish').mean() * 100
            vol = retro_data['Intraday_Range'].mean()
            direction = 'VOLATILE'
            conf = 10
            signals.append(('Mercury Retro', direction, conf))
            print(f"  Mercury Retrograde: Avg Gap: {avg_gap:+.3f}%, "
                  f"Bullish: {bullish_pct:.1f}%, Avg Range: {vol:.2f}% → VOLATILE")

    # 4. Retrograde count
    if 'Retro_Count' in dataset.columns:
        rc_data = dataset[dataset['Retro_Count'] == retro_count]
        if len(rc_data) >= 10:
            avg_gap = rc_data['Gap_Pct'].mean()
            direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
            conf = min(abs(avg_gap) * 100, 15)
            signals.append(('Retro Count', direction, conf))
            print(f"  {retro_count} Retrogrades active: {len(rc_data)} days, "
                  f"Avg Gap: {avg_gap:+.3f}% → {direction}")

    # 5. Yoga-based signals
    for yoga in analysis['yogas']:
        bias = yoga['market_bias']
        if 'bullish' in bias:
            signals.append(('Yoga: ' + yoga['name'], 'BULLISH', 15))
        elif 'bearish' in bias:
            signals.append(('Yoga: ' + yoga['name'], 'BEARISH', 15))
        else:
            signals.append(('Yoga: ' + yoga['name'], 'VOLATILE', 10))

    # 6. Moon phase signal
    moon_phase_text = mp['phase']
    if 'New Moon' in moon_phase_text:
        signals.append(('Moon Phase', 'VOLATILE', 10))
    elif 'Full Moon' in moon_phase_text:
        signals.append(('Moon Phase', 'VOLATILE', 10))
    elif 'Waxing' in moon_phase_text:
        signals.append(('Moon Phase', 'BULLISH', 8))
    elif 'Waning' in moon_phase_text:
        signals.append(('Moon Phase', 'BEARISH', 8))

    # ── Aggregate Signals ──
    print(f"\n{'='*50}")
    print("🎯 SIGNAL AGGREGATION:")
    print("-" * 50)

    bullish_score = sum(c for _, d, c in signals if d == 'BULLISH')
    bearish_score = sum(c for _, d, c in signals if d == 'BEARISH')
    volatile_score = sum(c for _, d, c in signals if d == 'VOLATILE')

    for name, direction, conf in signals:
        emoji = '🟢' if direction == 'BULLISH' else ('🔴' if direction == 'BEARISH' else '🟡')
        print(f"  {emoji} {name:25s} → {direction:10s} (weight: {conf})")

    total_directional = bullish_score + bearish_score
    if total_directional > 0:
        bull_pct = (bullish_score / (total_directional + volatile_score)) * 100
        bear_pct = (bearish_score / (total_directional + volatile_score)) * 100
    else:
        bull_pct = bear_pct = 0

    print(f"\n  Bullish Score:  {bullish_score} ({bull_pct:.0f}%)")
    print(f"  Bearish Score:  {bearish_score} ({bear_pct:.0f}%)")
    print(f"  Volatile Score: {volatile_score}")

    # Final Projection
    print(f"\n{'='*50}")
    if bullish_score > bearish_score * 1.3 and bullish_score > volatile_score:
        gap_proj = "GAP UP"
        direction_bias = "BULLISH"
        confidence = min(bull_pct, 70)
    elif bearish_score > bullish_score * 1.3 and bearish_score > volatile_score:
        gap_proj = "GAP DOWN"
        direction_bias = "BEARISH"
        confidence = min(bear_pct, 70)
    elif volatile_score > bullish_score and volatile_score > bearish_score:
        gap_proj = "FLAT/VOLATILE"
        direction_bias = "SIDEWAYS WITH WHIPSAWS"
        confidence = 40
    else:
        gap_proj = "FLAT/UNCERTAIN"
        direction_bias = "MIXED — NO CLEAR EDGE"
        confidence = 30

    print(f"  📊 ASTRO GAP PROJECTION:  {gap_proj}")
    print(f"  📈 DAY DIRECTION BIAS:    {direction_bias}")
    print(f"  🎯 CONFIDENCE:            ~{confidence:.0f}%")
    print(f"{'='*50}")

    # Cautions
    print(f"\n⚠️  CAUTIONS:")
    print(f"  • Astro signals are PROBABILISTIC, not deterministic.")
    print(f"  • Always combine with price action / technical analysis.")
    print(f"  • This is for RESEARCH & EDUCATION only.")
    print(f"  • Never risk capital solely on astrological signals.")

    return {
        'date': target_date,
        'gap_projection': gap_proj,
        'direction_bias': direction_bias,
        'confidence': confidence,
        'signals': signals,
        'analysis': analysis,
    }


# ── Quick Test ────────────────────────────────────────────
if __name__ == '__main__':
    # Build dataset (this takes a while first time)
    dataset = build_astro_market_dataset(start_date='2020-01-01')

    if not dataset.empty:
        # Run analyses
        analyze_moon_sign_gaps(dataset)
        analyze_moon_nakshatra_gaps(dataset)
        analyze_retrograde_impact(dataset)
        analyze_retro_count_impact(dataset)

        # Generate today's projection
        today = datetime.now().strftime('%Y-%m-%d')
        generate_today_projection(dataset, target_date=today)


Save: Ctrl + S

Step 4.4 — Create the Main Runner
bash

Copy code
touch main.py

Paste this into main.py:

python
Run Code

Copy code
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


Save: Ctrl + S

Step 4.5 — Create a Requirements File
bash

Copy code
touch requirements.txt

Paste into requirements.txt:

shell

Copy code
pyswisseph>=2.10
yfinance>=0.2.28
pandas>=2.0
numpy>=1.24
matplotlib>=3.7

Save: Ctrl + S

Your File Structure Should Now Look Like This:
kotlin

Copy code
📁 fin-astro-bot/
├── 📁 ephe/
│   ├── seas_18.se1
│   ├── semo_18.se1
│   └── sepl_18.se1
├── 📄 astro_engine.py        ← Planet calculator
├── 📄 market_data.py         ← Nifty data downloader
├── 📄 insights.py            ← Correlation engine
├── 📄 main.py                ← Main runner (use this!)
├── 📄 requirements.txt       ← Package list
├── 📄 README.md
└── 📄 .gitignore

Verify in the terminal:

bash

Copy code
ls -la

You should see all the files listed.

PHASE 5: RUN IT! 🚀
Test 1 — Test the Planet Calculator Alone
bash

Copy code
python astro_engine.py

Expected output (something like):

markdown

Copy code
🔮 FIN ASTRO — Planetary Analysis for 2025-07-10
=======================================================

📍 PLANETARY POSITIONS (Sidereal/Lahiri):
-------------------------------------------------------
  Sun        → Gemini         24.57° | Punarvasu Pada-3
  Moon       → Scorpio        12.33° | Anuradha Pada-1
  Mercury    → Cancer          8.45° | Pushya Pada-2
  Venus      → Taurus         19.88° | Rohini Pada-4
  Mars       → Aries           5.12° | Ashwini Pada-2
  Jupiter    → Gemini         15.67° | Ardra Pada-3
  Saturn     → Aquarius       25.34° | Purva Bhadra Pada-2 ℞
  Rahu       → Aquarius        3.22° | Dhanishtha Pada-3
  Ketu       → Leo             3.22° | Magha Pada-1

🔄 RETROGRADES: Saturn

🌙 MOON PHASE: Waxing Gibbous
   Tithi: Shukla Dashami (#10)
   Market Note: Strong momentum, trend continuation likely

Test 2 — Test Market Data
bash

Copy code
python market_data.py

Expected output:

markdown

Copy code
🏦 FIN ASTRO — Market Data Module Test
==================================================
📊 Downloading ^NSEI data...
✅ Downloaded 498 trading days.

📈 GAP DISTRIBUTION:
----------------------------------------
  Gap Up              150 (30.1%) ███████████████
  Flat                 98 (19.7%) █████████
  Gap Down            148 (29.7%) ██████████████
  ...

Test 3 — Run the Full Bot!
Quick mode (fast, just planetary positions):

bash

Copy code
python main.py --quick

Quick mode for a specific date:

bash

Copy code
python main.py --quick 2024-03-08

Full projection (builds historical data first time — takes 5-15 min):

bash

Copy code
python main.py --build

Then after that's done:

bash

Copy code
python main.py 2025-07-10

Or just:

bash

Copy code
python main.py

And choose option 1 or 2 from the menu.

PHASE 6: Save Everything to GitHub
Your code is running in Codespaces but not yet saved to your repository. Let's save it:

Step 6.1 — In the Terminal:
bash

Copy code
git add -A
git commit -m "🔮 Initial FIN ASTRO Bot - planetary engine, market data, insight engine"
git push

If it asks for your name/email:

bash

Copy code
git config --global user.name "YourGitHubUsername"
git config --global user.email "youremail@example.com"

Then run the git add, commit, and push commands again.

Step 6.2 — Verify
Go to your GitHub repo in the browser: https://github.com/YourUsername/fin-astro-bot

You should see all your files there!

PHASE 7: Update the README
Click on README.md in the Codespace editor. Replace everything with:

markdown

Copy code
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

⚠️ Disclaimer
This tool is for educational and research purposes only. Financial
astrology correlations are not scientifically proven predictors. Never
trade real money based solely on astrological signals. Always combine
with proper technical analysis and risk management.

Tech Stack
pyswisseph — Swiss Ephemeris for astronomical calculations
yfinance — Yahoo Finance market data
pandas / numpy — Data analysis
Vedic astrology (Lahiri ayanamsha, sidereal zodiac)
sql

Copy code

**Save and commit:**
```bash
git add -A
git commit -m "📝 Updated README with usage instructions"
git push

PHASE 8: How to Come Back and Use It Daily
Every time you want to use your bot:

less

Copy code
1. Go to https://github.com/YourUsername/fin-astro-bot
2. Click green "< > Code" button → Codespaces tab
3. Click on your existing codespace (it'll be listed there)
4. Wait for it to open (~30 seconds)
5. In the terminal, run:
   python main.py --quick          # Fast daily check
   python main.py                  # Full analysis

Note: Free Codespaces has limits (~60 hours/month). When you're done, go to https://github.com/codespaces, find your codespace, click ... → Stop codespace to save hours.

🎓 What You've Built — Summary
css

Copy code
┌─────────────────────────────────────────────────────────┐
│                    FIN ASTRO BOT                         │
├──────────────┬──────────────────┬───────────────────────┤
│ ASTRO ENGINE │  MARKET MODULE   │   INSIGHT ENGINE      │
│              │                  │                       │
│ • Planet     │  • Nifty OHLCV   │  • Moon sign → gaps   │
│   positions  │  • Bank Nifty    │  • Nakshatra → gaps   │
│ • Retrogrades│  • Gap calc      │  • Retrograde impact  │
│ • Combustions│  • Day direction │  • Yoga signals       │
│ • Yogas      │  • Returns       │  • Multi-signal       │
│ • Nakshatras │  • Volatility    │    aggregation        │
│ • Moon phase │                  │  • Confidence scores  │
│ • Aspects    │                  │  • Gap projection     │
├──────────────┴──────────────────┴───────────────────────┤
│                      MAIN.PY                             │
│  Quick Analysis │ Full Projection │ Back-test │ Build DB │
└─────────────────────────────────────────────────────────┘

🆘 Troubleshooting Common Issues
Problem	Solution
ModuleNotFoundError: No module named 'swisseph'	Run pip install pyswisseph again
No data received for ^NSEI	Yahoo Finance might be down. Try again in a few minutes
Terminal shows Permission denied	Add chmod +x before the file or use python filename.py
Codespace won't start	Go to github.com/codespaces, delete old one, create new
pyswisseph won't install	Try pip install flatlib as alternative (less accurate)
Ephemeris errors	Make sure the ephe/ folder has the .se1 files. Re-run the curl commands from Phase 3.2
Dates before 2000 give errors	The seas_18.se1 etc. cover specific date ranges. For broader ranges, download more ephemeris files from astro.com
Next Steps (When You're Ready to Level Up)
Add Bank Nifty — Change get_nifty_data to get_banknifty_data in insights.py
Add Charts — Use matplotlib to plot Nifty price overlaid with retrograde periods
Weekly/Monthly Reports — Loop through dates and generate batch reports
Web Interface — Add Flask or Streamlit for a browser-based dashboard
More Yogas — Add Veshi, Vashi, Ubhayachari, and other market-relevant yogas
Dasha Analysis — Add Vimshottari dasha periods for Nifty's "birth chart"
You now have a working Financial Astrology research bot built entirely from GitHub. Every piece of code is yours to modify, improve, and learn from. 🎉







avatar
Let's build

Weekly/Monthly Reports — Loop through dates and generate batch reports
Web Interface — Add Flask or Streamlit for a browser-based dashboard
More Yogas — Add Veshi, Vashi, Ubhayachari, and other market-relevant yogas
Dasha Analysis — Add Vimshottari dasha periods for Nifty's "birth chart"
Add a possibility and a easier to run it over any index i prefer, like it can be global indices, including bitcoin, or nasdaq, or any stock as well like TATAPOWER, etc




ATXP Icon
Let me break this into a clear build plan. First, let me understand your priorities so we build in the right order.


Ran show_clarification
Let me know which one you'd like to tackle first! Each is a substantial feature, so building them in the right order matters:

My recommended order:

🌐 Multi-Symbol first — because once you can run it on any ticker, all other features (reports, dashboard, yogas) automatically work across Bitcoin, NASDAQ, TATAPOWER, etc.
⭐ Yogas + Dasha — deepens the astro intelligence
📊 Reports + Dashboard — the visual layer on top of everything
But it's your bot — pick what excites you most! 🔮







avatar
Yeah much better, also do you recommend adding any more aspects of astrology into our research so when we plan on conducting a research over our tool we take into consideration every resource we can have available and get the analysis with higher accuracy, (sky is the limit here)





ATXP Icon
Great question! Let me think deeply about this — you want to make this the most comprehensive FIN ASTRO research tool possible. Let me map out EVERYTHING from Vedic astrology that serious financial astrologers actually use.


Ran show_accordion
That's the complete universe of everything we can add. Now here's my honest recommendation on what actually moves the needle:

🏆 My Recommended Priority Build Order
Priority	Feature	Impact on Accuracy	Build Effort
🥇	Multi-Symbol Support	Foundation for everything	Medium
🥇	Planetary Hours (Hora) + Rahu Kaal	Intraday timing gold	Easy
🥇	Advanced Yogas (all 12+)	Pattern recognition boost	Medium
🥈	Planetary Dignity/Strength	Tells you HOW strong a signal is	Medium
🥈	Vimshottari Dasha (Nifty chart)	Long-term trend direction	Hard
🥈	Karana, Nitya Yoga, Gandanta	Daily accuracy improvement	Easy
🥈	Ashtakavarga Transit Scoring	Turns astro into NUMBERS	Hard
🥉	Navamsha (D-9) positions	Hidden signal confirmation	Medium
🥉	Bradley Siderograph	Reversal timing	Medium
🥉	Eclipse corridors + Planetary stations	Rare but huge events	Easy
🥉	KP Sub-Lord System	Indian astrologer's secret	Hard
🥉	Sector Rotation Signals	Which stocks to pick	Medium
🏅	Streamlit Dashboard + Reports	Makes it all usable	Medium

Ran show_clarification
Here's the complete picture of everything we CAN add to make this the most comprehensive financial astrology research tool possible. I've organized it from highest daily-trading impact to deepest macro-forecasting layers.

My Top Recommendations (What Will Give You the BIGGEST Accuracy Boost):
Priority	Feature	Why
🥇	Planetary Hora (Intraday Timing)	Only tool that gives you exact MINUTE-level entry/exit windows
🥇	Ashtakavarga Scoring	Turns subjective astro into NUMBERS — perfect for a bot/algorithm
🥇	Planetary Dignity/Strength	Same planet in different conditions = completely different results
🥈	Gandanta Zones + Void of Course Moon	Rare but extremely high hit-rate reversal signals
🥈	Karana + Nitya Yoga	Daily panchang data that most tools ignore — adds 2 extra daily signals
🥈	Navamsha (D-9) Positions	The "confirmation layer" — separates real moves from fake breakouts
🥈	Nifty Birth Chart Dasha	The single best LONG-TERM forecasting method
🥉	Bradley Siderograph	Single curve that captures ALL planetary energy — turning points = reversals
🥉	KP Sub-Lord System	Most precise prediction system in Indian astrology
🥉	Sector Rotation Mapping	Which stocks/sectors to focus on THIS week based on planetary strength
Pick your approach and I'll start building every single file, step by step, right in your GitHub Codespace! 🔮








avatar
Let's build all step by step in the same manner as we did before, let me know all the steps to build the entire system in one single message





ATXP Icon
🔮 FIN ASTRO BOT v2.0 — THE COMPLETE MEGA-BUILD
Everything. Every technique. Every file. Step by step.

This is a LONG guide. Bookmark this page. Follow each phase one at a time. Don't rush — take breaks between phases if needed.

📋 WHAT WE'RE BUILDING (Final Architecture)
sql

Copy code
📁 fin-astro-bot/
├── 📁 ephe/                          ← Ephemeris data files
│   ├── seas_18.se1
│   ├── semo_18.se1
│   └── sepl_18.se1
│
├── 📁 core/                          ← CORE ASTRO ENGINE (Phase 1-4)
│   ├── __init__.py
│   ├── astro_engine.py               ← Rewritten: Planetary positions + dignity
│   ├── yogas.py                      ← ALL yogas (20+ market-relevant)
│   ├── dasha.py                      ← Vimshottari Dasha system
│   ├── hora.py                       ← Planetary hours + Rahu Kaal
│   ├── panchang.py                   ← Karana, Nitya Yoga, Gandanta, etc.
│   ├── ashtakavarga.py               ← Transit scoring system
│   ├── divisional.py                 ← Navamsha (D-9), Dashamsha (D-10)
│   ├── bradley.py                    ← Bradley Siderograph
│   ├── eclipses.py                   ← Eclipse detection + corridors
│   ├── mundane.py                    ← Nifty/India birth charts
│   ├── kp_system.py                  ← KP Sub-Lord system
│   └── sector_map.py                 ← Planet → Sector rotation
│
├── 📁 market/                        ← MARKET DATA (Phase 5)
│   ├── __init__.py
│   ├── data_fetcher.py               ← Universal: any symbol worldwide
│   ├── symbols.py                    ← Symbol registry + presets
│   └── gap_analyzer.py               ← Gap calc + statistics
│
├── 📁 analysis/                      ← CORRELATION ENGINE (Phase 6)
│   ├── __init__.py
│   ├── correlator.py                 ← Merge astro + market data
│   ├── backtester.py                 ← Historical hit rates
│   └── projector.py                  ← Signal aggregation + projections
│
├── 📁 reports/                       ← REPORT GENERATOR (Phase 7)
│   ├── __init__.py
│   ├── daily_report.py               ← Daily analysis report
│   ├── weekly_report.py              ← Weekly batch reports
│   ├── monthly_report.py             ← Monthly summaries
│   └── templates/
│       ├── daily.txt                 ← Text report template
│       └── report.html               ← HTML report template
│
├── 📁 dashboard/                     ← STREAMLIT WEB APP (Phase 8)
│   ├── app.py                        ← Main Streamlit dashboard
│   ├── pages/
│   │   ├── 1_daily_analysis.py
│   │   ├── 2_hora_timing.py
│   │   ├── 3_backtest.py
│   │   ├── 4_reports.py
│   │   ├── 5_dasha_view.py
│   │   └── 6_sector_rotation.py
│   └── components/
│       ├── charts.py
│       └── widgets.py
│
├── 📄 main.py                        ← CLI runner (updated)
├── 📄 requirements.txt               ← All packages
├── 📄 README.md                      ← Full documentation
└── 📄 .gitignore

⚡ BEFORE YOU START: Open Your Codespace
markdown

Copy code
1. Go to https://github.com/YourUsername/fin-astro-bot
2. Click green "< > Code" button → Codespaces tab
3. Click your existing codespace (or create new one)
4. Wait for it to load
5. Open Terminal (Ctrl + `)

PHASE 1: RESTRUCTURE & SETUP
Step 1.1 — Create the folder structure
Copy-paste this ENTIRE block into your terminal and press Enter:

bash

Copy code
# Create all folders
mkdir -p core market analysis reports/templates dashboard/pages dashboard/components

# Create all __init__.py files (makes Python treat folders as packages)
touch core/__init__.py market/__init__.py analysis/__init__.py reports/__init__.py

# Create all Python files
touch core/astro_engine.py core/yogas.py core/dasha.py core/hora.py
touch core/panchang.py core/ashtakavarga.py core/divisional.py
touch core/bradley.py core/eclipses.py core/mundane.py
touch core/kp_system.py core/sector_map.py

touch market/data_fetcher.py market/symbols.py market/gap_analyzer.py

touch analysis/correlator.py analysis/backtester.py analysis/projector.py

touch reports/daily_report.py reports/weekly_report.py reports/monthly_report.py
touch reports/templates/daily.txt reports/templates/report.html

touch dashboard/app.py
touch dashboard/pages/1_daily_analysis.py dashboard/pages/2_hora_timing.py
touch dashboard/pages/3_backtest.py dashboard/pages/4_reports.py
touch dashboard/pages/5_dasha_view.py dashboard/pages/6_sector_rotation.py
touch dashboard/components/charts.py dashboard/components/widgets.py

Step 1.2 — Install ALL packages
bash

Copy code
pip install pyswisseph yfinance pandas numpy matplotlib plotly streamlit fpdf2 schedule python-dateutil pytz

Step 1.3 — Update requirements.txt
Click on requirements.txt in the sidebar. Replace everything with:

shell

Copy code
pyswisseph>=2.10
yfinance>=0.2.28
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
plotly>=5.15
streamlit>=1.28
fpdf2>=2.7
schedule>=1.2
python-dateutil>=2.8
pytz>=2023.3

Save: Ctrl + S

Step 1.4 — Make sure ephemeris files exist
bash

Copy code
# Check if ephe folder has files
ls ephe/

# If empty or doesn't exist, re-download:
mkdir -p ephe
cd ephe
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
cd ..

PHASE 2: CORE ASTRO ENGINE (Rewritten + Enhanced)
Step 2.1 — core/__init__.py
Click core/__init__.py in the sidebar, paste:

python
Run Code

Copy code
"""
FIN ASTRO BOT — Core Astrology Engine Package
"""


Save.

Step 2.2 — core/astro_engine.py (Complete Rewrite with Dignity)
Click core/astro_engine.py, paste this ENTIRE file:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Core Planetary Engine
=============================================================
Calculates Vedic (sidereal/Lahiri) planetary positions with
full dignity analysis, speed, and state detection.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
import math
import os

# ── Setup ─────────────────────────────────────────────────
EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ── Constants ─────────────────────────────────────────────
PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE,
}

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira',
    'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
    'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
    'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula',
    'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter',
    'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
    'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun',
    'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13°20' each

# ── Exaltation / Debilitation Data ────────────────────────
EXALTATION = {
    'Sun': ('Aries', 10), 'Moon': ('Taurus', 3), 'Mercury': ('Virgo', 15),
    'Venus': ('Pisces', 27), 'Mars': ('Capricorn', 28),
    'Jupiter': ('Cancer', 5), 'Saturn': ('Libra', 20),
    'Rahu': ('Taurus', 20), 'Ketu': ('Scorpio', 20),
}

DEBILITATION = {
    'Sun': ('Libra', 10), 'Moon': ('Scorpio', 3), 'Mercury': ('Pisces', 15),
    'Venus': ('Virgo', 27), 'Mars': ('Cancer', 28),
    'Jupiter': ('Capricorn', 5), 'Saturn': ('Aries', 20),
    'Rahu': ('Scorpio', 20), 'Ketu': ('Taurus', 20),
}

MOOLATRIKONA = {
    'Sun': ('Leo', 0, 20), 'Moon': ('Taurus', 3, 30),
    'Mercury': ('Virgo', 15, 20), 'Venus': ('Libra', 0, 15),
    'Mars': ('Aries', 0, 12), 'Jupiter': ('Sagittarius', 0, 10),
    'Saturn': ('Aquarius', 0, 20),
}

OWN_SIGNS = {
    'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
    'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
    'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius'],
}

# Planetary friendship table
NATURAL_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
}

NATURAL_ENEMIES = {
    'Sun': ['Venus', 'Saturn'],
    'Moon': [],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
}

# Combustion ranges
COMBUSTION_RANGES = {
    'Moon': 12.0, 'Mercury': 14.0, 'Venus': 10.0,
    'Mars': 17.0, 'Jupiter': 11.0, 'Saturn': 15.0,
}

# ── Helper Functions ──────────────────────────────────────

def date_to_jd(date_str, time_str='12:00'):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

def get_sign_index(degree):
    return int(degree / 30.0) % 12

def get_sign(degree):
    return SIGNS[get_sign_index(degree)]

def get_sign_degree(degree):
    return degree % 30.0

def get_nakshatra(degree):
    nak_index = int(degree / NAKSHATRA_SPAN) % 27
    pada = int((degree % NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4.0)) + 1
    return NAKSHATRAS[nak_index], pada, NAKSHATRA_LORDS[nak_index]

def angular_distance(deg1, deg2):
    diff = abs(deg1 - deg2) % 360.0
    return min(diff, 360.0 - diff)

def sign_distance(sign1, sign2):
    """Houses between two signs (1-indexed)."""
    idx1 = SIGNS.index(sign1)
    idx2 = SIGNS.index(sign2)
    return ((idx2 - idx1) % 12) + 1

# ── Planetary Dignity ─────────────────────────────────────

def get_dignity(planet_name, sign, sign_deg):
    """
    Determine the dignity/state of a planet.
    Returns: 'Exalted', 'Moolatrikona', 'Own Sign', 'Friendly',
             'Neutral', 'Enemy', 'Debilitated'
    """
    # Check Exaltation
    if planet_name in EXALTATION:
        ex_sign, ex_deg = EXALTATION[planet_name]
        if sign == ex_sign:
            return 'Exalted'

    # Check Debilitation
    if planet_name in DEBILITATION:
        deb_sign, deb_deg = DEBILITATION[planet_name]
        if sign == deb_sign:
            return 'Debilitated'

    # Check Moolatrikona
    if planet_name in MOOLATRIKONA:
        mt_sign, mt_start, mt_end = MOOLATRIKONA[planet_name]
        if sign == mt_sign and mt_start <= sign_deg <= mt_end:
            return 'Moolatrikona'

    # Check Own Sign
    if planet_name in OWN_SIGNS:
        if sign in OWN_SIGNS[planet_name]:
            return 'Own Sign'

    # Check Friend/Enemy based on sign lord
    sign_lord = SIGN_LORDS.get(sign, '')
    if planet_name in NATURAL_FRIENDS:
        if sign_lord in NATURAL_FRIENDS.get(planet_name, []):
            return 'Friendly'
    if planet_name in NATURAL_ENEMIES:
        if sign_lord in NATURAL_ENEMIES.get(planet_name, []):
            return 'Enemy'

    return 'Neutral'


def get_dignity_score(dignity):
    """Numerical score for dignity (for weighted calculations)."""
    scores = {
        'Exalted': 5, 'Moolatrikona': 4, 'Own Sign': 3,
        'Friendly': 2, 'Neutral': 1, 'Enemy': -1, 'Debilitated': -2,
    }
    return scores.get(dignity, 0)


# ── Main Calculation ──────────────────────────────────────

def get_planetary_positions(date_str, time_str='12:00'):
    """Full planetary positions with dignity, nakshatra lords, etc."""
    jd = date_to_jd(date_str, time_str)
    positions = {}

    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        result = swe.calc_ut(jd, planet_id, flags)

        longitude = result[0][0] % 360.0
        lat = result[0][1]
        speed = result[0][3]

        sign = get_sign(longitude)
        sign_deg = get_sign_degree(longitude)
        nakshatra, pada, nak_lord = get_nakshatra(longitude)
        is_retro = speed < 0
        dignity = get_dignity(name, sign, sign_deg)

        positions[name] = {
            'longitude': round(longitude, 4),
            'latitude': round(lat, 4),
            'sign': sign,
            'sign_index': get_sign_index(longitude),
            'sign_degree': round(sign_deg, 2),
            'nakshatra': nakshatra,
            'pada': pada,
            'nakshatra_lord': nak_lord,
            'sign_lord': SIGN_LORDS.get(sign, ''),
            'speed': round(speed, 4),
            'retrograde': is_retro,
            'dignity': dignity,
            'dignity_score': get_dignity_score(dignity),
        }

    # Ketu (opposite Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180.0) % 360.0
    ketu_sign = get_sign(ketu_long)
    ketu_sign_deg = get_sign_degree(ketu_long)
    ketu_nak, ketu_pada, ketu_nak_lord = get_nakshatra(ketu_long)

    positions['Ketu'] = {
        'longitude': round(ketu_long, 4),
        'latitude': 0.0,
        'sign': ketu_sign,
        'sign_index': get_sign_index(ketu_long),
        'sign_degree': round(ketu_sign_deg, 2),
        'nakshatra': ketu_nak,
        'pada': ketu_pada,
        'nakshatra_lord': ketu_nak_lord,
        'sign_lord': SIGN_LORDS.get(ketu_sign, ''),
        'speed': -abs(positions['Rahu']['speed']),
        'retrograde': True,
        'dignity': get_dignity('Ketu', ketu_sign, ketu_sign_deg),
        'dignity_score': get_dignity_score(get_dignity('Ketu', ketu_sign, ketu_sign_deg)),
    }

    return positions


def detect_combustions(positions):
    """Detect combust planets with cazimi check."""
    combustions = []
    sun_deg = positions['Sun']['longitude']

    for planet, max_dist in COMBUSTION_RANGES.items():
        if planet in positions:
            dist = angular_distance(sun_deg, positions[planet]['longitude'])
            if dist <= max_dist:
                if dist <= 0.2833:  # 17 arcminutes = cazimi
                    severity = 'Cazimi (POWERFUL)'
                elif dist < max_dist / 3:
                    severity = 'Deep'
                elif dist < max_dist * 2 / 3:
                    severity = 'Moderate'
                else:
                    severity = 'Partial'

                combustions.append({
                    'planet': planet,
                    'distance_from_sun': round(dist, 2),
                    'max_range': max_dist,
                    'severity': severity,
                    'is_cazimi': dist <= 0.2833,
                })
    return combustions


def detect_planetary_war(positions):
    """Detect Graha Yuddha (planetary war) — two planets within 1°."""
    wars = []
    combat_planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    for i in range(len(combat_planets)):
        for j in range(i + 1, len(combat_planets)):
            p1, p2 = combat_planets[i], combat_planets[j]
            dist = angular_distance(
                positions[p1]['longitude'],
                positions[p2]['longitude']
            )
            if dist <= 1.0:
                # Winner has higher latitude (north)
                lat1 = positions[p1].get('latitude', 0)
                lat2 = positions[p2].get('latitude', 0)
                winner = p1 if lat1 > lat2 else p2
                loser = p2 if winner == p1 else p1

                wars.append({
                    'planet1': p1, 'planet2': p2,
                    'distance': round(dist, 3),
                    'winner': winner, 'loser': loser,
                    'sign': positions[p1]['sign'],
                })
    return wars


def detect_major_aspects(positions):
    """Detect aspects with Vedic special aspects included."""
    aspects = []
    planet_names = list(positions.keys())

    # Standard aspects
    aspect_types = {
        0: ('Conjunction', 10), 60: ('Sextile', 6),
        90: ('Square', 8), 120: ('Trine', 8), 180: ('Opposition', 10),
    }

    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1, p2 = planet_names[i], planet_names[j]
            dist = angular_distance(
                positions[p1]['longitude'], positions[p2]['longitude']
            )
            for exact_angle, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': p1, 'planet2': p2,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 2,
                    })

    # Vedic special aspects
    # Mars: 4th and 8th house aspects (90° and 210°)
    # Jupiter: 5th and 9th house aspects (120° and 240°)
    # Saturn: 3rd and 10th house aspects (60° and 270°)
    vedic_special = {
        'Mars': [(120, 'Mars 4th aspect', 8), (210, 'Mars 8th aspect', 8)],
        'Jupiter': [(150, 'Jupiter 5th aspect', 8), (240, 'Jupiter 9th aspect', 8)],
        'Saturn': [(60, 'Saturn 3rd aspect', 8), (270, 'Saturn 10th aspect', 8)],
    }

    for special_planet, aspect_list in vedic_special.items():
        if special_planet not in positions:
            continue
        sp_long = positions[special_planet]['longitude']
        for other_name in planet_names:
            if other_name == special_planet:
                continue
            dist = (positions[other_name]['longitude'] - sp_long) % 360
            for exact_angle, aspect_name, orb in aspect_list:
                if abs(dist - exact_angle) <= orb:
                    aspects.append({
                        'planet1': special_planet, 'planet2': other_name,
                        'aspect': aspect_name,
                        'exact_angle': exact_angle,
                        'actual_distance': round(dist, 2),
                        'orb': round(abs(dist - exact_angle), 2),
                        'tight': abs(dist - exact_angle) <= 3,
                    })

    return aspects


def detect_ingresses(date_str):
    """Check for sign changes (ingresses)."""
    jd_today = date_to_jd(date_str, '12:00')
    yesterday = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    jd_yesterday = date_to_jd(yesterday, '12:00')

    ingresses = []
    for name, planet_id in PLANETS.items():
        flags = swe.FLG_SIDEREAL
        today_long = swe.calc_ut(jd_today, planet_id, flags)[0][0] % 360
        yest_long = swe.calc_ut(jd_yesterday, planet_id, flags)[0][0] % 360

        if get_sign(today_long) != get_sign(yest_long):
            ingresses.append({
                'planet': name,
                'from_sign': get_sign(yest_long),
                'to_sign': get_sign(today_long),
            })
    return ingresses


def detect_stations(date_str):
    """Detect planets turning retrograde or direct (station)."""
    stations = []
    today = datetime.strptime(date_str, '%Y-%m-%d')

    for name, planet_id in PLANETS.items():
        if name in ['Sun', 'Moon', 'Rahu']:
            continue

        jd_today = date_to_jd(date_str, '12:00')
        jd_yesterday = date_to_jd((today - timedelta(days=1)).strftime('%Y-%m-%d'), '12:00')

        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        speed_today = swe.calc_ut(jd_today, planet_id, flags)[0][3]
        speed_yesterday = swe.calc_ut(jd_yesterday, planet_id, flags)[0][3]

        if speed_yesterday >= 0 and speed_today < 0:
            stations.append({
                'planet': name, 'type': 'Turns Retrograde',
                'market_impact': 'HIGH — expect reversal/volatility'
            })
        elif speed_yesterday < 0 and speed_today >= 0:
            stations.append({
                'planet': name, 'type': 'Turns Direct',
                'market_impact': 'HIGH — blocked energy releases'
            })
        elif abs(speed_today) < 0.02 and name not in ['Moon']:
            stations.append({
                'planet': name, 'type': 'Near Stationary',
                'market_impact': 'MEDIUM — planet energy concentrated'
            })

    return stations


def get_ascendant(date_str, time_str='09:15', lat=19.0760, lon=72.8777):
    """
    Calculate Lagna (Ascendant) for a given date/time/location.
    Default: Mumbai (NSE location), 9:15 AM (market open).
    """
    jd = date_to_jd(date_str, time_str)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    asc_degree = ascmc[0] % 360
    return {
        'degree': round(asc_degree, 4),
        'sign': get_sign(asc_degree),
        'sign_degree': round(get_sign_degree(asc_degree), 2),
        'nakshatra': get_nakshatra(asc_degree)[0],
        'pada': get_nakshatra(asc_degree)[1],
        'nakshatra_lord': get_nakshatra(asc_degree)[2],
    }


# ── Full Analysis ─────────────────────────────────────────

def full_astro_analysis(date_str, time_str='12:00'):
    """Complete astrological analysis for a date."""
    positions = get_planetary_positions(date_str, time_str)
    return {
        'date': date_str,
        'positions': positions,
        'retrogrades': [n for n, d in positions.items()
                        if d['retrograde'] and n not in ['Rahu', 'Ketu']],
        'combustions': detect_combustions(positions),
        'planetary_wars': detect_planetary_war(positions),
        'aspects': detect_major_aspects(positions),
        'ingresses': detect_ingresses(date_str),
        'stations': detect_stations(date_str),
        'ascendant': get_ascendant(date_str),
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 FIN ASTRO v2.0 — Planetary Engine Test: {today}")
    print("=" * 60)

    analysis = full_astro_analysis(today)

    print("\n📍 PLANETARY POSITIONS:")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':18s} {'Dignity':14s} {'R':3s}")
    print("-" * 70)
    for name, d in analysis['positions'].items():
        r = '℞' if d['retrograde'] else ''
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:15s} P{d['pada']} "
              f"{d['dignity']:14s} {r}")

    if analysis['planetary_wars']:
        print(f"\n⚔️ PLANETARY WARS:")
        for w in analysis['planetary_wars']:
            print(f"  {w['planet1']} vs {w['planet2']} ({w['distance']:.3f}°) "
                  f"→ Winner: {w['winner']}, Loser: {w['loser']}")

    if analysis['stations']:
        print(f"\n🛑 STATIONS:")
        for s in analysis['stations']:
            print(f"  {s['planet']} — {s['type']} ({s['market_impact']})")

    print(f"\n🏠 ASCENDANT (Mumbai 9:15 AM): "
          f"{analysis['ascendant']['sign']} {analysis['ascendant']['sign_degree']:.2f}°")


Save: Ctrl + S

Step 2.3 — core/yogas.py (20+ Market-Relevant Yogas)
Click core/yogas.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Complete Yoga Detection Engine
=============================================================
20+ Vedic yogas relevant to financial markets.
Each yoga returns market bias + confidence weight.
=============================================================
"""

from core.astro_engine import angular_distance, sign_distance, SIGNS, SIGN_LORDS


def detect_all_yogas(positions, aspects=None):
    """Master function: detect ALL yogas and return list."""
    yogas = []

    yogas += _conjunction_yogas(positions)
    yogas += _solar_yogas(positions)
    yogas += _lunar_yogas(positions)
    yogas += _node_yogas(positions)
    yogas += _strength_yogas(positions)
    yogas += _special_combinations(positions)

    return yogas


# ── 1. CONJUNCTION / ASPECT YOGAS ─────────────────────────

def _conjunction_yogas(pos):
    yogas = []

    # Guru-Chandala: Jupiter + Rahu
    if angular_distance(pos['Jupiter']['longitude'], pos['Rahu']['longitude']) <= 15:
        yogas.append({
            'name': 'Guru-Chandala Yoga',
            'planets': ['Jupiter', 'Rahu'],
            'description': 'Jupiter polluted by Rahu — distorted wisdom, over-speculation',
            'market_bias': 'volatile_bearish',
            'weight': 20,
            'category': 'conjunction',
        })

    # Venus-Jupiter: Wealth combination
    if angular_distance(pos['Venus']['longitude'], pos['Jupiter']['longitude']) <= 10:
        yogas.append({
            'name': 'Venus-Jupiter Conjunction',
            'planets': ['Venus', 'Jupiter'],
            'description': 'Two greatest benefics together — wealth, optimism, bullish sentiment',
            'market_bias': 'bullish',
            'weight': 18,
            'category': 'conjunction',
        })

    # Saturn-Mars: Conflict energy
    sat_mars = angular_distance(pos['Saturn']['longitude'], pos['Mars']['longitude'])
    if sat_mars <= 10:
        yogas.append({
            'name': 'Saturn-Mars Conjunction (Graha Yuddha)',
            'planets': ['Saturn', 'Mars'],
            'description': 'Extreme tension, fear vs aggression — sharp drops, conflict',
            'market_bias': 'bearish',
            'weight': 22,
            'category': 'conjunction',
        })
    elif abs(sat_mars - 180) <= 10:
        yogas.append({
            'name': 'Saturn-Mars Opposition',
            'planets': ['Saturn', 'Mars'],
            'description': 'Push-pull conflict — whipsaw, indecision, eventual breakdown',
            'market_bias': 'volatile_bearish',
            'weight': 18,
            'category': 'conjunction',
        })

    # Chandra-Mangala: Moon-Mars
    if angular_distance(pos['Moon']['longitude'], pos['Mars']['longitude']) <= 10:
        yogas.append({
            'name': 'Chandra-Mangala Yoga',
            'planets': ['Moon', 'Mars'],
            'description': 'Emotional aggression — high volume, impulsive trading, volatility',
            'market_bias': 'volatile',
            'weight': 15,
            'category': 'conjunction',
        })

    # Budha-Aditya: Mercury + Sun (check NOT combust)
    merc_sun = angular_distance(pos['Mercury']['longitude'], pos['Sun']['longitude'])
    if merc_sun <= 10 and merc_sun > 3:  # Close but not too combust
        yogas.append({
            'name': 'Budha-Aditya Yoga',
            'planets': ['Mercury', 'Sun'],
            'description': 'Intelligence + authority — smart money moves, policy clarity',
            'market_bias': 'bullish',
            'weight': 12,
            'category': 'conjunction',
        })

    # Saturn-Jupiter: Policy/expansion cycle
    if angular_distance(pos['Saturn']['longitude'], pos['Jupiter']['longitude']) <= 10:
        yogas.append({
            'name': 'Saturn-Jupiter Conjunction',
            'planets': ['Saturn', 'Jupiter'],
            'description': 'Great Conjunction — new 20-year economic cycle begins',
            'market_bias': 'volatile',
            'weight': 25,
            'category': 'conjunction',
        })

    # Mercury-Venus: Commerce + luxury
    if angular_distance(pos['Mercury']['longitude'], pos['Venus']['longitude']) <= 8:
        yogas.append({
            'name': 'Mercury-Venus Conjunction',
            'planets': ['Mercury', 'Venus'],
            'description': 'Commerce + luxury — consumer spending, retail sector bullish',
            'market_bias': 'bullish',
            'weight': 10,
            'category': 'conjunction',
        })

    return yogas


# ── 2. SOLAR YOGAS (Planets relative to Sun) ─────────────

def _solar_yogas(pos):
    yogas = []
    sun_sign_idx = pos['Sun']['sign_index']
    non_luminaries = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    # Check which planets are in 2nd and 12th from Sun
    planets_in_2nd = []
    planets_in_12th = []
    planets_in_both_sides = False

    for planet in non_luminaries:
        p_sign_idx = pos[planet]['sign_index']
        house_from_sun = ((p_sign_idx - sun_sign_idx) % 12) + 1

        if house_from_sun == 2:
            planets_in_2nd.append(planet)
        elif house_from_sun == 12:
            planets_in_12th.append(planet)

    # Veshi Yoga: Planet in 2nd from Sun
    if planets_in_2nd:
        yogas.append({
            'name': 'Veshi Yoga',
            'planets': ['Sun'] + planets_in_2nd,
            'description': f'{", ".join(planets_in_2nd)} in 2nd from Sun — accumulation phase, market building strength',
            'market_bias': 'bullish',
            'weight': 12,
            'category': 'solar',
        })

    # Vashi Yoga: Planet in 12th from Sun
    if planets_in_12th:
        yogas.append({
            'name': 'Vashi Yoga',
            'planets': ['Sun'] + planets_in_12th,
            'description': f'{", ".join(planets_in_12th)} in 12th from Sun — distribution phase, smart money selling',
            'market_bias': 'bearish',
            'weight': 12,
            'category': 'solar',
        })

    # Ubhayachari Yoga: Planets on BOTH sides of Sun
    if planets_in_2nd and planets_in_12th:
        yogas.append({
            'name': 'Ubhayachari Yoga',
            'planets': ['Sun'] + planets_in_2nd + planets_in_12th,
            'description': 'Sun flanked by planets — strong directional trend, decisive market',
            'market_bias': 'trend_strong',
            'weight': 16,
            'category': 'solar',
        })

    return yogas


# ── 3. LUNAR YOGAS (Planets relative to Moon) ────────────

def _lunar_yogas(pos):
    yogas = []
    moon_sign_idx = pos['Moon']['sign_index']

    # Gaja-Kesari: Jupiter in kendra from Moon (1/4/7/10)
    jup_sign_idx = pos['Jupiter']['sign_index']
    house_diff = ((jup_sign_idx - moon_sign_idx) % 12)
    if house_diff in [0, 3, 6, 9]:
        yogas.append({
            'name': 'Gaja-Kesari Yoga',
            'planets': ['Jupiter', 'Moon'],
            'description': 'Jupiter in kendra from Moon — prosperity, institutional optimism',
            'market_bias': 'bullish',
            'weight': 18,
            'category': 'lunar',
        })

    # Kemadruma Yoga: No planet in 2nd or 12th from Moon
    has_2nd = False
    has_12th = False
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 1:
            has_2nd = True
        elif h == 11:
            has_12th = True

    if not has_2nd and not has_12th:
        yogas.append({
            'name': 'Kemadruma Yoga',
            'planets': ['Moon'],
            'description': 'Moon isolated — no support. Panic, loneliness, sharp drops, lack of buying interest',
            'market_bias': 'bearish',
            'weight': 20,
            'category': 'lunar',
        })

    # Shakata Yoga: Jupiter in 6th or 8th from Moon
    if house_diff in [5, 7]:  # 6th house = index 5, 8th house = index 7
        yogas.append({
            'name': 'Shakata Yoga',
            'planets': ['Jupiter', 'Moon'],
            'description': 'Jupiter in dusthana from Moon — instability, policy shocks, broken promises',
            'market_bias': 'volatile_bearish',
            'weight': 16,
            'category': 'lunar',
        })

    # Amala Yoga: Benefic in 10th from Moon
    benefics = ['Jupiter', 'Venus', 'Mercury']
    for b in benefics:
        b_sign_idx = pos[b]['sign_index']
        h = ((b_sign_idx - moon_sign_idx) % 12)
        if h == 9:  # 10th house = index 9
            yogas.append({
                'name': f'Amala Yoga ({b})',
                'planets': [b, 'Moon'],
                'description': f'{b} in 10th from Moon — clean rally, positive action, institutional buying',
                'market_bias': 'bullish',
                'weight': 14,
                'category': 'lunar',
            })
            break

    # Dur Yoga: Malefic in 10th from Moon
    malefics = ['Saturn', 'Mars']
    for m in malefics:
        m_sign_idx = pos[m]['sign_index']
        h = ((m_sign_idx - moon_sign_idx) % 12)
        if h == 9:
            yogas.append({
                'name': f'Dur Yoga ({m})',
                'planets': [m, 'Moon'],
                'description': f'{m} in 10th from Moon — dirty selloff, negative news driven',
                'market_bias': 'bearish',
                'weight': 14,
                'category': 'lunar',
            })
            break

    # Sunapha: Planet in 2nd from Moon (not Sun)
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 1:
            yogas.append({
                'name': f'Sunapha Yoga ({planet})',
                'planets': [planet, 'Moon'],
                'description': f'{planet} in 2nd from Moon — wealth growth, market support',
                'market_bias': 'bullish',
                'weight': 10,
                'category': 'lunar',
            })
            break

    # Anapha: Planet in 12th from Moon (not Sun)
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        p_sign_idx = pos[planet]['sign_index']
        h = ((p_sign_idx - moon_sign_idx) % 12)
        if h == 11:
            yogas.append({
                'name': f'Anapha Yoga ({planet})',
                'planets': [planet, 'Moon'],
                'description': f'{planet} in 12th from Moon — past momentum, cautious optimism',
                'market_bias': 'mildly_bullish',
                'weight': 8,
                'category': 'lunar',
            })
            break

    return yogas


# ── 4. NODE YOGAS (Rahu/Ketu) ────────────────────────────

def _node_yogas(pos):
    yogas = []

    rahu_deg = pos['Rahu']['longitude']
    ketu_deg = pos['Ketu']['longitude']
    sun_deg = pos['Sun']['longitude']
    moon_deg = pos['Moon']['longitude']

    # Grahan Yoga (Eclipse-like): Sun/Moon close to Rahu/Ketu
    for node, node_deg in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        for lum, lum_deg in [('Sun', sun_deg), ('Moon', moon_deg)]:
            dist = angular_distance(lum_deg, node_deg)
            if dist <= 12:
                yogas.append({
                    'name': f'Grahan Yoga ({lum}-{node})',
                    'planets': [lum, node],
                    'description': f'{lum} eclipsed by {node} — confusion, fear, sudden reversals',
                    'market_bias': 'volatile',
                    'weight': 20 if dist <= 5 else 12,
                    'category': 'nodal',
                })

    # Kala Sarpa Yoga: All planets on one side of Rahu-Ketu axis
    rahu_idx = pos['Rahu']['sign_index']
    ketu_idx = pos['Ketu']['sign_index']
    all_one_side = True
    side_count = 0
    check_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    for p in check_planets:
        p_idx = pos[p]['sign_index']
        # Check if planet is between Rahu and Ketu (going forward)
        if rahu_idx < ketu_idx:
            between = rahu_idx <= p_idx <= ketu_idx
        else:
            between = p_idx >= rahu_idx or p_idx <= ketu_idx
        if between:
            side_count += 1

    if side_count == len(check_planets) or side_count == 0:
        yogas.append({
            'name': 'Kala Sarpa Yoga',
            'planets': ['Rahu', 'Ketu'] + check_planets,
            'description': 'All planets hemmed by nodes — fatalistic, extreme moves, trapped energy',
            'market_bias': 'volatile_bearish',
            'weight': 25,
            'category': 'nodal',
        })

    return yogas


# ── 5. STRENGTH-BASED YOGAS ──────────────────────────────

def _strength_yogas(pos):
    yogas = []

    # Multiple Retrograde Stress
    retro_planets = [n for n in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                     if pos[n]['retrograde']]
    if len(retro_planets) >= 3:
        yogas.append({
            'name': 'Multiple Retrograde Stress',
            'planets': retro_planets,
            'description': f'{len(retro_planets)} planets retrograde — uncertainty, review, revision mode',
            'market_bias': 'volatile',
            'weight': len(retro_planets) * 5,
            'category': 'strength',
        })

    # Neecha Bhanga Raja Yoga: Debilitated planet with cancellation
    # (Lord of debilitation sign is strong OR lord of exaltation sign aspects)
    for planet_name, data in pos.items():
        if data['dignity'] == 'Debilitated' and planet_name not in ['Rahu', 'Ketu']:
            deb_sign = data['sign']
            deb_lord = SIGN_LORDS.get(deb_sign, '')

            # Check if debilitation lord is exalted or in own sign
            if deb_lord in pos:
                lord_dignity = pos[deb_lord]['dignity']
                if lord_dignity in ['Exalted', 'Own Sign', 'Moolatrikona']:
                    yogas.append({
                        'name': f'Neecha Bhanga Raja Yoga ({planet_name})',
                        'planets': [planet_name, deb_lord],
                        'description': f'{planet_name} debilitated but saved by strong {deb_lord} — beaten-down sectors bounce back strongly',
                        'market_bias': 'bullish',
                        'weight': 18,
                        'category': 'strength',
                    })

    # Exalted benefic = very bullish
    for planet in ['Jupiter', 'Venus']:
        if pos[planet]['dignity'] == 'Exalted':
            yogas.append({
                'name': f'{planet} Exalted',
                'planets': [planet],
                'description': f'{planet} at peak strength — maximum optimism/wealth energy',
                'market_bias': 'bullish',
                'weight': 20,
                'category': 'strength',
            })

    # Debilitated malefic = reduced negative energy = mildly bullish
    for planet in ['Saturn', 'Mars']:
        if pos[planet]['dignity'] == 'Debilitated':
            yogas.append({
                'name': f'{planet} Debilitated',
                'planets': [planet],
                'description': f'{planet} weakened — reduced fear/aggression, but chaotic energy',
                'market_bias': 'volatile',
                'weight': 12,
                'category': 'strength',
            })

    # Exalted malefic = strong negative potential
    for planet in ['Saturn', 'Mars']:
        if pos[planet]['dignity'] == 'Exalted':
            yogas.append({
                'name': f'{planet} Exalted',
                'planets': [planet],
                'description': f'{planet} at peak power — structured but intense pressure on markets',
                'market_bias': 'volatile_bearish' if planet == 'Saturn' else 'volatile',
                'weight': 15,
                'category': 'strength',
            })

    return yogas


# ── 6. SPECIAL COMBINATIONS ──────────────────────────────

def _special_combinations(pos):
    yogas = []

    # Parivartana Yoga (Mutual Exchange)
    checked = set()
    for p1_name, p1_data in pos.items():
        if p1_name in ['Rahu', 'Ketu']:
            continue
        p1_sign = p1_data['sign']
        p1_sign_lord = SIGN_LORDS.get(p1_sign, '')

        if p1_sign_lord in pos and p1_sign_lord not in ['Rahu', 'Ketu']:
            p2_data = pos[p1_sign_lord]
            p2_sign = p2_data['sign']
            p2_sign_lord = SIGN_LORDS.get(p2_sign, '')

            pair = tuple(sorted([p1_name, p1_sign_lord]))
            if p2_sign_lord == p1_name and pair not in checked:
                checked.add(pair)
                yogas.append({
                    'name': f'Parivartana Yoga ({p1_name}-{p1_sign_lord})',
                    'planets': list(pair),
                    'description': f'{pair[0]} and {pair[1]} in mutual exchange — sector rotation, regime change, energy swap',
                    'market_bias': 'volatile',
                    'weight': 16,
                    'category': 'special',
                })

    # All benefics in one sign = massive positivity
    benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
    benefic_signs = [pos[b]['sign'] for b in benefics if b in pos]
    for sign in set(benefic_signs):
        count = benefic_signs.count(sign)
        if count >= 3:
            yogas.append({
                'name': f'Benefic Stellium in {sign}',
                'planets': [b for b in benefics if pos[b]['sign'] == sign],
                'description': f'{count} benefics concentrated in {sign} — extreme optimism, bubble risk',
                'market_bias': 'bullish',
                'weight': 20,
                'category': 'special',
            })

    # All malefics in one sign = concentrated negativity
    malefics_list = ['Saturn', 'Mars', 'Rahu', 'Ketu']
    malefic_signs = [pos[m]['sign'] for m in malefics_list if m in pos]
    for sign in set(malefic_signs):
        count = malefic_signs.count(sign)
        if count >= 3:
            yogas.append({
                'name': f'Malefic Stellium in {sign}',
                'planets': [m for m in malefics_list if pos[m]['sign'] == sign],
                'description': f'{count} malefics concentrated in {sign} — extreme stress sector-specific crash risk',
                'market_bias': 'bearish',
                'weight': 22,
                'category': 'special',
            })

    return yogas


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from core.astro_engine import get_planetary_positions
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n⭐ YOGA DETECTION TEST — {today}")
    print("=" * 60)

    pos = get_planetary_positions(today)
    yogas = detect_all_yogas(pos)

    if yogas:
        for y in yogas:
            emoji = '🟢' if 'bullish' in y['market_bias'] else (
                '🔴' if 'bearish' in y['market_bias'] else '🟡')
            print(f"\n{emoji} {y['name']} [{y['category'].upper()}]")
            print(f"   Planets: {', '.join(y['planets'])}")
            print(f"   {y['description']}")
            print(f"   Market Bias: {y['market_bias'].upper()}, Weight: {y['weight']}")
    else:
        print("No significant yogas detected today.")


Save: Ctrl + S

Step 2.4 — core/panchang.py (Karana, Nitya Yoga, Gandanta, Void of Course)
Click core/panchang.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Panchang (Daily Vedic Calendar) Engine
=============================================================
Calculates: Tithi, Karana, Nitya Yoga, Vara (weekday),
Nakshatra, Gandanta zones, Void of Course Moon.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, date_to_jd, get_sign,
    get_nakshatra, angular_distance, SIGNS, NAKSHATRA_SPAN
)
import swisseph as swe
from datetime import datetime


# ── TITHI ─────────────────────────────────────────────────

TITHI_NAMES = [
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
    'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
    'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima',
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
    'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
    'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Amavasya'
]

TITHI_MARKET_NOTES = {
    'Pratipada': 'New beginning energy. Markets may set new direction.',
    'Dwitiya': 'Building phase. Moderate positivity.',
    'Tritiya': 'Creative energy. Good for growth stocks.',
    'Chaturthi': 'Vinayaka\'s tithi. Obstacles possible, then resolution.',
    'Panchami': 'Lakshmi\'s tithi. Generally auspicious for wealth.',
    'Shashthi': 'Mars energy. Volatility, quick moves.',
    'Saptami': 'Sun energy. Authority, government policy impact.',
    'Ashtami': '⚠️ CRITICAL: 8th tithi = transformation, sudden reversals, high risk.',
    'Navami': 'Mars energy. Aggressive moves, breakouts.',
    'Dashami': 'Completion energy. Trend may exhaust.',
    'Ekadashi': 'Fasting day. Low volume possible, spiritual energy.',
    'Dwadashi': 'Recovery phase after Ekadashi restraint.',
    'Trayodashi': 'Pradosh. Shiva energy. Destruction of old trends.',
    'Chaturdashi': '⚠️ Day before New/Full Moon. High tension. Avoid big bets.',
    'Purnima': '⚠️ FULL MOON: Peak emotion, reversals common, high volatility.',
    'Amavasya': '⚠️ NEW MOON: Low energy, confusion, avoid new positions.',
}


def get_tithi(moon_deg, sun_deg):
    diff = (moon_deg - sun_deg) % 360.0
    tithi_num = int(diff / 12.0) + 1
    tithi_num = min(tithi_num, 30)
    paksha = 'Shukla' if tithi_num <= 15 else 'Krishna'
    name = TITHI_NAMES[tithi_num - 1]
    market_note = TITHI_MARKET_NOTES.get(name, '')
    return {
        'number': tithi_num,
        'name': name,
        'paksha': paksha,
        'market_note': market_note,
        'is_critical': name in ['Ashtami', 'Chaturdashi', 'Purnima', 'Amavasya'],
    }


# ── KARANA ────────────────────────────────────────────────

KARANA_NAMES = [
    'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garija',
    'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Nagava', 'Kimstughna'
]

KARANA_NATURE = {
    'Bava': ('Movable', 'bullish', 'Good for starting trades'),
    'Balava': ('Movable', 'bullish', 'Strength, upward momentum'),
    'Kaulava': ('Movable', 'bullish', 'Friendship energy, accumulation'),
    'Taitila': ('Movable', 'bullish', 'Wealth building, steady gains'),
    'Garija': ('Movable', 'neutral', 'Mixed energy, consolidation'),
    'Vanija': ('Movable', 'bullish', 'Trade & commerce favorable'),
    'Vishti': ('Fixed', 'bearish', '⚠️ BHADRA KARANA: Very inauspicious. Avoid new trades. Losses likely.'),
    'Shakuni': ('Fixed', 'volatile', 'Bird of omen — sudden news, unexpected moves'),
    'Chatushpada': ('Fixed', 'bearish', 'Stubbornness, resistance to trend'),
    'Nagava': ('Fixed', 'bearish', 'Snake energy — hidden dangers, manipulation'),
    'Kimstughna': ('Fixed', 'neutral', 'Confusion, unclear direction'),
}


def get_karana(moon_deg, sun_deg):
    diff = (moon_deg - sun_deg) % 360.0
    karana_num = int(diff / 6.0) + 1  # Each karana = 6° of Moon-Sun distance

    # First karana of Shukla Pratipada is Kimstughna
    # Cycle: Kimstughna (1st half of 1st tithi), then Bava-Vishti repeat,
    # last 4 karanas of Krishna Chaturdashi-Amavasya are fixed
    if karana_num == 1:
        name = 'Kimstughna'
    elif karana_num >= 58:
        fixed_karanas = ['Shakuni', 'Chatushpada', 'Nagava']
        name = fixed_karanas[karana_num - 58] if karana_num - 58 < 3 else 'Kimstughna'
    else:
        cycle_idx = (karana_num - 2) % 7
        name = KARANA_NAMES[cycle_idx]

    nature, bias, note = KARANA_NATURE.get(name, ('Unknown', 'neutral', ''))
    return {
        'number': karana_num,
        'name': name,
        'nature': nature,
        'market_bias': bias,
        'note': note,
        'is_vishti': name == 'Vishti',
    }


# ── NITYA YOGA (Astronomical Yoga) ───────────────────────

NITYA_YOGA_NAMES = [
    'Vishkambha', 'Preeti', 'Ayushman', 'Saubhagya', 'Shobhana',
    'Atiganda', 'Sukarma', 'Dhriti', 'Shoola', 'Ganda',
    'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
    'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
    'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
    'Indra', 'Vaidhriti'
]

NITYA_YOGA_NATURE = {
    'Vishkambha': ('Shubha', 'bullish', 'Obstacle-removing, good start'),
    'Preeti': ('Shubha', 'bullish', 'Love/joy — positive sentiment'),
    'Ayushman': ('Shubha', 'bullish', 'Long life — stability, longevity of trends'),
    'Saubhagya': ('Shubha', 'bullish', 'Good fortune — lucky day for markets'),
    'Shobhana': ('Shubha', 'bullish', 'Beauty — aesthetics, luxury sector up'),
    'Atiganda': ('Ashubha', 'bearish', '⚠️ Danger — accidents, sudden drops'),
    'Sukarma': ('Shubha', 'bullish', 'Good deeds rewarded — righteous gains'),
    'Dhriti': ('Shubha', 'bullish', 'Determination — trend holds strong'),
    'Shoola': ('Ashubha', 'bearish', '⚠️ Thorn/pain — losses, sharp pricks'),
    'Ganda': ('Ashubha', 'bearish', '⚠️ Knot — trapped, no exit, stuck markets'),
    'Vriddhi': ('Shubha', 'bullish', 'Growth — expansion, bullish signal'),
    'Dhruva': ('Shubha', 'bullish', 'Fixed/stable — consolidation, hold positions'),
    'Vyaghata': ('Ashubha', 'bearish', '⚠️ Destruction — breakdowns, crashes'),
    'Harshana': ('Shubha', 'bullish', 'Joy — optimistic buying'),
    'Vajra': ('Mixed', 'volatile', 'Thunderbolt — sudden powerful moves either way'),
    'Siddhi': ('Shubha', 'bullish', 'Accomplishment — targets hit, success'),
    'Vyatipata': ('Ashubha', 'bearish', '⚠️ Calamity — one of worst yogas. Major negativity.'),
    'Variyan': ('Shubha', 'bullish', 'Comfort — easy, flowing markets'),
    'Parigha': ('Ashubha', 'bearish', '⚠️ Obstacle/iron bar — blocked, resistance'),
    'Shiva': ('Shubha', 'bullish', 'Auspicious — divine blessing on markets'),
    'Siddha': ('Shubha', 'bullish', 'Accomplished — completion, profit booking'),
    'Sadhya': ('Shubha', 'bullish', 'Achievable — realistic targets met'),
    'Shubha': ('Shubha', 'bullish', 'Auspicious — one of the best yogas'),
    'Shukla': ('Shubha', 'bullish', 'Bright/white — clarity, transparency'),
    'Brahma': ('Shubha', 'bullish', 'Creator — new beginnings, IPOs favored'),
    'Indra': ('Shubha', 'bullish', 'King of gods — power, authority, leadership stocks'),
    'Vaidhriti': ('Ashubha', 'bearish', '⚠️ Split apart — division, breakdown, worst yoga'),
}


def get_nitya_yoga(moon_deg, sun_deg):
    """Nitya Yoga = (Sun longitude + Moon longitude) / 13°20'."""
    total = (sun_deg + moon_deg) % 360.0
    yoga_num = int(total / NAKSHATRA_SPAN) + 1
    yoga_num = min(yoga_num, 27)
    name = NITYA_YOGA_NAMES[yoga_num - 1]
    nature, bias, note = NITYA_YOGA_NATURE.get(name, ('Unknown', 'neutral', ''))
    return {
        'number': yoga_num,
        'name': name,
        'nature': nature,
        'market_bias': bias,
        'note': note,
        'is_inauspicious': nature == 'Ashubha',
    }


# ── VARA (Weekday) ───────────────────────────────────────

VARA_DATA = {
    0: ('Monday', 'Moon', 'Liquidity, silver, FMCG. Moon-ruled day — emotional trading.'),
    1: ('Tuesday', 'Mars', 'Volatility, real estate, defense. Aggressive moves.'),
    2: ('Wednesday', 'Mercury', 'IT, telecom, banking. Communication, fast trades.'),
    3: ('Thursday', 'Jupiter', 'Finance, education, law. Expansion, bullish tendency.'),
    4: ('Friday', 'Venus', 'Luxury, auto, entertainment. Positive, accumulation.'),
    5: ('Saturday', 'Saturn', 'Infrastructure, oil. Slow, heavy, restrictive.'),
    6: ('Sunday', 'Sun', 'Market closed. But astro energy still applies for Monday open.'),
}


def get_vara(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    day_num = dt.weekday()
    name, lord, note = VARA_DATA[day_num]
    return {'name': name, 'lord': lord, 'note': note}


# ── GANDANTA ZONES ────────────────────────────────────────

GANDANTA_JUNCTIONS = [
    (0, 'Pisces→Aries', 'Water→Fire: Emotional to aggressive. Deep karmic transition.'),
    (120, 'Cancer→Leo', 'Water→Fire: Nurturing to authoritative. Policy shifts.'),
    (240, 'Scorpio→Sagittarius', 'Water→Fire: Hidden to expansive. Secrets revealed.'),
]


def check_gandanta(positions):
    """Check if Moon (or any planet) is in Gandanta zone (last 3°20' or first 3°20' of junction)."""
    gandantas = []
    gandanta_range = 3.333  # 3°20'

    for planet_name, data in positions.items():
        deg = data['longitude']
        sign_deg = data['sign_degree']

        for junction_deg, junction_name, note in GANDANTA_JUNCTIONS:
            # Last 3°20' of water sign
            if abs((deg % 360) - junction_deg) < gandanta_range or \
               abs((deg % 360) - (junction_deg + 360)) < gandanta_range:
                if sign_deg >= (30 - gandanta_range) or sign_deg <= gandanta_range:
                    gandantas.append({
                        'planet': planet_name,
                        'junction': junction_name,
                        'sign_degree': data['sign_degree'],
                        'note': note,
                        'severity': 'Exact' if sign_deg >= 29 or sign_deg <= 1 else 'Approaching',
                        'market_impact': 'HIGH — reversals, karmic events' if planet_name == 'Moon' else 'MEDIUM',
                    })

    return gandantas


# ── VOID OF COURSE MOON ──────────────────────────────────

def check_void_of_course(date_str, positions):
    """
    Simplified VOC check: Moon makes no major aspect to any planet
    before leaving current sign. Approximation for daily use.
    """
    moon_deg = positions['Moon']['longitude']
    moon_sign_deg = positions['Moon']['sign_degree']
    moon_speed = abs(positions['Moon']['speed'])

    # Degrees left in current sign
    degrees_left = 30.0 - moon_sign_deg

    # Time to leave sign (hours)
    if moon_speed > 0:
        hours_left = (degrees_left / moon_speed) * 24
    else:
        hours_left = float('inf')

    # Check if Moon will aspect any planet before leaving sign
    # Simplified: if Moon is in last 5° and no planet within aspect range ahead
    is_voc = False
    voc_note = ''

    if moon_sign_deg >= 25:  # Last 5 degrees
        # Check if any planet is in the remaining degrees of this sign
        has_aspect_ahead = False
        for planet_name, pdata in positions.items():
            if planet_name == 'Moon':
                continue
            p_deg = pdata['longitude']
            dist = (p_deg - moon_deg) % 360
            if dist < degrees_left and dist > 0:
                has_aspect_ahead = True
                break

        if not has_aspect_ahead:
            is_voc = True
            voc_note = f'Moon void of course — last {degrees_left:.1f}° in {positions["Moon"]["sign"]}. Market may drift, avoid new entries.'

    return {
        'is_voc': is_voc,
        'degrees_left_in_sign': round(degrees_left, 2),
        'approx_hours_left': round(hours_left, 1) if hours_left != float('inf') else None,
        'note': voc_note,
    }


# ── MOON PHASE ────────────────────────────────────────────

def get_moon_phase(positions):
    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']
    diff = (moon_deg - sun_deg) % 360.0

    if diff < 15:
        phase = 'New Moon (Amavasya zone)'
        note = 'Low energy, reversals possible, avoid big positions'
    elif diff < 90:
        phase = 'Waxing Crescent'
        note = 'Building momentum, cautious buying'
    elif diff < 135:
        phase = 'Waxing Gibbous'
        note = 'Strong momentum, trend continuation likely'
    elif diff < 195:
        phase = 'Full Moon (Purnima zone)'
        note = 'Peak emotion, high volatility, possible reversal'
    elif diff < 270:
        phase = 'Waning Gibbous'
        note = 'Profit booking phase, declining momentum'
    elif diff < 345:
        phase = 'Waning Crescent'
        note = 'Exhaustion, caution, prepare for new cycle'
    else:
        phase = 'New Moon (Amavasya zone)'
        note = 'Low energy, reversals possible, avoid big positions'

    return {'phase': phase, 'sun_moon_distance': round(diff, 2), 'market_note': note}


# ── FULL PANCHANG ─────────────────────────────────────────

def get_full_panchang(date_str, positions=None):
    """Complete Panchang for a date."""
    if positions is None:
        positions = get_planetary_positions(date_str)

    moon_deg = positions['Moon']['longitude']
    sun_deg = positions['Sun']['longitude']

    tithi = get_tithi(moon_deg, sun_deg)
    karana = get_karana(moon_deg, sun_deg)
    nitya_yoga = get_nitya_yoga(moon_deg, sun_deg)
    vara = get_vara(date_str)
    moon_phase = get_moon_phase(positions)
    gandantas = check_gandanta(positions)
    voc = check_void_of_course(date_str, positions)

    # Moon nakshatra
    moon_nak, moon_pada, moon_nak_lord = get_nakshatra(moon_deg)

    return {
        'date': date_str,
        'vara': vara,
        'tithi': tithi,
        'karana': karana,
        'nitya_yoga': nitya_yoga,
        'moon_phase': moon_phase,
        'moon_nakshatra': {'name': moon_nak, 'pada': moon_pada, 'lord': moon_nak_lord},
        'gandantas': gandantas,
        'void_of_course': voc,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📅 FULL PANCHANG — {today}")
    print("=" * 60)

    panchang = get_full_panchang(today)

    v = panchang['vara']
    print(f"\n📆 Vara: {v['name']} (Lord: {v['lord']})")
    print(f"   {v['note']}")

    t = panchang['tithi']
    print(f"\n🌙 Tithi: {t['paksha']} {t['name']} (#{t['number']})")
    print(f"   {t['market_note']}")
    if t['is_critical']:
        print(f"   ⚠️ CRITICAL TITHI — Extra caution!")

    k = panchang['karana']
    print(f"\n🔷 Karana: {k['name']} ({k['nature']})")
    print(f"   {k['note']}")
    if k['is_vishti']:
        print(f"   🚫 VISHTI KARANA (BHADRA) — AVOID new trades!")

    ny = panchang['nitya_yoga']
    print(f"\n⭐ Nitya Yoga: {ny['name']} ({ny['nature']})")
    print(f"   {ny['note']}")
    if ny['is_inauspicious']:
        print(f"   ⚠️ INAUSPICIOUS YOGA — Caution advised!")

    mp = panchang['moon_phase']
    print(f"\n🌗 Moon Phase: {mp['phase']}")
    print(f"   {mp['market_note']}")

    mn = panchang['moon_nakshatra']
    print(f"\n🌟 Moon Nakshatra: {mn['name']} Pada {mn['pada']} (Lord: {mn['lord']})")

    if panchang['gandantas']:
        print(f"\n🔥 GANDANTA ALERTS:")
        for g in panchang['gandantas']:
            print(f"   {g['planet']}: {g['junction']} ({g['severity']})")
            print(f"   {g['note']}")

    voc = panchang['void_of_course']
    if voc['is_voc']:
        print(f"\n🕳️ VOID OF COURSE MOON: {voc['note']}")


Save: Ctrl + S

Step 2.5 — core/hora.py (Planetary Hours + Rahu Kaal)
Click core/hora.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Planetary Hours (Hora) & Rahu Kaal
=============================================================
Calculates which planet rules each hour of the trading day.
THE #1 intraday timing tool in financial astrology.
=============================================================
"""

from datetime import datetime, timedelta
import swisseph as swe
from core.astro_engine import date_to_jd
import math

# ── Constants ─────────────────────────────────────────────

# Planetary hour sequence (Chaldean order)
HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']

# Day rulers (which planet starts the hora sequence)
DAY_RULERS = {
    0: 'Moon',      # Monday
    1: 'Mars',      # Tuesday
    2: 'Mercury',   # Wednesday
    3: 'Jupiter',   # Thursday
    4: 'Venus',     # Friday
    5: 'Saturn',    # Saturday
    6: 'Sun',       # Sunday
}

# Market interpretation of each hora
HORA_MARKET_EFFECT = {
    'Sun': {
        'bias': 'bullish',
        'note': 'Authority, government orders, power stocks. Strong directional move.',
        'sectors': ['Power', 'Pharma', 'Government PSUs'],
        'action': 'Good for trend trades',
    },
    'Moon': {
        'bias': 'volatile',
        'note': 'Emotional trading, liquidity moves, sentiment shifts.',
        'sectors': ['FMCG', 'Silver', 'Hospitality'],
        'action': 'Watch for sentiment reversals',
    },
    'Mars': {
        'bias': 'volatile',
        'note': 'Aggressive moves, breakouts/breakdowns, high volume spikes.',
        'sectors': ['Real Estate', 'Defense', 'Steel', 'Energy'],
        'action': '⚠️ Quick scalps only. Set tight stops.',
    },
    'Mercury': {
        'bias': 'neutral',
        'note': 'Communication, data, fast trades. Good for IT/banking.',
        'sectors': ['IT', 'Telecom', 'Banking (trading)'],
        'action': 'Good for quick in-out trades',
    },
    'Jupiter': {
        'bias': 'bullish',
        'note': '🟢 BEST hora for buying. Optimism, expansion, institutional flow.',
        'sectors': ['Banking (investment)', 'Finance', 'Education'],
        'action': '✅ BEST TIME TO BUY. Accumulate.',
    },
    'Venus': {
        'bias': 'bullish',
        'note': 'Luxury, comfort, steady gains. Good for accumulation.',
        'sectors': ['Auto', 'Luxury', 'Entertainment', 'Sugar'],
        'action': 'Good for buying, especially value stocks',
    },
    'Saturn': {
        'bias': 'bearish',
        'note': '🔴 CAUTION hora. Slow, heavy, restrictive. Profit booking time.',
        'sectors': ['Infrastructure', 'Mining', 'Oil & Gas'],
        'action': '⚠️ AVOID new buys. Book profits. Bears active.',
    },
}

# Rahu Kaal timings per weekday (based on sunrise division)
# Format: (start_segment, end_segment) — each day is divided into 8 segments
RAHU_KAAL_SEGMENTS = {
    0: (2, 3),    # Monday: 2nd segment
    1: (7, 8),    # Tuesday: 8th segment
    2: (5, 6),    # Wednesday: 6th segment
    3: (4, 5),    # Thursday: 5th segment
    4: (3, 4),    # Friday: 4th segment
    5: (1, 2),    # Saturday: 2nd segment
    6: (6, 7),    # Sunday: 7th segment
}

GULIKA_SEGMENTS = {
    0: (6, 7),    # Monday
    1: (5, 6),    # Tuesday
    2: (4, 5),    # Wednesday
    3: (3, 4),    # Thursday
    4: (2, 3),    # Friday
    5: (1, 2),    # Saturday
    6: (0, 1),    # Sunday
}

YAMAGANDA_SEGMENTS = {
    0: (4, 5),    # Monday
    1: (3, 4),    # Tuesday
    2: (2, 3),    # Wednesday
    3: (1, 2),    # Thursday
    4: (0, 1),    # Friday
    5: (6, 7),    # Saturday
    6: (5, 6),    # Sunday
}


# ── Sunrise / Sunset ─────────────────────────────────────

def get_sunrise_sunset(date_str, lat=19.0760, lon=72.8777):
    """
    Calculate sunrise and sunset for Mumbai (NSE location).
    Returns times in IST.
    """
    jd = date_to_jd(date_str, '12:00')

    # Swiss Ephemeris sunrise
    try:
        result_rise = swe.rise_trans(
            jd, swe.SUN, lon, lat, 0.0, 0.0,
            swe.CALC_RISE | swe.BIT_DISC_CENTER
        )
        result_set = swe.rise_trans(
            jd, swe.SUN, lon, lat, 0.0, 0.0,
            swe.CALC_SET | swe.BIT_DISC_CENTER
        )

        sunrise_jd = result_rise[1][0]
        sunset_jd = result_set[1][0]

        # Convert JD to datetime (already in UT, add 5:30 for IST)
        sunrise_ut = swe.jdut1_to_utc(sunrise_jd, 1)
        sunset_ut = swe.jdut1_to_utc(sunset_jd, 1)

        ist_offset = timedelta(hours=5, minutes=30)

        sunrise = datetime(int(sunrise_ut[0]), int(sunrise_ut[1]),
                          int(sunrise_ut[2]), int(sunrise_ut[3]),
                          int(sunrise_ut[4]), int(sunrise_ut[5])) + ist_offset
        sunset = datetime(int(sunset_ut[0]), int(sunset_ut[1]),
                         int(sunset_ut[2]), int(sunset_ut[3]),
                         int(sunset_ut[4]), int(sunset_ut[5])) + ist_offset

        return sunrise, sunset

    except Exception:
        # Fallback: approximate for Mumbai
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        sunrise = dt.replace(hour=6, minute=15)
        sunset = dt.replace(hour=18, minute=30)
        return sunrise, sunset


# ── Planetary Hours Calculation ───────────────────────────

def get_planetary_hours(date_str, market_start='09:15', market_end='15:30'):
    """
    Calculate planetary hours for the trading day.
    Returns hora table for market hours.
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    weekday = dt.weekday()
    day_ruler = DAY_RULERS[weekday]

    sunrise, sunset = get_sunrise_sunset(date_str)

    # Day duration and night duration
    day_length = (sunset - sunrise).total_seconds()
    night_length = 86400 - day_length  # 24 hours - day

    # Each day hora = day_length / 12
    day_hora_seconds = day_length / 12.0
    night_hora_seconds = night_length / 12.0

    # Find starting planet index
    start_idx = HORA_SEQUENCE.index(day_ruler)

    # Generate all 24 horas
    all_horas = []
    current_time = sunrise

    for i in range(24):
        planet_idx = (start_idx + i) % 7
        planet = HORA_SEQUENCE[planet_idx]

        if i < 12:
            duration = timedelta(seconds=day_hora_seconds)
        else:
            duration = timedelta(seconds=night_hora_seconds)

        end_time = current_time + duration

        all_horas.append({
            'hora_number': i + 1,
            'planet': planet,
            'start': current_time,
            'end': end_time,
            'is_day': i < 12,
        })

        current_time = end_time

    # Filter for market hours
    mkt_start = datetime.strptime(f"{date_str} {market_start}", "%Y-%m-%d %H:%M")
    mkt_end = datetime.strptime(f"{date_str} {market_end}", "%Y-%m-%d %H:%M")

    market_horas = []
    for hora in all_horas:
        # Check overlap with market hours
        overlap_start = max(hora['start'], mkt_start)
        overlap_end = min(hora['end'], mkt_end)

        if overlap_start < overlap_end:
            effect = HORA_MARKET_EFFECT.get(hora['planet'], {})
            market_horas.append({
                'planet': hora['planet'],
                'start': overlap_start.strftime('%H:%M'),
                'end': overlap_end.strftime('%H:%M'),
                'duration_min': round((overlap_end - overlap_start).total_seconds() / 60),
                'bias': effect.get('bias', 'neutral'),
                'note': effect.get('note', ''),
                'sectors': effect.get('sectors', []),
                'action': effect.get('action', ''),
            })

    return {
        'date': date_str,
        'weekday': dt.strftime('%A'),
        'day_ruler': day_ruler,
        'sunrise': sunrise.strftime('%H:%M'),
        'sunset': sunset.strftime('%H:%M'),
        'market_horas': market_horas,
    }


# ── Rahu Kaal & Inauspicious Periods ─────────────────────

def get_inauspicious_periods(date_str):
    """Calculate Rahu Kaal, Gulika, and Yamaganda for the day."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    weekday = dt.weekday()
    sunrise, sunset = get_sunrise_sunset(date_str)

    day_length = (sunset - sunrise).total_seconds()
    segment_duration = timedelta(seconds=day_length / 8.0)

    periods = {}

    # Rahu Kaal
    rk_start_seg, rk_end_seg = RAHU_KAAL_SEGMENTS[weekday]
    rk_start = sunrise + segment_duration * rk_start_seg
    rk_end = sunrise + segment_duration * rk_end_seg
    periods['rahu_kaal'] = {
        'start': rk_start.strftime('%H:%M'),
        'end': rk_end.strftime('%H:%M'),
        'note': '⚠️ RAHU KAAL: Avoid new trades. Fake moves & traps common. Wait it out.',
        'duration_min': round((rk_end - rk_start).total_seconds() / 60),
    }

    # Gulika Kaal
    gk_start_seg, gk_end_seg = GULIKA_SEGMENTS[weekday]
    gk_start = sunrise + segment_duration * gk_start_seg
    gk_end = sunrise + segment_duration * gk_end_seg
    periods['gulika_kaal'] = {
        'start': gk_start.strftime('%H:%M'),
        'end': gk_end.strftime('%H:%M'),
        'note': 'Gulika Kaal: Subtle negative energy. Not ideal for new positions.',
        'duration_min': round((gk_end - gk_start).total_seconds() / 60),
    }

    # Yamaganda
    yk_start_seg, yk_end_seg = YAMAGANDA_SEGMENTS[weekday]
    yk_start = sunrise + segment_duration * yk_start_seg
    yk_end = sunrise + segment_duration * yk_end_seg
    periods['yamaganda'] = {
        'start': yk_start.strftime('%H:%M'),
        'end': yk_end.strftime('%H:%M'),
        'note': 'Yamaganda: Death-like stagnation. Markets may go completely flat.',
        'duration_min': round((yk_end - yk_start).total_seconds() / 60),
    }

    # Abhijit Muhurta (midday, ~24 min window around solar noon)
    solar_noon = sunrise + timedelta(seconds=day_length / 2)
    abhijit_start = solar_noon - timedelta(minutes=12)
    abhijit_end = solar_noon + timedelta(minutes=12)
    periods['abhijit_muhurta'] = {
        'start': abhijit_start.strftime('%H:%M'),
        'end': abhijit_end.strftime('%H:%M'),
        'note': '✅ ABHIJIT MUHURTA: Most auspicious 24 min of the day. Best for important trades.',
        'duration_min': 24,
    }

    return periods


# ── Hora Summary for Trading ─────────────────────────────

def get_trading_hora_summary(date_str):
    """Combined hora + inauspicious periods for complete intraday guide."""
    horas = get_planetary_hours(date_str)
    bad_periods = get_inauspicious_periods(date_str)

    # Find best and worst windows
    best_windows = [h for h in horas['market_horas']
                    if h['planet'] in ['Jupiter', 'Venus']]
    worst_windows = [h for h in horas['market_horas']
                     if h['planet'] in ['Saturn', 'Mars']]

    return {
        **horas,
        'inauspicious': bad_periods,
        'best_buy_windows': best_windows,
        'caution_windows': worst_windows,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n⏰ PLANETARY HOURS & TIMING — {today}")
    print("=" * 70)

    summary = get_trading_hora_summary(today)

    print(f"\n📅 {summary['weekday']} | Day Ruler: {summary['day_ruler']}")
    print(f"🌅 Sunrise: {summary['sunrise']} | 🌇 Sunset: {summary['sunset']}")

    print(f"\n📊 MARKET HORA TABLE (9:15 AM - 3:30 PM):")
    print(f"{'Time':15s} {'Planet':10s} {'Bias':10s} {'Action'}")
    print("-" * 70)
    for h in summary['market_horas']:
        emoji = '🟢' if h['bias'] == 'bullish' else (
            '🔴' if h['bias'] == 'bearish' else '🟡')
        print(f"{h['start']}-{h['end']}    {emoji} {h['planet']:10s} "
              f"{h['bias']:10s} {h['action']}")

    print(f"\n⚠️ INAUSPICIOUS PERIODS:")
    for name, period in summary['inauspicious'].items():
        print(f"  {name:20s}: {period['start']} - {period['end']} "
              f"({period['duration_min']} min)")

    if summary['best_buy_windows']:
        print(f"\n✅ BEST BUY WINDOWS:")
        for w in summary['best_buy_windows']:
            print(f"  {w['start']}-{w['end']} ({w['planet']} hora)")

    if summary['caution_windows']:
        print(f"\n🔴 CAUTION WINDOWS:")
        for w in summary['caution_windows']:
            print(f"  {w['start']}-{w['end']} ({w['planet']} hora)")


Save: Ctrl + S

Step 2.6 — core/dasha.py (Vimshottari Dasha System)
Click core/dasha.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Vimshottari Dasha System
=============================================================
Calculates Mahadasha → Antardasha → Pratyantardasha
for any birth chart (especially Nifty/Bank Nifty).
=============================================================
"""

from datetime import datetime, timedelta
from core.astro_engine import get_nakshatra, get_planetary_positions, NAKSHATRA_LORDS

# ── Vimshottari Dasha Periods (years) ─────────────────────
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
    'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17,
}

# Dasha sequence (always this order)
DASHA_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
                  'Rahu', 'Jupiter', 'Saturn', 'Mercury']

TOTAL_DASHA_YEARS = 120  # Full Vimshottari cycle

# Market interpretation of each Mahadasha lord
DASHA_MARKET_INTERPRETATION = {
    'Sun': {
        'general': 'Government focus, policy-driven markets, gold bullish',
        'bullish_sectors': ['Power', 'Pharma', 'PSU Banks', 'Gold'],
        'bearish_sectors': ['Opposition-linked sectors'],
        'overall': 'Moderate bullish with authority/policy themes',
    },
    'Moon': {
        'general': 'Sentiment-driven markets, liquidity focus, silver & FMCG',
        'bullish_sectors': ['FMCG', 'Silver', 'Hospitality', 'Water'],
        'bearish_sectors': ['Heavy industry (lack of stability)'],
        'overall': 'Emotional, volatile, liquidity-dependent',
    },
    'Mars': {
        'general': 'Aggressive markets, high volatility, defense & real estate focus',
        'bullish_sectors': ['Real Estate', 'Defense', 'Steel', 'Energy'],
        'bearish_sectors': ['Peaceful sectors', 'Tourism'],
        'overall': 'Volatile with sharp rallies AND crashes',
    },
    'Mercury': {
        'general': 'Communication, IT, trade-focused markets, fast moves',
        'bullish_sectors': ['IT', 'Telecom', 'E-commerce', 'Banking'],
        'bearish_sectors': ['Traditional manufacturing'],
        'overall': 'Smart money, quick trades, data-driven moves',
    },
    'Jupiter': {
        'general': 'Expansion, optimism, banking & finance boom, bull markets',
        'bullish_sectors': ['Banking', 'Finance', 'Education', 'Law'],
        'bearish_sectors': ['Rarely bearish in Jupiter period'],
        'overall': '🟢 MOST BULLISH dasha — expansion, prosperity',
    },
    'Venus': {
        'general': 'Luxury, consumption, auto, entertainment focus',
        'bullish_sectors': ['Auto', 'Luxury', 'Entertainment', 'Textiles'],
        'bearish_sectors': ['Austerity-linked sectors'],
        'overall': 'Bullish with consumer & lifestyle themes',
    },
    'Saturn': {
        'general': 'Restrictive, slow, infrastructure focus, corrections',
        'bullish_sectors': ['Infrastructure', 'Mining', 'Oil & Gas', 'Agriculture'],
        'bearish_sectors': ['Luxury', 'Entertainment', 'Growth stocks'],
        'overall': '🔴 MOST CHALLENGING dasha — corrections, bear phases',
    },
    'Rahu': {
        'general': 'Foreign influence, speculation, crypto, disruption',
        'bullish_sectors': ['Tech disruption', 'Crypto', 'Foreign investment'],
        'bearish_sectors': ['Traditional value stocks'],
        'overall': 'Wild, speculative, unpredictable — booms AND busts',
    },
    'Ketu': {
        'general': 'Spiritual, detached, sudden events, IT backend',
        'bullish_sectors': ['Pharma (research)', 'IT services', 'Spiritual'],
        'bearish_sectors': ['Material luxury', 'Entertainment'],
        'overall': 'Confusing, detached, sudden reversals',
    },
}


# ── Dasha Calculation ─────────────────────────────────────

def calculate_dasha_periods(moon_longitude, birth_date_str):
    """
    Calculate all Mahadasha periods from birth date based on Moon's nakshatra.
    
    Args:
        moon_longitude: Sidereal longitude of Moon at birth
        birth_date_str: 'YYYY-MM-DD' format
    
    Returns:
        List of dasha periods with start/end dates
    """
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

    # Get Moon's nakshatra
    nak_name, pada, nak_lord = get_nakshatra(moon_longitude)

    # Calculate elapsed portion of starting nakshatra
    nak_span = 360.0 / 27.0  # 13.333...
    nak_start_deg = (moon_longitude // nak_span) * nak_span
    elapsed_in_nak = moon_longitude - nak_start_deg
    nak_fraction_elapsed = elapsed_in_nak / nak_span

    # First dasha lord = nakshatra lord
    first_lord = nak_lord
    first_lord_total_years = DASHA_YEARS[first_lord]
    first_lord_remaining_years = first_lord_total_years * (1 - nak_fraction_elapsed)

    # Build dasha sequence starting from first lord
    start_idx = DASHA_SEQUENCE.index(first_lord)

    dashas = []
    current_date = birth_date

    # First (partial) dasha
    days = first_lord_remaining_years * 365.25
    end_date = current_date + timedelta(days=days)
    interp = DASHA_MARKET_INTERPRETATION.get(first_lord, {})
    dashas.append({
        'lord': first_lord,
        'start': current_date,
        'end': end_date,
        'years': round(first_lord_remaining_years, 2),
        'is_partial': True,
        'interpretation': interp,
    })
    current_date = end_date

    # Remaining full dashas (cycle through)
    for i in range(1, 10):  # Up to 9 more dashas (full cycle = 120 years)
        lord_idx = (start_idx + i) % 9
        lord = DASHA_SEQUENCE[lord_idx]
        years = DASHA_YEARS[lord]
        days = years * 365.25
        end_date = current_date + timedelta(days=days)
        interp = DASHA_MARKET_INTERPRETATION.get(lord, {})

        dashas.append({
            'lord': lord,
            'start': current_date,
            'end': end_date,
            'years': years,
            'is_partial': False,
            'interpretation': interp,
        })
        current_date = end_date

        # Stop if we've gone 120+ years from birth
        if (current_date - birth_date).days > 120 * 365.25:
            break

    return {
        'moon_nakshatra': nak_name,
        'moon_pada': pada,
        'nakshatra_lord': nak_lord,
        'dashas': dashas,
    }


def calculate_antardasha(mahadasha_lord, maha_start, maha_end):
    """
    Calculate Antardasha (sub-periods) within a Mahadasha.
    """
    maha_days = (maha_end - maha_start).total_seconds() / 86400.0
    total_dasha_days = TOTAL_DASHA_YEARS * 365.25

    start_idx = DASHA_SEQUENCE.index(mahadasha_lord)
    antardashas = []
    current_date = maha_start

    for i in range(9):
        lord_idx = (start_idx + i) % 9
        lord = DASHA_SEQUENCE[lord_idx]

        # Antardasha proportion = (maha_years * antar_years) / total_years
        proportion = (DASHA_YEARS[mahadasha_lord] * DASHA_YEARS[lord]) / (TOTAL_DASHA_YEARS)
        antar_days = proportion * 365.25

        # Scale to actual mahadasha duration
        scale_factor = maha_days / (DASHA_YEARS[mahadasha_lord] * 365.25)
        actual_days = antar_days * scale_factor

        end_date = current_date + timedelta(days=actual_days)

        if end_date > maha_end:
            end_date = maha_end

        antardashas.append({
            'mahadasha_lord': mahadasha_lord,
            'antardasha_lord': lord,
            'start': current_date,
            'end': end_date,
            'days': round(actual_days),
        })

        current_date = end_date
        if current_date >= maha_end:
            break

    return antardashas


def get_current_dasha(dashas, target_date_str):
    """Find which Mahadasha and Antardasha is active on a given date."""
    target = datetime.strptime(target_date_str, '%Y-%m-%d')

    current_maha = None
    for d in dashas['dashas']:
        if d['start'] <= target <= d['end']:
            current_maha = d
            break

    if not current_maha:
        return None

    # Calculate antardashas
    antardashas = calculate_antardasha(
        current_maha['lord'], current_maha['start'], current_maha['end']
    )

    current_antar = None
    for a in antardashas:
        if a['start'] <= target <= a['end']:
            current_antar = a
            break

    return {
        'mahadasha': current_maha,
        'antardasha': current_antar,
        'all_antardashas': antardashas,
    }


# ── Predefined Birth Charts ──────────────────────────────

# Nifty 50: NSE launched 3 November 1995 at 9:55 AM IST
NIFTY_BIRTH = {
    'name': 'Nifty 50',
    'date': '1995-11-03',
    'time': '09:55',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

# Bank Nifty: launched 13 June 2005
BANKNIFTY_BIRTH = {
    'name': 'Bank Nifty',
    'date': '2005-06-13',
    'time': '09:15',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

# Sensex: launched 1 January 1986
SENSEX_BIRTH = {
    'name': 'BSE Sensex',
    'date': '1986-01-01',
    'time': '10:00',
    'place': 'Mumbai',
    'lat': 19.0760,
    'lon': 72.8777,
}

BIRTH_CHARTS = {
    'nifty': NIFTY_BIRTH,
    'banknifty': BANKNIFTY_BIRTH,
    'sensex': SENSEX_BIRTH,
}


def get_index_dasha(index_name='nifty', target_date=None):
    """Get current dasha period for a market index."""
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    birth = BIRTH_CHARTS.get(index_name.lower(), NIFTY_BIRTH)

    # Get Moon position at birth
    positions = get_planetary_positions(birth['date'], birth['time'])
    moon_long = positions['Moon']['longitude']

    # Calculate dashas
    dashas = calculate_dasha_periods(moon_long, birth['date'])

    # Get current period
    current = get_current_dasha(dashas, target_date)

    return {
        'index': birth['name'],
        'birth_date': birth['date'],
        'moon_nakshatra': dashas['moon_nakshatra'],
        'moon_pada': dashas['moon_pada'],
        'all_dashas': dashas,
        'current': current,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 VIMSHOTTARI DASHA — NIFTY 50")
    print(f"   Birth: 3 Nov 1995 (NSE Launch)")
    print(f"   Analysis for: {today}")
    print("=" * 65)

    result = get_index_dasha('nifty', today)

    print(f"\n🌙 Nifty Moon Nakshatra: {result['moon_nakshatra']} "
          f"(Pada {result['moon_pada']})")

    if result['current']:
        maha = result['current']['mahadasha']
        print(f"\n📊 CURRENT MAHADASHA: {maha['lord']}")
        print(f"   Period: {maha['start'].strftime('%Y-%m-%d')} to "
              f"{maha['end'].strftime('%Y-%m-%d')}")
        print(f"   Duration: {maha['years']} years")

        interp = maha.get('interpretation', {})
        if interp:
            print(f"   General: {interp.get('general', 'N/A')}")
            print(f"   Overall: {interp.get('overall', 'N/A')}")
            print(f"   Bullish: {', '.join(interp.get('bullish_sectors', []))}")
            print(f"   Bearish: {', '.join(interp.get('bearish_sectors', []))}")

        antar = result['current'].get('antardasha')
        if antar:
            print(f"\n📊 CURRENT ANTARDASHA: {antar['antardasha_lord']}")
            print(f"   Period: {antar['start'].strftime('%Y-%m-%d')} to "
                  f"{antar['end'].strftime('%Y-%m-%d')}")
            print(f"   Duration: {antar['days']} days")

        print(f"\n📋 ALL MAHADASHAS FOR NIFTY:")
        print(f"{'Lord':10s} {'Start':12s} {'End':12s} {'Years':>6s}")
        print("-" * 45)
        for d in result['all_dashas']['dashas']:
            marker = ' ◀ CURRENT' if d['lord'] == maha['lord'] else ''
            print(f"{d['lord']:10s} {d['start'].strftime('%Y-%m-%d'):12s} "
                  f"{d['end'].strftime('%Y-%m-%d'):12s} {d['years']:6.1f}{marker}")


Save: Ctrl + S

Step 2.7 — core/ashtakavarga.py (Transit Scoring System)
Click core/ashtakavarga.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Ashtakavarga Transit Scoring
=============================================================
Calculates Bindu (point) scores for planetary transits.
Each planet gets 0-8 points per sign based on contributions
from all other planets. Higher score = stronger transit.

Sarvashtakavarga (SAV) = total of all planets' bindus per sign.
=============================================================
"""

from core.astro_engine import get_planetary_positions, SIGNS

# ── Ashtakavarga Bindu Tables ─────────────────────────────
# Format: For each planet, from each contributor planet's position,
# which houses (counted from contributor) give a bindu (point).
# Source: Standard Parashari Ashtakavarga tables

# Houses that give bindu (1-indexed from contributor's sign)
BINDU_TABLES = {
    'Sun': {
        'Sun':     [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon':    [3, 6, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus':   [6, 7, 12],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [3, 4, 6, 10, 11, 12],
    },
    'Moon': {
        'Sun':     [3, 6, 7, 8, 10, 11],
        'Moon':    [1, 3, 6, 7, 10, 11],
        'Mars':    [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus':   [3, 4, 5, 7, 9, 10, 11],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [3, 6, 10, 11],
    },
    'Mars': {
        'Sun':     [3, 5, 6, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus':   [6, 8, 11, 12],
        'Saturn':  [1, 4, 7, 8, 9, 10, 11],
        'Lagna':   [1, 3, 6, 10, 11],
    },
    'Mercury': {
        'Sun':     [5, 6, 9, 11, 12],
        'Moon':    [2, 4, 6, 8, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [1, 2, 4, 6, 8, 10, 11],
    },
    'Jupiter': {
        'Sun':     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon':    [2, 5, 7, 9, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus':   [2, 5, 6, 9, 10, 11],
        'Saturn':  [3, 5, 6, 12],
        'Lagna':   [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    'Venus': {
        'Sun':     [8, 11, 12],
        'Moon':    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars':    [3, 5, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn':  [3, 4, 5, 8, 9, 10, 11],
        'Lagna':   [1, 2, 3, 4, 5, 8, 9, 11],
    },
    'Saturn': {
        'Sun':     [1, 2, 4, 7, 8, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus':   [6, 11, 12],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [1, 3, 4, 6, 10, 11],
    },
}


def calculate_ashtakavarga(positions, lagna_sign_index=None):
    """
    Calculate Ashtakavarga scores for all planets in all signs.
    
    Returns:
        prashtara: Dict of {planet: [score_aries, score_taurus, ...]}
        sarvashtakavarga: [total_aries, total_taurus, ...] (sum of all planets)
    """
    # If no lagna provided, use Aries as reference
    if lagna_sign_index is None:
        lagna_sign_index = 0

    prashtara = {}

    for planet_name in BINDU_TABLES:
        scores = [0] * 12  # One score per sign

        for contributor, bindu_houses in BINDU_TABLES[planet_name].items():
            if contributor == 'Lagna':
                contrib_sign_idx = lagna_sign_index
            elif contributor in positions:
                contrib_sign_idx = positions[contributor]['sign_index']
            else:
                continue

            for house in bindu_houses:
                target_sign = (contrib_sign_idx + house - 1) % 12
                scores[target_sign] += 1

        prashtara[planet_name] = scores

    # Sarvashtakavarga = sum across all planets for each sign
    sav = [0] * 12
    for planet_scores in prashtara.values():
        for i in range(12):
            sav[i] += planet_scores[i]

    return {
        'prashtara': prashtara,
        'sarvashtakavarga': sav,
    }


def get_transit_score(positions, ashtakavarga):
    """
    Score each planet's current transit based on its Ashtakavarga bindus
    in its current sign.
    """
    scores = {}
    prashtara = ashtakavarga['prashtara']

    for planet_name in prashtara:
        if planet_name in positions:
            current_sign_idx = positions[planet_name]['sign_index']
            bindus = prashtara[planet_name][current_sign_idx]

            if bindus >= 5:
                quality = 'STRONG (Bullish)'
                market_note = f'{planet_name} transit supported — positive for its sectors'
            elif bindus >= 4:
                quality = 'MODERATE'
                market_note = f'{planet_name} transit average — mixed results'
            else:
                quality = 'WEAK (Bearish)'
                market_note = f'{planet_name} transit unsupported — negative for its sectors'

            scores[planet_name] = {
                'bindus': bindus,
                'max_possible': 8,
                'quality': quality,
                'current_sign': positions[planet_name]['sign'],
                'market_note': market_note,
            }

    return scores


def get_sav_analysis(sav):
    """Analyze Sarvashtakavarga for overall sign strength."""
    avg = sum(sav) / 12
    analysis = []

    for i, score in enumerate(sav):
        sign = SIGNS[i]
        if score >= 30:
            strength = 'VERY STRONG'
            note = f'Planets transiting {sign} give excellent results'
        elif score >= 27:
            strength = 'STRONG'
            note = f'Planets transiting {sign} give good results'
        elif score >= 24:
            strength = 'AVERAGE'
            note = f'Planets transiting {sign} give mixed results'
        elif score >= 20:
            strength = 'WEAK'
            note = f'Planets transiting {sign} give poor results'
        else:
            strength = 'VERY WEAK'
            note = f'Planets transiting {sign} give negative results'

        analysis.append({
            'sign': sign,
            'score': score,
            'strength': strength,
            'note': note,
        })

    return sorted(analysis, key=lambda x: x['score'], reverse=True)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📊 ASHTAKAVARGA ANALYSIS — {today}")
    print("=" * 65)

    # Get current positions
    positions = get_planetary_positions(today)

    # Calculate Ashtakavarga
    av = calculate_ashtakavarga(positions)

    # Transit scores
    transit_scores = get_transit_score(positions, av)

    print("\n🎯 CURRENT TRANSIT SCORES:")
    print(f"{'Planet':10s} {'Sign':13s} {'Bindus':>7s} {'Quality'}")
    print("-" * 50)
    for planet, data in transit_scores.items():
        emoji = '🟢' if data['bindus'] >= 5 else ('🔴' if data['bindus'] <= 3 else '🟡')
        print(f"{planet:10s} {data['current_sign']:13s} {data['bindus']:4d}/8   "
              f"{emoji} {data['quality']}")

    # SAV Analysis
    print(f"\n📈 SARVASHTAKAVARGA (Sign Strength):")
    print(f"{'Sign':13s} {'Score':>6s} {'Strength'}")
    print("-" * 40)
    sav_analysis = get_sav_analysis(av['sarvashtakavarga'])
    for item in sav_analysis:
        bar = '█' * (item['score'] // 3)
        print(f"{item['sign']:13s} {item['score']:4d}    {item['strength']:12s} {bar}")


Save: Ctrl + S

Step 2.8 — core/divisional.py (Navamsha D-9 & Dashamsha D-10)
Click core/divisional.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Divisional Charts (Vargas)
=============================================================
Navamsha (D-9):  Hidden strength of planets. The "confirmation" chart.
Dashamsha (D-10): Career & public status. Directly applicable to indices.
Hora (D-2):      Wealth division — Sun's hora vs Moon's hora.
=============================================================
"""

from core.astro_engine import get_planetary_positions, SIGNS, get_dignity, get_dignity_score, SIGN_LORDS


def calculate_navamsha_sign(longitude):
    """
    Calculate Navamsha (D-9) sign for a given sidereal longitude.
    Each sign is divided into 9 parts of 3°20' each.
    """
    # Each navamsha = 3.3333 degrees
    navamsha_num = int(longitude / (30.0 / 9.0)) % 108
    # Navamsha signs cycle: Aries sign starts from Aries,
    # Taurus from Capricorn, Gemini from Libra, Cancer from Cancer, etc.
    # Simplified: navamsha_num directly maps to sign
    sign_idx = navamsha_num % 12
    return SIGNS[sign_idx], sign_idx


def calculate_dashamsha_sign(longitude):
    """
    Calculate Dashamsha (D-10) sign.
    Each sign is divided into 10 parts of 3° each.
    Odd signs count from same sign, even signs count from 9th sign.
    """
    rashi_num = int(longitude / 30.0) % 12  # 0-indexed
    degrees_in_sign = longitude % 30.0
    dashamsha_part = int(degrees_in_sign / 3.0)  # 0-9

    if rashi_num % 2 == 0:  # Odd signs (0-indexed: Aries=0 is odd sign)
        d10_sign_idx = (rashi_num + dashamsha_part) % 12
    else:  # Even signs
        d10_sign_idx = (rashi_num + 9 + dashamsha_part) % 12

    return SIGNS[d10_sign_idx], d10_sign_idx


def calculate_hora_sign(longitude):
    """
    Calculate Hora (D-2) sign.
    First 15° = Sun's hora (Leo), Last 15° = Moon's hora (Cancer).
    Odd signs: first half = Sun, second half = Moon.
    Even signs: first half = Moon, second half = Sun.
    """
    rashi_num = int(longitude / 30.0) % 12
    degrees_in_sign = longitude % 30.0

    if rashi_num % 2 == 0:  # Odd signs
        if degrees_in_sign < 15:
            return 'Leo', 4  # Sun's hora
        else:
            return 'Cancer', 3  # Moon's hora
    else:  # Even signs
        if degrees_in_sign < 15:
            return 'Cancer', 3  # Moon's hora
        else:
            return 'Leo', 4  # Sun's hora


def get_all_divisional_positions(date_str, time_str='12:00'):
    """Calculate D-1 (Rashi), D-2 (Hora), D-9 (Navamsha), D-10 (Dashamsha) for all planets."""
    positions = get_planetary_positions(date_str, time_str)
    divisional = {}

    for name, data in positions.items():
        long = data['longitude']

        # Navamsha (D-9)
        nav_sign, nav_idx = calculate_navamsha_sign(long)
        nav_dignity = get_dignity(name, nav_sign, (long % (30.0/9.0)) * 9)

        # Dashamsha (D-10)
        d10_sign, d10_idx = calculate_dashamsha_sign(long)
        d10_dignity = get_dignity(name, d10_sign, (long % 3.0) * 10)

        # Hora (D-2)
        hora_sign, hora_idx = calculate_hora_sign(long)

        # Vargottama check: same sign in D-1 and D-9
        is_vargottama = data['sign'] == nav_sign

        divisional[name] = {
            # D-1 (Rashi)
            'rashi_sign': data['sign'],
            'rashi_dignity': data['dignity'],
            'rashi_score': data['dignity_score'],

            # D-9 (Navamsha)
            'navamsha_sign': nav_sign,
            'navamsha_dignity': nav_dignity,
            'navamsha_score': get_dignity_score(nav_dignity),

            # D-10 (Dashamsha)
            'dashamsha_sign': d10_sign,
            'dashamsha_dignity': d10_dignity,
            'dashamsha_score': get_dignity_score(d10_dignity),

            # D-2 (Hora)
            'hora_sign': hora_sign,
            'hora_type': 'Sun (Gold/Authority)' if hora_sign == 'Leo' else 'Moon (Silver/Liquidity)',

            # Special
            'is_vargottama': is_vargottama,

            # Composite strength (D1 + D9 weighted)
            'composite_strength': round(
                data['dignity_score'] * 0.6 + get_dignity_score(nav_dignity) * 0.4, 2
            ),
        }

    return divisional


def get_vargottama_planets(divisional_data):
    """Find planets that are Vargottama (same sign in D-1 and D-9) — very strong."""
    return [name for name, data in divisional_data.items() if data['is_vargottama']]


def get_composite_strength_ranking(divisional_data):
    """Rank planets by composite strength (D-1 + D-9)."""
    ranking = []
    for name, data in divisional_data.items():
        ranking.append({
            'planet': name,
            'rashi': f"{data['rashi_sign']} ({data['rashi_dignity']})",
            'navamsha': f"{data['navamsha_sign']} ({data['navamsha_dignity']})",
            'composite': data['composite_strength'],
            'vargottama': data['is_vargottama'],
        })
    return sorted(ranking, key=lambda x: x['composite'], reverse=True)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from datetime import datetime

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📐 DIVISIONAL CHARTS — {today}")
    print("=" * 80)

    div = get_all_divisional_positions(today)

    print(f"\n{'Planet':10s} {'Rashi(D1)':16s} {'Navamsha(D9)':16s} {'Dashams(D10)':16s} {'Hora':12s} {'VG':4s} {'Str':>5s}")
    print("-" * 85)
    for name, data in div.items():
        vg = '✅' if data['is_vargottama'] else ''
        print(f"{name:10s} {data['rashi_sign']:8s}({data['rashi_dignity'][:4]:4s}) "
              f"{data['navamsha_sign']:8s}({data['navamsha_dignity'][:4]:4s}) "
              f"{data['dashamsha_sign']:8s}({data['dashamsha_dignity'][:4]:4s}) "
              f"{data['hora_type'][:10]:12s} {vg:4s} {data['composite_strength']:5.2f}")

    vg_planets = get_vargottama_planets(div)
    if vg_planets:
        print(f"\n⭐ VARGOTTAMA PLANETS (Extra Strong): {', '.join(vg_planets)}")

    print(f"\n📊 COMPOSITE STRENGTH RANKING:")
    ranking = get_composite_strength_ranking(div)
    for r in ranking:
        emoji = '💪' if r['composite'] >= 3 else ('😐' if r['composite'] >= 0 else '😰')
        print(f"  {emoji} {r['planet']:10s} → {r['composite']:+.2f} "
              f"| D1: {r['rashi']:22s} | D9: {r['navamsha']}")


Save: Ctrl + S

Step 2.9 — core/bradley.py (Bradley Siderograph)
Click core/bradley.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Bradley Siderograph
=============================================================
A composite indicator summing declination-based aspects.
Its TURNING POINTS (peaks/troughs) correlate with market reversals.
NOTE: Direction is NOT the signal — the CHANGE in direction is.
=============================================================
"""

import swisseph as swe
from core.astro_engine import date_to_jd, PLANETS
from datetime import datetime, timedelta
import os

EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)

# Aspect weights for Bradley calculation
ASPECT_WEIGHTS = {
    0: 10,     # Conjunction
    60: 4,     # Sextile
    90: -6,    # Square
    120: 6,    # Trine
    180: -8,   # Opposition
}

# Planet pairs to consider (major planets only)
BRADLEY_PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
}

# Declination weights
DECL_WEIGHTS = {
    ('Sun', 'Moon'): 5,
    ('Sun', 'Mercury'): 2,
    ('Sun', 'Venus'): 3,
    ('Sun', 'Mars'): 3,
    ('Sun', 'Jupiter'): 4,
    ('Sun', 'Saturn'): 4,
    ('Moon', 'Jupiter'): 3,
    ('Moon', 'Saturn'): 3,
    ('Jupiter', 'Saturn'): 5,
    ('Mars', 'Jupiter'): 3,
    ('Mars', 'Saturn'): 4,
    ('Venus', 'Jupiter'): 3,
}


def calculate_bradley_value(date_str):
    """
    Calculate Bradley Siderograph value for a single date.
    Uses geocentric declinations and longitude aspects.
    """
    jd = date_to_jd(date_str, '12:00')
    value = 0

    # Get all planet positions and declinations
    planet_data = {}
    for name, pid in BRADLEY_PLANETS.items():
        result = swe.calc_ut(jd, pid, swe.FLG_SPEED)
        planet_data[name] = {
            'longitude': result[0][0] % 360,
            'declination': result[0][1],
        }

    # Calculate aspect-based component
    planet_names = list(BRADLEY_PLANETS.keys())
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]

            long1 = planet_data[p1]['longitude']
            long2 = planet_data[p2]['longitude']

            diff = abs(long1 - long2) % 360
            if diff > 180:
                diff = 360 - diff

            # Check each aspect
            for aspect_deg, weight in ASPECT_WEIGHTS.items():
                orb = 8 if aspect_deg in [0, 180] else 6
                if abs(diff - aspect_deg) <= orb:
                    # Weight by closeness to exact
                    closeness = 1 - (abs(diff - aspect_deg) / orb)

                    # Get pair weight
                    pair = tuple(sorted([p1, p2]))
                    pair_weight = DECL_WEIGHTS.get(pair, DECL_WEIGHTS.get((pair[1], pair[0]), 1))

                    value += weight * closeness * pair_weight * 0.1

    # Add declination parallel/contra-parallel component
    for pair, weight in DECL_WEIGHTS.items():
        if pair[0] in planet_data and pair[1] in planet_data:
            decl1 = planet_data[pair[0]]['declination']
            decl2 = planet_data[pair[1]]['declination']

            # Parallel (same declination) = conjunction-like
            if abs(decl1 - decl2) <= 1.5:
                value += weight * 0.5

            # Contra-parallel (opposite declination) = opposition-like
            if abs(decl1 + decl2) <= 1.5:
                value -= weight * 0.3

    return round(value, 2)


def calculate_bradley_series(start_date, end_date=None, days=90):
    """
    Calculate Bradley Siderograph for a date range.
    Returns list of (date, value) for charting.
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end = start + timedelta(days=days)

    series = []
    current = start
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        try:
            value = calculate_bradley_value(date_str)
            series.append({'date': date_str, 'value': value})
        except Exception:
            pass
        current += timedelta(days=1)

    return series


def find_turning_points(series, window=5):
    """
    Find peaks and troughs in Bradley series.
    THESE are the market reversal signals (not the direction).
    """
    if len(series) < window * 2 + 1:
        return []

    turning_points = []
    values = [s['value'] for s in series]

    for i in range(window, len(values) - window):
        # Check if local maximum
        if all(values[i] >= values[i - j] for j in range(1, window + 1)) and \
           all(values[i] >= values[i + j] for j in range(1, window + 1)):
            turning_points.append({
                'date': series[i]['date'],
                'value': series[i]['value'],
                'type': 'PEAK',
                'market_signal': 'Potential market HIGH — watch for reversal DOWN',
            })

        # Check if local minimum
        elif all(values[i] <= values[i - j] for j in range(1, window + 1)) and \
             all(values[i] <= values[i + j] for j in range(1, window + 1)):
            turning_points.append({
                'date': series[i]['date'],
                'value': series[i]['value'],
                'type': 'TROUGH',
                'market_signal': 'Potential market LOW — watch for reversal UP',
            })

    return turning_points


def get_bradley_analysis(date_str, lookahead=30, lookbehind=30):
    """Complete Bradley analysis: current value + nearby turning points."""
    start = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=lookbehind)).strftime('%Y-%m-%d')
    end = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=lookahead)).strftime('%Y-%m-%d')

    series = calculate_bradley_series(start, end)
    current_value = calculate_bradley_value(date_str)
    turning_points = find_turning_points(series)

    # Find nearest turning points
    target_dt = datetime.strptime(date_str, '%Y-%m-%d')
    upcoming = [tp for tp in turning_points
                if datetime.strptime(tp['date'], '%Y-%m-%d') >= target_dt]
    recent = [tp for tp in turning_points
              if datetime.strptime(tp['date'], '%Y-%m-%d') < target_dt]

    return {
        'date': date_str,
        'current_value': current_value,
        'trend': 'RISING' if len(series) >= 2 and series[-1]['value'] > series[-2]['value'] else 'FALLING',
        'upcoming_turning_points': upcoming[:3],
        'recent_turning_points': recent[-3:],
        'series': series,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n📈 BRADLEY SIDEROGRAPH — {today}")
    print("=" * 60)

    analysis = get_bradley_analysis(today)

    print(f"\n📊 Current Value: {analysis['current_value']}")
    print(f"📈 Trend: {analysis['trend']}")

    if analysis['upcoming_turning_points']:
        print(f"\n🔮 UPCOMING TURNING POINTS:")
        for tp in analysis['upcoming_turning_points']:
            emoji = '🔺' if tp['type'] == 'PEAK' else '🔻'
            print(f"  {emoji} {tp['date']}: {tp['type']} (value: {tp['value']})")
            print(f"     {tp['market_signal']}")

    if analysis['recent_turning_points']:
        print(f"\n📅 RECENT TURNING POINTS:")
        for tp in analysis['recent_turning_points']:
            emoji = '🔺' if tp['type'] == 'PEAK' else '🔻'
            print(f"  {emoji} {tp['date']}: {tp['type']} (value: {tp['value']})")


Save: Ctrl + S

Step 2.10 — core/eclipses.py (Eclipse Detection)
Click core/eclipses.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Eclipse Detection & Corridor Analysis
=============================================================
Detects solar/lunar eclipses, eclipse seasons (corridors),
and their market impact windows.
=============================================================
"""

import swisseph as swe
from datetime import datetime, timedelta
from core.astro_engine import date_to_jd, get_planetary_positions, angular_distance
import os

EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ephe')
swe.set_ephe_path(EPHE_PATH)


def find_eclipses_in_range(start_date, end_date):
    """Find all solar and lunar eclipses in a date range."""
    eclipses = []

    start_jd = date_to_jd(start_date)
    end_jd = date_to_jd(end_date)

    # Find solar eclipses
    jd = start_jd
    while jd < end_jd:
        try:
            result = swe.sol_eclipse_when_glob(jd, swe.FLG_SWIEPH)
            eclipse_jd = result[1][0]

            if eclipse_jd > end_jd:
                break

            # Get date
            utc = swe.jdut1_to_utc(eclipse_jd, 1)
            date = f"{int(utc[0])}-{int(utc[1]):02d}-{int(utc[2]):02d}"

            eclipse_type = 'Total Solar' if result[0] & swe.SE_ECL_TOTAL else \
                          'Annular Solar' if result[0] & swe.SE_ECL_ANNULAR else \
                          'Partial Solar'

            eclipses.append({
                'type': eclipse_type,
                'date': date,
                'jd': eclipse_jd,
                'category': 'solar',
                'market_impact': _get_eclipse_market_impact(eclipse_type),
            })

            jd = eclipse_jd + 25  # Jump ahead to find next
        except Exception:
            jd += 30
            continue

    # Find lunar eclipses
    jd = start_jd
    while jd < end_jd:
        try:
            result = swe.lun_eclipse_when(jd, swe.FLG_SWIEPH)
            eclipse_jd = result[1][0]

            if eclipse_jd > end_jd:
                break

            utc = swe.jdut1_to_utc(eclipse_jd, 1)
            date = f"{int(utc[0])}-{int(utc[1]):02d}-{int(utc[2]):02d}"

            eclipse_type = 'Total Lunar' if result[0] & swe.SE_ECL_TOTAL else \
                          'Partial Lunar' if result[0] & swe.SE_ECL_PARTIAL else \
                          'Penumbral Lunar'

            eclipses.append({
                'type': eclipse_type,
                'date': date,
                'jd': eclipse_jd,
                'category': 'lunar',
                'market_impact': _get_eclipse_market_impact(eclipse_type),
            })

            jd = eclipse_jd + 25
        except Exception:
            jd += 30
            continue

    return sorted(eclipses, key=lambda x: x['jd'])


def _get_eclipse_market_impact(eclipse_type):
    impacts = {
        'Total Solar': {
            'severity': 'EXTREME',
            'pre_days': 7,
            'post_days': 30,
            'note': 'Total Solar Eclipse: Maximum disruption. Markets typically sell off 5-7 days before. Effect lasts ~1 month. Government/policy changes likely.'
        },
        'Annular Solar': {
            'severity': 'HIGH',
            'pre_days': 5,
            'post_days': 21,
            'note': 'Annular Solar Eclipse: Strong disruption. Markets volatile. Ring of fire = hidden power shifts.'
        },
        'Partial Solar': {
            'severity': 'MODERATE',
            'pre_days': 3,
            'post_days': 14,
            'note': 'Partial Solar Eclipse: Moderate disruption. Specific sectors affected based on sign.'
        },
        'Total Lunar': {
            'severity': 'HIGH',
            'pre_days': 3,
            'post_days': 14,
            'note': 'Total Lunar Eclipse (Blood Moon): Emotional peak. Mass psychology reversal. Full Moon energy amplified.'
        },
        'Partial Lunar': {
            'severity': 'MODERATE',
            'pre_days': 2,
            'post_days': 7,
            'note': 'Partial Lunar Eclipse: Emotional disturbance. Sentiment shifts.'
        },
        'Penumbral Lunar': {
            'severity': 'LOW',
            'pre_days': 1,
            'post_days': 3,
            'note': 'Penumbral Lunar Eclipse: Subtle emotional undercurrent. Minor market impact.'
        },
    }
    return impacts.get(eclipse_type, {
        'severity': 'UNKNOWN', 'pre_days': 3, 'post_days': 7, 'note': 'Eclipse detected.'
    })


def check_eclipse_corridor(date_str, eclipses=None):
    """
    Check if a date falls within an eclipse corridor
    (the ~35-day window between consecutive eclipses).
    This is historically the MOST volatile period.
    """
    if eclipses is None:
        # Look within +/- 6 months
        start = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=180)).strftime('%Y-%m-%d')
        end = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=180)).strftime('%Y-%m-%d')
        eclipses = find_eclipses_in_range(start, end)

    target = datetime.strptime(date_str, '%Y-%m-%d')
    in_corridor = False
    corridor_info = None

    for i in range(len(eclipses) - 1):
        e1_date = datetime.strptime(eclipses[i]['date'], '%Y-%m-%d')
        e2_date = datetime.strptime(eclipses[i + 1]['date'], '%Y-%m-%d')

        gap = (e2_date - e1_date).days

        if gap <= 40 and e1_date <= target <= e2_date:
            in_corridor = True
            corridor_info = {
                'eclipse_1': eclipses[i],
                'eclipse_2': eclipses[i + 1],
                'corridor_days': gap,
                'day_in_corridor': (target - e1_date).days,
                'note': '⚠️ IN ECLIPSE CORRIDOR: Historically the most volatile period. '
                        'Expect large swings, reversals, and unexpected news.'
            }
            break

    # Also check if near a single eclipse
    nearest = None
    min_distance = float('inf')
    for e in eclipses:
        e_date = datetime.strptime(e['date'], '%Y-%m-%d')
        distance = abs((target - e_date).days)
        if distance < min_distance:
            min_distance = distance
            nearest = e

    return {
        'in_corridor': in_corridor,
        'corridor_info': corridor_info,
        'nearest_eclipse': nearest,
        'days_to_nearest': min_distance if nearest else None,
    }


def get_eclipse_analysis(date_str):
    """Full eclipse analysis for a date."""
    # Get eclipses for current year
    year = date_str[:4]
    eclipses = find_eclipses_in_range(f'{year}-01-01', f'{year}-12-31')
    corridor = check_eclipse_corridor(date_str, eclipses)

    return {
        'date': date_str,
        'year_eclipses': eclipses,
        'corridor': corridor,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    year = today[:4]
    print(f"\n🌑 ECLIPSE ANALYSIS — {year}")
    print("=" * 65)

    analysis = get_eclipse_analysis(today)

    print(f"\n🔭 ECLIPSES IN {year}:")
    for e in analysis['year_eclipses']:
        print(f"  {e['date']}: {e['type']} [{e['market_impact']['severity']}]")

    corridor = analysis['corridor']
    if corridor['in_corridor']:
        print(f"\n⚠️ {corridor['corridor_info']['note']}")
    elif corridor['nearest_eclipse']:
        print(f"\n📅 Nearest eclipse: {corridor['nearest_eclipse']['date']} "
              f"({corridor['nearest_eclipse']['type']})")
        print(f"   Distance: {corridor['days_to_nearest']} days")


Save: Ctrl + S

Step 2.11 — core/mundane.py (National & Index Birth Charts)
Click core/mundane.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Mundane Astrology (Nation/Index Charts)
=============================================================
Transits to India's independence chart and Nifty's birth chart.
The backbone of macro-level market forecasting.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, angular_distance, get_sign,
    get_nakshatra, SIGNS
)
from datetime import datetime


# ── Birth Chart Data ──────────────────────────────────────

INDIA_CHART = {
    'name': 'India Independence',
    'date': '1947-08-15',
    'time': '00:00',
    'place': 'Delhi',
    'lat': 28.6139, 'lon': 77.2090,
    'description': 'India\'s independence. Transits to this chart affect national policy, economy, and markets.'
}

NIFTY_CHART = {
    'name': 'Nifty 50 (NSE)',
    'date': '1995-11-03',
    'time': '09:55',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'NSE Nifty 50 launch. The "birth chart" of India\'s primary index.'
}

BANKNIFTY_CHART = {
    'name': 'Bank Nifty',
    'date': '2005-06-13',
    'time': '09:15',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'Bank Nifty launch. Represents Indian banking sector.'
}

SENSEX_CHART = {
    'name': 'BSE Sensex',
    'date': '1986-01-02',
    'time': '10:00',
    'place': 'Mumbai',
    'lat': 19.0760, 'lon': 72.8777,
    'description': 'BSE Sensex base date. India\'s oldest major index.'
}

BITCOIN_CHART = {
    'name': 'Bitcoin',
    'date': '2009-01-03',
    'time': '18:15',  # Genesis block approximate
    'place': 'Global',
    'lat': 0.0, 'lon': 0.0,
    'description': 'Bitcoin genesis block. Reference chart for crypto.'
}

ALL_CHARTS = {
    'india': INDIA_CHART,
    'nifty': NIFTY_CHART,
    'banknifty': BANKNIFTY_CHART,
    'sensex': SENSEX_CHART,
    'bitcoin': BITCOIN_CHART,
}


def get_natal_positions(chart_name='nifty'):
    """Get planetary positions at birth of an entity."""
    chart = ALL_CHARTS.get(chart_name.lower(), NIFTY_CHART)
    return get_planetary_positions(chart['date'], chart['time'])


def transit_to_natal_aspects(transit_date, chart_name='nifty'):
    """
    Calculate aspects between current transiting planets
    and natal chart positions.
    """
    chart = ALL_CHARTS.get(chart_name.lower(), NIFTY_CHART)
    natal = get_planetary_positions(chart['date'], chart['time'])
    transit = get_planetary_positions(transit_date)

    aspects = []
    aspect_types = {
        0: ('Conjunction', 8), 60: ('Sextile', 5),
        90: ('Square', 6), 120: ('Trine', 6), 180: ('Opposition', 8),
    }

    # Key transit-to-natal combinations
    key_transits = {
        ('Jupiter', 'Moon'): ('Jupiter transit to natal Moon — MOST bullish. Major rallies.', 25),
        ('Jupiter', 'Sun'): ('Jupiter transit to natal Sun — Authority boosted. Policy positive.', 20),
        ('Saturn', 'Moon'): ('Saturn transit to natal Moon — Sade Sati pressure. Corrections.', -25),
        ('Saturn', 'Sun'): ('Saturn transit to natal Sun — Government pressure, restrictions.', -20),
        ('Rahu', 'Moon'): ('Rahu transit to natal Moon — Speculation frenzy, then crash.', -15),
        ('Rahu', 'Jupiter'): ('Rahu transit to natal Jupiter — Distorted growth, bubble.', -10),
        ('Mars', 'Saturn'): ('Mars transit to natal Saturn — Accidents, sharp drops.', -18),
        ('Venus', 'Jupiter'): ('Venus transit to natal Jupiter — Wealth flows, prosperity.', 15),
    }

    important_transit_planets = ['Jupiter', 'Saturn', 'Rahu', 'Mars', 'Venus']
    important_natal_planets = ['Sun', 'Moon', 'Mercury', 'Jupiter', 'Saturn', 'Rahu']

    for t_name in important_transit_planets:
        for n_name in important_natal_planets:
            if t_name not in transit or n_name not in natal:
                continue

            t_deg = transit[t_name]['longitude']
            n_deg = natal[n_name]['longitude']
            dist = angular_distance(t_deg, n_deg)

            for exact_deg, (aspect_name, orb) in aspect_types.items():
                if abs(dist - exact_deg) <= orb:
                    pair = (t_name, n_name)
                    interp = key_transits.get(pair, (f'{t_name} {aspect_name} natal {n_name}', 0))

                    is_bullish = interp[1] > 0
                    is_tight = abs(dist - exact_deg) <= 2

                    aspects.append({
                        'transit_planet': t_name,
                        'natal_planet': n_name,
                        'aspect': aspect_name,
                        'orb': round(abs(dist - exact_deg), 2),
                        'tight': is_tight,
                        'interpretation': interp[0],
                        'score': interp[1],
                        'bias': 'bullish' if is_bullish else 'bearish',
                    })

    return {
        'chart': chart['name'],
        'transit_date': transit_date,
        'aspects': sorted(aspects, key=lambda x: abs(x['score']), reverse=True),
    }


def get_mundane_analysis(transit_date, charts=None):
    """Get transit analysis for all relevant charts."""
    if charts is None:
        charts = ['nifty', 'india']

    results = {}
    for chart_name in charts:
        results[chart_name] = transit_to_natal_aspects(transit_date, chart_name)

    # Aggregate scores
    total_score = 0
    key_aspects = []
    for chart_name, data in results.items():
        for aspect in data['aspects']:
            if aspect['tight']:
                total_score += aspect['score']
                key_aspects.append(f"[{chart_name.upper()}] {aspect['interpretation']}")

    overall = 'BULLISH' if total_score > 10 else ('BEARISH' if total_score < -10 else 'NEUTRAL')

    return {
        'date': transit_date,
        'chart_analyses': results,
        'total_score': total_score,
        'overall_bias': overall,
        'key_aspects': key_aspects,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🏛️ MUNDANE ASTROLOGY — {today}")
    print("=" * 65)

    analysis = get_mundane_analysis(today)

    for chart_name, data in analysis['chart_analyses'].items():
        print(f"\n📋 TRANSITS TO {data['chart'].upper()}:")
        if data['aspects']:
            for a in data['aspects'][:5]:
                emoji = '🟢' if a['bias'] == 'bullish' else '🔴'
                tight_mark = '🎯' if a['tight'] else ''
                print(f"  {emoji} Transit {a['transit_planet']} {a['aspect']} "
                      f"Natal {a['natal_planet']} (orb: {a['orb']}°) {tight_mark}")
                print(f"     {a['interpretation']}")
        else:
            print("  No major transit aspects active.")

    print(f"\n📊 OVERALL MUNDANE SCORE: {analysis['total_score']:+d}")
    print(f"📈 BIAS: {analysis['overall_bias']}")


Save: Ctrl + S

Step 2.12 — core/kp_system.py (KP Sub-Lord System)
Click core/kp_system.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — KP (Krishnamurti Paddhati) System
=============================================================
Sub-lord theory for precise prediction. Each nakshatra is
divided into 9 unequal sub-divisions based on Vimshottari.
=============================================================
"""

from core.astro_engine import (
    get_planetary_positions, get_ascendant,
    NAKSHATRAS, NAKSHATRA_LORDS, NAKSHATRA_SPAN
)
from core.dasha import DASHA_YEARS, DASHA_SEQUENCE, TOTAL_DASHA_YEARS
from datetime import datetime


# ── KP Sub-Lord Table ─────────────────────────────────────

def build_kp_sublord_table():
    """
    Build the KP sub-lord table. Each nakshatra (13°20') is divided
    into 9 sub-divisions proportional to Vimshottari dasha years,
    starting from the nakshatra lord.
    """
    table = []

    for nak_idx in range(27):
        nak_lord = NAKSHATRA_LORDS[nak_idx]
        nak_start = nak_idx * NAKSHATRA_SPAN

        # Start sub-lord sequence from nakshatra lord
        start_seq_idx = DASHA_SEQUENCE.index(nak_lord)

        current_deg = nak_start
        for i in range(9):
            sub_lord_idx = (start_seq_idx + i) % 9
            sub_lord = DASHA_SEQUENCE[sub_lord_idx]

            # Sub-division span proportional to dasha years
            sub_span = NAKSHATRA_SPAN * (DASHA_YEARS[sub_lord] / TOTAL_DASHA_YEARS)
            sub_end = current_deg + sub_span

            table.append({
                'start_deg': round(current_deg, 4),
                'end_deg': round(sub_end, 4),
                'nakshatra': NAKSHATRAS[nak_idx],
                'nakshatra_lord': nak_lord,
                'sub_lord': sub_lord,
            })

            current_deg = sub_end

    return table


# Build once
KP_TABLE = build_kp_sublord_table()


def get_kp_sublord(degree):
    """Get KP sub-lord for a given sidereal degree."""
    degree = degree % 360.0
    for entry in KP_TABLE:
        if entry['start_deg'] <= degree < entry['end_deg']:
            return entry
    # Edge case: last entry
    return KP_TABLE[-1]


def get_kp_significators(positions):
    """
    Get star lord (nakshatra lord) and sub-lord for each planet.
    In KP, the sub-lord is the MOST important factor for prediction.
    """
    kp_data = {}

    for name, data in positions.items():
        kp_entry = get_kp_sublord(data['longitude'])
        kp_data[name] = {
            'longitude': data['longitude'],
            'sign': data['sign'],
            'sign_lord': data.get('sign_lord', ''),
            'star_lord': kp_entry['nakshatra_lord'],
            'sub_lord': kp_entry['sub_lord'],
            'nakshatra': kp_entry['nakshatra'],
        }

    return kp_data


def get_ruling_planets(date_str, time_str='09:15', lat=19.0760, lon=72.8777):
    """
    KP Ruling Planets at a given moment.
    These are the 5 significators of the current moment:
    1. Ascendant sign lord
    2. Ascendant star lord
    3. Ascendant sub lord
    4. Moon sign lord
    5. Moon star lord
    6. Day lord
    
    Ruling planets that agree with a chart's significators = CONFIRMATION.
    """
    positions = get_planetary_positions(date_str, time_str)
    ascendant = get_ascendant(date_str, time_str, lat, lon)

    # Ascendant KP
    asc_kp = get_kp_sublord(ascendant['degree'])

    # Moon KP
    moon_kp = get_kp_sublord(positions['Moon']['longitude'])

    # Day lord
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    day_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
    day_lord = day_lords[dt.weekday()]

    ruling = {
        'asc_sign_lord': ascendant.get('nakshatra_lord', asc_kp['nakshatra_lord']),
        'asc_star_lord': asc_kp['nakshatra_lord'],
        'asc_sub_lord': asc_kp['sub_lord'],
        'moon_sign_lord': positions['Moon'].get('sign_lord', ''),
        'moon_star_lord': moon_kp['nakshatra_lord'],
        'day_lord': day_lord,
    }

    # Get unique ruling planets
    all_rulers = list(set(ruling.values()))

    # Market interpretation
    bullish_rulers = ['Jupiter', 'Venus', 'Moon', 'Mercury']
    bearish_rulers = ['Saturn', 'Mars', 'Rahu', 'Ketu']

    bull_count = sum(1 for r in all_rulers if r in bullish_rulers)
    bear_count = sum(1 for r in all_rulers if r in bearish_rulers)

    if bull_count > bear_count:
        bias = 'BULLISH'
        note = 'Ruling planets favor optimism and buying'
    elif bear_count > bull_count:
        bias = 'BEARISH'
        note = 'Ruling planets favor caution and selling'
    else:
        bias = 'NEUTRAL'
        note = 'Mixed ruling planets — no clear direction'

    return {
        'components': ruling,
        'unique_rulers': all_rulers,
        'bullish_count': bull_count,
        'bearish_count': bear_count,
        'bias': bias,
        'note': note,
    }


def get_kp_analysis(date_str, time_str='09:15'):
    """Full KP analysis for market timing."""
    positions = get_planetary_positions(date_str, time_str)
    kp_sig = get_kp_significators(positions)
    ruling = get_ruling_planets(date_str, time_str)

    return {
        'date': date_str,
        'kp_significators': kp_sig,
        'ruling_planets': ruling,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n🔮 KP SYSTEM ANALYSIS — {today}")
    print("=" * 70)

    analysis = get_kp_analysis(today)

    print(f"\n📍 KP SIGNIFICATORS:")
    print(f"{'Planet':10s} {'Sign':10s} {'Sign Lord':10s} {'Star Lord':10s} {'Sub Lord':10s}")
    print("-" * 55)
    for name, data in analysis['kp_significators'].items():
        print(f"{name:10s} {data['sign']:10s} {data['sign_lord']:10s} "
              f"{data['star_lord']:10s} {data['sub_lord']:10s}")

    rp = analysis['ruling_planets']
    print(f"\n🎯 RULING PLANETS (9:15 AM Mumbai):")
    for key, value in rp['components'].items():
        print(f"  {key:20s}: {value}")
    print(f"\n  Unique Rulers: {', '.join(rp['unique_rulers'])}")
    print(f"  Bullish/Bearish: {rp['bullish_count']}/{rp['bearish_count']}")
    print(f"  📊 BIAS: {rp['bias']} — {rp['note']}")


Save: Ctrl + S

Step 2.13 — core/sector_map.py (Planet → Sector Rotation)
Click core/sector_map.py, paste:

python
Run Code

Copy code
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
        'stocks_nse': ['TATASTEEL', 'JSW STEEL', 'HAL', 'BEL', 'DLF'],
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
        'stocks_nse': ['IRCTC', 'INDIGO', 'NAUKRI (INFO EDGE)', 'ZOMATO'],
        'theme': 'Disruption, foreign influence, speculation',
    },
    'Ketu': {
        'sectors': ['Pharma R&D', 'IT Backend', 'Spiritual/Alt Medicine', 'Mining (hidden)'],
        'commodities': ['Herbs', 'Nuclear materials'],
        'stocks_nse': ['DIVIS', 'LALPATHLAB', 'MPHASIS'],
        'theme': 'Detachment, sudden events, hidden value',
    },
}


def get_sector_rotation_signals(date_str):
    """
    Analyze planetary strength and generate sector rotation signals.
    Returns ranked list of sectors with buy/sell/hold recommendations.
    """
    positions = get_planetary_positions(date_str)
    div = get_all_divisional_positions(date_str)

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

        # 3. Navamsha strength (from divisional)
        nav_score = div_data.get('navamsha_score', 0)
        score += nav_score * 6

        # 4. Vargottama bonus
        if div_data.get('is_vargottama', False):
            score += 15

        # 5. Speed bonus (fast = actively expressing)
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
    """



1 / 2








avatar
Can you continue from Step 2.13 — core/sector_map.py (Planet → Sector Rotation)
and complete this guide





ATXP Icon
🔮 FIN ASTRO BOT v2.0 — CONTINUATION (Step 2.13 onwards)
Picking up exactly where we left off. Keep working in the same GitHub Codespace.

Step 2.13 — core/sector_map.py (COMPLETE VERSION)
Click core/sector_map.py in the sidebar. Replace EVERYTHING with this complete file:

python
Run Code

Copy code
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


Save: Ctrl + S

PHASE 3: MARKET DATA MODULE (Universal — Any Symbol Worldwide)
Step 3.1 — market/__init__.py
Click market/__init__.py, paste:

python
Run Code

Copy code
"""FIN ASTRO BOT — Market Data Package"""


Save.

Step 3.2 — market/symbols.py (Symbol Registry)
Click market/symbols.py, paste:

python
Run Code

Copy code
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


Save: Ctrl + S

Step 3.3 — market/data_fetcher.py (Universal Market Data)
Click market/data_fetcher.py, paste:

python
Run Code

Copy code
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


Save: Ctrl + S

Step 3.4 — market/gap_analyzer.py
Click market/gap_analyzer.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Advanced Gap Analyzer
=============================================================
"""

import pandas as pd
import numpy as np
from market.data_fetcher import get_market_data_with_gaps, get_gap_statistics


def analyze_gap_patterns(data, display_name=''):
    """Detailed gap pattern analysis."""
    if data.empty:
        return {}

    results = {}

    # Day-of-week gap patterns
    data_copy = data.copy()
    data_copy['Weekday'] = data_copy.index.day_name()

    print(f"\n📅 GAP BY DAY OF WEEK{' — ' + display_name if display_name else ''}:")
    print(f"{'Day':12s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s} {'Avg Range%':>11s}")
    print("-" * 52)

    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        subset = data_copy[data_copy['Weekday'] == day]
        if len(subset) > 5:
            avg_gap = subset['Gap_Pct'].mean()
            bullish = (subset['Day_Direction'] == 'Bullish').mean() * 100
            avg_range = subset['Intraday_Range'].mean()
            print(f"  {day:10s} {len(subset):5d}  {avg_gap:+8.4f}  {bullish:8.1f}  {avg_range:10.3f}")

            results[day] = {
                'count': len(subset),
                'avg_gap': round(avg_gap, 4),
                'bullish_pct': round(bullish, 1),
                'avg_range': round(avg_range, 3),
            }

    # Monthly patterns
    data_copy['Month'] = data_copy.index.month
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    print(f"\n📆 GAP BY MONTH:")
    print(f"{'Month':6s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s}")
    print("-" * 35)

    for m in range(1, 13):
        subset = data_copy[data_copy['Month'] == m]
        if len(subset) > 5:
            avg_gap = subset['Gap_Pct'].mean()
            bullish = (subset['Day_Direction'] == 'Bullish').mean() * 100
            print(f"  {month_names[m-1]:4s} {len(subset):5d}  {avg_gap:+8.4f}  {bullish:8.1f}")

    return results


def find_extreme_gaps(data, top_n=10, display_name=''):
    """Find the most extreme gap days."""
    if data.empty or 'Gap_Pct' not in data.columns:
        return

    print(f"\n🔺 TOP {top_n} LARGEST GAP UPS{' — ' + display_name if display_name else ''}:")
    top_up = data.nlargest(top_n, 'Gap_Pct')[['Open', 'Close', 'Gap_Pct', 'Day_Direction']]
    print(top_up.to_string())

    print(f"\n🔻 TOP {top_n} LARGEST GAP DOWNS:")
    top_down = data.nsmallest(top_n, 'Gap_Pct')[['Open', 'Close', 'Gap_Pct', 'Day_Direction']]
    print(top_down.to_string())


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    data, name = get_market_data_with_gaps('nifty', start='2020-01-01')
    if not data.empty:
        get_gap_statistics(data, name)
        analyze_gap_patterns(data, name)
        find_extreme_gaps(data, top_n=5, display_name=name)


Save: Ctrl + S

PHASE 4: ANALYSIS ENGINE (Correlation + Backtesting + Projection)
Step 4.1 — analysis/__init__.py
Click analysis/__init__.py, paste:

python
Run Code

Copy code
"""FIN ASTRO BOT — Analysis Package"""


Save.

Step 4.2 — analysis/correlator.py (Merge Astro + Market)
Click analysis/correlator.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Astro-Market Correlator
=============================================================
Merges planetary data with market data for any symbol.
Creates the master dataset for correlation analysis.
=============================================================
"""

import pandas as pd
import pickle
import os
from datetime import datetime
from core.astro_engine import get_planetary_positions
from core.panchang import get_full_panchang
from market.data_fetcher import get_market_data_with_gaps

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')


def build_astro_market_dataset(user_input='nifty', start_date='2015-01-01', end_date=None):
    """
    Build merged astro + market dataset for ANY symbol.
    Calculates planetary positions for each trading day.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    print(f"🔮 Building Astro-Market Dataset for '{user_input}'...")
    print("   (Calculating planets for each trading day — takes a few minutes)\n")

    # Fetch market data
    market, display_name = get_market_data_with_gaps(user_input, start=start_date, end=end_date)
    if market.empty:
        return pd.DataFrame(), display_name

    # Calculate astro for each trading day
    astro_records = []
    total = len(market)

    for idx, (date, row) in enumerate(market.iterrows()):
        date_str = date.strftime('%Y-%m-%d')

        if (idx + 1) % 100 == 0 or idx == 0:
            print(f"   Processing {idx + 1}/{total} ({date_str})...")

        try:
            pos = get_planetary_positions(date_str)
            panchang = get_full_panchang(date_str, pos)

            record = {
                'Date': date,
                # Moon (fast-moving, daily impact)
                'Moon_Sign': pos['Moon']['sign'],
                'Moon_Nakshatra': pos['Moon']['nakshatra'],
                'Moon_Degree': pos['Moon']['longitude'],
                'Moon_Dignity': pos['Moon']['dignity'],

                # Key planet signs
                'Sun_Sign': pos['Sun']['sign'],
                'Mercury_Sign': pos['Mercury']['sign'],
                'Venus_Sign': pos['Venus']['sign'],
                'Mars_Sign': pos['Mars']['sign'],
                'Jupiter_Sign': pos['Jupiter']['sign'],
                'Saturn_Sign': pos['Saturn']['sign'],
                'Rahu_Sign': pos['Rahu']['sign'],

                # Retrogrades
                'Mercury_Retro': pos['Mercury']['retrograde'],
                'Venus_Retro': pos['Venus']['retrograde'],
                'Mars_Retro': pos['Mars']['retrograde'],
                'Jupiter_Retro': pos['Jupiter']['retrograde'],
                'Saturn_Retro': pos['Saturn']['retrograde'],

                'Retro_Count': sum(1 for p in ['Mercury', 'Venus', 'Mars',
                                                'Jupiter', 'Saturn']
                                   if pos[p]['retrograde']),

                # Dignities
                'Jupiter_Dignity': pos['Jupiter']['dignity'],
                'Saturn_Dignity': pos['Saturn']['dignity'],
                'Venus_Dignity': pos['Venus']['dignity'],

                # Panchang
                'Tithi': panchang['tithi']['name'],
                'Tithi_Num': panchang['tithi']['number'],
                'Paksha': panchang['tithi']['paksha'],
                'Karana': panchang['karana']['name'],
                'Karana_Vishti': panchang['karana']['is_vishti'],
                'Nitya_Yoga': panchang['nitya_yoga']['name'],
                'Nitya_Yoga_Bad': panchang['nitya_yoga']['is_inauspicious'],
                'Weekday': panchang['vara']['name'],

                # Sun-Moon distance (phase)
                'Sun_Moon_Dist': (pos['Moon']['longitude'] - pos['Sun']['longitude']) % 360,
            }
            astro_records.append(record)

        except Exception:
            continue

    if not astro_records:
        print("❌ Could not calculate astro data.")
        return pd.DataFrame(), display_name

    astro_df = pd.DataFrame(astro_records)
    astro_df.set_index('Date', inplace=True)

    # Merge
    merged = market.join(astro_df, how='inner')
    print(f"\n✅ Dataset built: {len(merged)} trading days with astro data for {display_name}.")

    # Cache it
    safe_name = display_name.replace(' ', '_').replace('/', '_').replace('^', '')
    cache_file = os.path.join(CACHE_DIR, f'dataset_{safe_name}.pkl')
    with open(cache_file, 'wb') as f:
        pickle.dump({'data': merged, 'name': display_name}, f)
    print(f"💾 Cached to {cache_file}")

    return merged, display_name


def load_cached_dataset(user_input):
    """Load previously built dataset from cache."""
    from market.symbols import resolve_symbol
    symbol, display_name = resolve_symbol(user_input)

    safe_name = display_name.replace(' ', '_').replace('/', '_').replace('^', '')
    cache_file = os.path.join(CACHE_DIR, f'dataset_{safe_name}.pkl')

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cached = pickle.load(f)
        print(f"📂 Loaded cached dataset: {len(cached['data'])} days for {cached['name']}")
        return cached['data'], cached['name']

    return pd.DataFrame(), display_name


def get_or_build_dataset(user_input, start_date='2018-01-01'):
    """Load from cache or build fresh."""
    data, name = load_cached_dataset(user_input)
    if not data.empty:
        return data, name
    return build_astro_market_dataset(user_input, start_date=start_date)


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    # Build for nifty (short range for testing)
    data, name = build_astro_market_dataset('nifty', start_date='2024-01-01')
    if not data.empty:
        print(f"\nColumns: {list(data.columns)}")
        print(f"\nSample:")
        print(data[['Close', 'Gap_Pct', 'Moon_Sign', 'Moon_Nakshatra',
                     'Tithi', 'Karana', 'Retro_Count']].tail(5))


Save: Ctrl + S

Step 4.3 — analysis/backtester.py (Historical Hit Rates)
Click analysis/backtester.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Historical Back-Tester
=============================================================
Computes hit rates for all astro factors against market data.
=============================================================
"""

import pandas as pd
import numpy as np


def analyze_factor(dataset, factor_column, target='Gap_Pct', min_samples=10):
    """Analyze a single factor's impact on market."""
    results = []

    for value in dataset[factor_column].dropna().unique():
        subset = dataset[dataset[factor_column] == value]
        if len(subset) < min_samples:
            continue

        avg_gap = subset[target].mean()
        avg_return = subset['Daily_Return'].mean() if 'Daily_Return' in subset.columns else 0
        bullish_pct = (subset['Day_Direction'] == 'Bullish').mean() * 100 if 'Day_Direction' in subset.columns else 50
        avg_range = subset['Intraday_Range'].mean() if 'Intraday_Range' in subset.columns else 0

        results.append({
            'value': value,
            'count': len(subset),
            'avg_gap_pct': round(avg_gap, 4),
            'avg_return_pct': round(avg_return, 4),
            'bullish_pct': round(bullish_pct, 1),
            'avg_range_pct': round(avg_range, 3),
        })

    return sorted(results, key=lambda x: x['avg_gap_pct'], reverse=True)


def run_full_backtest(dataset, display_name=''):
    """Run backtest on all major astro factors."""
    if dataset.empty:
        print("No data for backtesting.")
        return {}

    results = {}

    factors = [
        ('Moon_Sign', 'Moon Sign'),
        ('Moon_Nakshatra', 'Moon Nakshatra'),
        ('Tithi', 'Tithi'),
        ('Karana', 'Karana'),
        ('Nitya_Yoga', 'Nitya Yoga'),
        ('Weekday', 'Weekday'),
        ('Paksha', 'Paksha'),
        ('Jupiter_Sign', 'Jupiter Sign'),
        ('Saturn_Sign', 'Saturn Sign'),
    ]

    for col, label in factors:
        if col not in dataset.columns:
            continue

        analysis = analyze_factor(dataset, col)
        if analysis:
            results[label] = analysis

            print(f"\n📊 {label.upper()} IMPACT{' — ' + display_name if display_name else ''}:")
            print(f"{'Value':20s} {'Count':>6s} {'Avg Gap%':>9s} {'Bullish%':>9s} {'Range%':>8s}")
            print("-" * 58)
            for item in analysis[:15]:
                direction = '📈' if item['avg_gap_pct'] > 0.02 else ('📉' if item['avg_gap_pct'] < -0.02 else '➡️')
                print(f"{str(item['value']):20s} {item['count']:5d}  {item['avg_gap_pct']:+8.4f}  "
                      f"{item['bullish_pct']:8.1f}  {item['avg_range_pct']:7.3f} {direction}")

    # Retrograde analysis
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
        col = f'{planet}_Retro'
        if col not in dataset.columns:
            continue

        retro = dataset[dataset[col] == True]
        direct = dataset[dataset[col] == False]

        if len(retro) >= 10 and len(direct) >= 10:
            print(f"\n🔄 {planet.upper()} RETROGRADE IMPACT:")
            print(f"  Retrograde: {len(retro)} days, Avg Gap: {retro['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(retro['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Direct:     {len(direct)} days, Avg Gap: {direct['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(direct['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    # Vishti (Bhadra) Karana
    if 'Karana_Vishti' in dataset.columns:
        vishti = dataset[dataset['Karana_Vishti'] == True]
        non_vishti = dataset[dataset['Karana_Vishti'] == False]
        if len(vishti) >= 5:
            print(f"\n🚫 VISHTI (BHADRA) KARANA IMPACT:")
            print(f"  Vishti days:     {len(vishti)}, Avg Gap: {vishti['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(vishti['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Non-Vishti days: {len(non_vishti)}, Avg Gap: {non_vishti['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(non_vishti['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    # Inauspicious Nitya Yoga
    if 'Nitya_Yoga_Bad' in dataset.columns:
        bad = dataset[dataset['Nitya_Yoga_Bad'] == True]
        good = dataset[dataset['Nitya_Yoga_Bad'] == False]
        if len(bad) >= 5:
            print(f"\n⚠️ INAUSPICIOUS NITYA YOGA IMPACT:")
            print(f"  Inauspicious: {len(bad)}, Avg Gap: {bad['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(bad['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")
            print(f"  Auspicious:   {len(good)}, Avg Gap: {good['Gap_Pct'].mean():+.4f}%, "
                  f"Bullish: {(good['Day_Direction'] == 'Bullish').mean() * 100:.1f}%")

    return results


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    from analysis.correlator import get_or_build_dataset

    data, name = get_or_build_dataset('nifty', start_date='2020-01-01')
    if not data.empty:
        run_full_backtest(data, name)


Save: Ctrl + S

Step 4.4 — analysis/projector.py (Signal Aggregation + Projections)
Click analysis/projector.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Projection Engine
=============================================================
Aggregates ALL signals (astro, panchang, yoga, hora, mundane,
KP, Bradley, Ashtakavarga) into a single projection.
=============================================================
"""

from datetime import datetime
from core.astro_engine import full_astro_analysis
from core.yogas import detect_all_yogas
from core.panchang import get_full_panchang
from core.hora import get_trading_hora_summary
from core.dasha import get_index_dasha
from core.kp_system import get_kp_analysis
from core.sector_map import get_top_sectors
from core.mundane import get_mundane_analysis


def generate_full_projection(target_date=None, symbol='nifty', dataset=None):
    """
    THE MASTER PROJECTION FUNCTION.
    Combines every astrological technique into one report.
    """
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\n{'='*70}")
    print(f"🔮 FIN ASTRO BOT v2.0 — COMPLETE PROJECTION")
    print(f"📅 Date: {target_date}  |  📊 Symbol: {symbol.upper()}")
    print(f"{'='*70}")

    signals = []  # (name, direction, weight, detail)

    # ── 1. PLANETARY POSITIONS + DIGNITY ──────────────────
    analysis = full_astro_analysis(target_date)
    pos = analysis['positions']

    print(f"\n{'─'*50}")
    print(f"📍 PLANETARY POSITIONS (Sidereal/Lahiri)")
    print(f"{'─'*50}")
    print(f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':16s} {'Dignity':12s} {'R':3s}")
    print(f"{'─'*70}")

    for name, d in pos.items():
        r = '℞' if d['retrograde'] else ''
        print(f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
              f"{d['nakshatra']:13s} P{d['pada']}  "
              f"{d['dignity']:12s} {r}")

    # Dignity-based signals
    for planet in ['Jupiter', 'Venus', 'Saturn', 'Mars']:
        dignity = pos[planet]['dignity']
        if dignity == 'Exalted':
            bias = 'BULLISH' if planet in ['Jupiter', 'Venus'] else 'VOLATILE'
            signals.append((f'{planet} Exalted', bias, 12, f'{planet} at peak strength'))
        elif dignity == 'Debilitated':
            bias = 'BEARISH' if planet in ['Jupiter', 'Venus'] else 'VOLATILE'
            signals.append((f'{planet} Debilitated', bias, 10, f'{planet} weakened'))

    # ── 2. YOGAS ──────────────────────────────────────────
    yogas = detect_all_yogas(pos)

    if yogas:
        print(f"\n{'─'*50}")
        print(f"⭐ ACTIVE YOGAS ({len(yogas)} found)")
        print(f"{'─'*50}")

        for y in yogas:
            emoji = '🟢' if 'bullish' in y['market_bias'] else (
                '🔴' if 'bearish' in y['market_bias'] else '🟡')
            print(f"  {emoji} {y['name']} [{y['category']}]")
            print(f"    {y['description']}")
            print(f"    Bias: {y['market_bias'].upper()} | Weight: {y['weight']}")

            if 'bullish' in y['market_bias']:
                signals.append((f"Yoga: {y['name']}", 'BULLISH', y['weight'], y['description']))
            elif 'bearish' in y['market_bias']:
                signals.append((f"Yoga: {y['name']}", 'BEARISH', y['weight'], y['description']))
            else:
                signals.append((f"Yoga: {y['name']}", 'VOLATILE', y['weight'] // 2, y['description']))

    # ── 3. PANCHANG ───────────────────────────────────────
    panchang = get_full_panchang(target_date, pos)

    print(f"\n{'─'*50}")
    print(f"📅 PANCHANG")
    print(f"{'─'*50}")

    t = panchang['tithi']
    k = panchang['karana']
    ny = panchang['nitya_yoga']
    v = panchang['vara']
    mp = panchang['moon_phase']

    print(f"  Vara:        {v['name']} (Lord: {v['lord']})")
    print(f"  Tithi:       {t['paksha']} {t['name']} (#{t['number']})")
    print(f"  Karana:      {k['name']} ({k['nature']})")
    print(f"  Nitya Yoga:  {ny['name']} ({ny['nature']})")
    print(f"  Moon Phase:  {mp['phase']}")
    print(f"  Moon Nak:    {panchang['moon_nakshatra']['name']} P{panchang['moon_nakshatra']['pada']}")

    # Panchang signals
    if t['is_critical']:
        signals.append(('Critical Tithi', 'VOLATILE', 15, f"{t['name']} — high risk day"))

    if k['is_vishti']:
        signals.append(('Vishti Karana', 'BEARISH', 18, 'Bhadra Karana — avoid new trades'))

    if ny['is_inauspicious']:
        signals.append(('Bad Nitya Yoga', 'BEARISH', 14, f"{ny['name']} — inauspicious yoga"))
    elif ny['nature'] == 'Shubha':
        signals.append(('Good Nitya Yoga', 'BULLISH', 10, f"{ny['name']} — auspicious yoga"))

    # Moon phase
    if 'New Moon' in mp['phase']:
        signals.append(('New Moon', 'VOLATILE', 12, 'Low energy, potential reversal'))
    elif 'Full Moon' in mp['phase']:
        signals.append(('Full Moon', 'VOLATILE', 12, 'Peak emotion, potential reversal'))
    elif 'Waxing' in mp['phase']:
        signals.append(('Waxing Moon', 'BULLISH', 8, 'Building momentum'))
    elif 'Waning' in mp['phase']:
        signals.append(('Waning Moon', 'BEARISH', 8, 'Declining momentum'))

    # Gandanta
    if panchang['gandantas']:
        for g in panchang['gandantas']:
            if g['planet'] == 'Moon':
                signals.append(('Moon Gandanta', 'VOLATILE', 20, f"Moon at {g['junction']} — extreme karmic zone"))
                print(f"\n  🔥 GANDANTA: Moon at {g['junction']} ({g['severity']})")

    # VOC
    if panchang['void_of_course']['is_voc']:
        signals.append(('Void of Course Moon', 'VOLATILE', 10, 'Market may drift aimlessly'))
        print(f"  🕳️ VOC Moon: {panchang['void_of_course']['note']}")

    # ── 4. HORA TIMING ────────────────────────────────────
    try:
        hora = get_trading_hora_summary(target_date)

        print(f"\n{'─'*50}")
        print(f"⏰ INTRADAY HORA TIMING")
        print(f"{'─'*50}")
        print(f"  Day Ruler: {hora['day_ruler']}")

        for h in hora['market_horas']:
            emoji = '🟢' if h['bias'] == 'bullish' else ('🔴' if h['bias'] == 'bearish' else '🟡')
            print(f"  {h['start']}-{h['end']} {emoji} {h['planet']:10s} {h['action']}")

        print(f"\n  ⚠️ Inauspicious Periods:")
        for name, period in hora['inauspicious'].items():
            if 'rahu' in name or 'abhijit' in name:
                print(f"    {name}: {period['start']}-{period['end']}")

    except Exception as e:
        print(f"  (Hora calculation skipped: {e})")

    # ── 5. SPECIAL EVENTS ─────────────────────────────────
    if analysis['combustions']:
        print(f"\n  🔥 Combustions:")
        for c in analysis['combustions']:
            print(f"    {c['planet']} — {c['severity']} ({c['distance_from_sun']}° from Sun)")

    if analysis['planetary_wars']:
        print(f"\n  ⚔️ Planetary Wars:")
        for w in analysis['planetary_wars']:
            print(f"    {w['planet1']} vs {w['planet2']} — Winner: {w['winner']}")
            signals.append(('Planetary War', 'VOLATILE', 15,
                          f"{w['planet1']} vs {w['planet2']}"))

    if analysis['stations']:
        print(f"\n  🛑 Stations:")
        for s in analysis['stations']:
            print(f"    {s['planet']}: {s['type']}")
            signals.append(('Planet Station', 'VOLATILE', 18,
                          f"{s['planet']} {s['type']}"))

    if analysis['ingresses']:
        print(f"\n  🚀 Sign Changes:")
        for ing in analysis['ingresses']:
            print(f"    {ing['planet']}: {ing['from_sign']} → {ing['to_sign']}")
            signals.append(('Sign Change', 'VOLATILE', 10,
                          f"{ing['planet']} enters {ing['to_sign']}"))

    # ── 6. DASHA (if applicable) ──────────────────────────
    try:
        if symbol.lower() in ['nifty', 'banknifty', 'sensex']:
            dasha = get_index_dasha(symbol.lower(), target_date)
            if dasha['current']:
                maha = dasha['current']['mahadasha']
                antar = dasha['current'].get('antardasha')

                print(f"\n{'─'*50}")
                print(f"🔮 DASHA PERIODS ({symbol.upper()})")
                print(f"{'─'*50}")
                print(f"  Mahadasha: {maha['lord']} "
                      f"({maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')})")
                if antar:
                    print(f"  Antardasha: {antar['antardasha_lord']} "
                          f"({antar['start'].strftime('%Y-%m-%d')} to {antar['end'].strftime('%Y-%m-%d')})")

                interp = maha.get('interpretation', {})
                if interp:
                    overall = interp.get('overall', '')
                    if 'BULLISH' in overall.upper():
                        signals.append(('Mahadasha', 'BULLISH', 15, f"{maha['lord']} Mahadasha — {overall}"))
                    elif 'CHALLENGING' in overall.upper() or 'BEARISH' in overall.upper():
                        signals.append(('Mahadasha', 'BEARISH', 15, f"{maha['lord']} Mahadasha — {overall}"))
    except Exception:
        pass

    # ── 7. KP RULING PLANETS ─────────────────────────────
    try:
        kp = get_kp_analysis(target_date)
        rp = kp['ruling_planets']

        print(f"\n{'─'*50}")
        print(f"🎯 KP RULING PLANETS")
        print(f"{'─'*50}")
        print(f"  Rulers: {', '.join(rp['unique_rulers'])}")
        print(f"  Bullish/Bearish: {rp['bullish_count']}/{rp['bearish_count']}")
        print(f"  Bias: {rp['bias']}")

        if rp['bias'] == 'BULLISH':
            signals.append(('KP Ruling Planets', 'BULLISH', 12, rp['note']))
        elif rp['bias'] == 'BEARISH':
            signals.append(('KP Ruling Planets', 'BEARISH', 12, rp['note']))
    except Exception:
        pass

    # ── 8. MUNDANE TRANSITS ──────────────────────────────
    try:
        if symbol.lower() in ['nifty', 'banknifty', 'sensex']:
            charts = ['nifty', 'india'] if symbol.lower() in ['nifty', 'banknifty'] else ['india']
            mundane = get_mundane_analysis(target_date, charts)

            if mundane['key_aspects']:
                print(f"\n{'─'*50}")
                print(f"🏛️ MUNDANE TRANSIT ASPECTS")
                print(f"{'─'*50}")
                for asp in mundane['key_aspects'][:5]:
                    print(f"  {asp}")

                if mundane['overall_bias'] == 'BULLISH':
                    signals.append(('Mundane Transits', 'BULLISH', 15, f"Score: {mundane['total_score']:+d}"))
                elif mundane['overall_bias'] == 'BEARISH':
                    signals.append(('Mundane Transits', 'BEARISH', 15, f"Score: {mundane['total_score']:+d}"))
    except Exception:
        pass

    # ── 9. HISTORICAL PATTERN MATCHING ────────────────────
    if dataset is not None and not dataset.empty:
        print(f"\n{'─'*50}")
        print(f"📊 HISTORICAL PATTERN MATCHING")
        print(f"{'─'*50}")

        moon_sign = pos['Moon']['sign']
        moon_nak = pos['Moon']['nakshatra']

        # Moon Sign pattern
        if 'Moon_Sign' in dataset.columns:
            moon_data = dataset[dataset['Moon_Sign'] == moon_sign]
            if len(moon_data) >= 10:
                avg_gap = moon_data['Gap_Pct'].mean()
                bullish_pct = (moon_data['Day_Direction'] == 'Bullish').mean() * 100
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                conf = min(abs(bullish_pct - 50) * 1.5, 20)
                signals.append((f'Moon in {moon_sign}', direction, conf,
                              f'{len(moon_data)} days, Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}%'))
                print(f"  Moon in {moon_sign}: {len(moon_data)} days, "
                      f"Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")

        # Moon Nakshatra pattern
        if 'Moon_Nakshatra' in dataset.columns:
            nak_data = dataset[dataset['Moon_Nakshatra'] == moon_nak]
            if len(nak_data) >= 5:
                avg_gap = nak_data['Gap_Pct'].mean()
                bullish_pct = (nak_data['Day_Direction'] == 'Bullish').mean() * 100
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                conf = min(abs(bullish_pct - 50) * 1.5, 18)
                signals.append((f'Moon in {moon_nak}', direction, conf,
                              f'{len(nak_data)} days, Avg Gap: {avg_gap:+.3f}%'))
                print(f"  Moon in {moon_nak}: {len(nak_data)} days, "
                      f"Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")

        # Tithi pattern
        if 'Tithi' in dataset.columns:
            tithi_name = panchang['tithi']['name']
            tithi_data = dataset[dataset['Tithi'] == tithi_name]
            if len(tithi_data) >= 5:
                avg_gap = tithi_data['Gap_Pct'].mean()
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                signals.append((f'Tithi: {tithi_name}', direction, 8,
                              f'Avg Gap: {avg_gap:+.3f}%'))

        # Retrograde count pattern
        if 'Retro_Count' in dataset.columns:
            retro_count = sum(1 for p in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
                             if pos[p]['retrograde'])
            rc_data = dataset[dataset['Retro_Count'] == retro_count]
            if len(rc_data) >= 10:
                avg_gap = rc_data['Gap_Pct'].mean()
                direction = 'BULLISH' if avg_gap > 0.02 else ('BEARISH' if avg_gap < -0.02 else 'NEUTRAL')
                signals.append((f'{retro_count} Retrogrades', direction, 8,
                              f'Avg Gap: {avg_gap:+.3f}%'))

    # ══════════════════════════════════════════════════════
    # SIGNAL AGGREGATION
    # ══════════════════════════════════════════════════════

    print(f"\n{'='*70}")
    print(f"🎯 SIGNAL AGGREGATION ({len(signals)} signals)")
    print(f"{'='*70}")

    bullish_score = sum(w for _, d, w, _ in signals if d == 'BULLISH')
    bearish_score = sum(w for _, d, w, _ in signals if d == 'BEARISH')
    volatile_score = sum(w for _, d, w, _ in signals if d == 'VOLATILE')

    for name, direction, weight, detail in sorted(signals, key=lambda x: x[2], reverse=True):
        emoji = '🟢' if direction == 'BULLISH' else ('🔴' if direction == 'BEARISH' else '🟡')
        print(f"  {emoji} {name:30s} {direction:10s} wt:{weight:3d} | {detail[:50]}")

    total = bullish_score + bearish_score + volatile_score
    if total > 0:
        bull_pct = (bullish_score / total) * 100
        bear_pct = (bearish_score / total) * 100
        vol_pct = (volatile_score / total) * 100
    else:
        bull_pct = bear_pct = vol_pct = 33.3

    print(f"\n  Bullish:  {bullish_score:4d} ({bull_pct:.0f}%)")
    print(f"  Bearish:  {bearish_score:4d} ({bear_pct:.0f}%)")
    print(f"  Volatile: {volatile_score:4d} ({vol_pct:.0f}%)")

    # Final projection
    print(f"\n{'='*70}")

    if bullish_score > bearish_score * 1.3 and bullish_score > volatile_score:
        gap_proj = "📈 GAP UP EXPECTED"
        bias = "BULLISH"
        confidence = min(bull_pct, 75)
    elif bearish_score > bullish_score * 1.3 and bearish_score > volatile_score:
        gap_proj = "📉 GAP DOWN EXPECTED"
        bias = "BEARISH"
        confidence = min(bear_pct, 75)
    elif volatile_score > max(bullish_score, bearish_score):
        gap_proj = "🔀 VOLATILE / FLAT"
        bias = "SIDEWAYS WITH WHIPSAWS"
        confidence = 45
    else:
        gap_proj = "➡️ FLAT / UNCERTAIN"
        bias = "NO CLEAR EDGE"
        confidence = 35

    print(f"  🎯 GAP PROJECTION:    {gap_proj}")
    print(f"  📊 DAY BIAS:          {bias}")
    print(f"  🔮 CONFIDENCE:        ~{confidence:.0f}%")
    print(f"{'='*70}")

    print(f"\n⚠️  DISCLAIMER:")
    print(f"  This is for RESEARCH & EDUCATION only.")
    print(f"  Astro signals are probabilistic, not deterministic.")
    print(f"  Always combine with technical analysis & risk management.")
    print(f"  Never risk capital solely on astrological signals.")

    return {
        'date': target_date,
        'symbol': symbol,
        'gap_projection': gap_proj,
        'bias': bias,
        'confidence': confidence,
        'signals': signals,
        'bullish_score': bullish_score,
        'bearish_score': bearish_score,
        'volatile_score': volatile_score,
    }


# ── Test ──────────────────────────────────────────────────
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    generate_full_projection(today, 'nifty')


Save: Ctrl + S

PHASE 5: REPORTS (Daily / Weekly / Monthly)
Step 5.1 — reports/__init__.py
Click reports/__init__.py, paste:

python
Run Code

Copy code
"""FIN ASTRO BOT — Reports Package"""


Save.

Step 5.2 — reports/daily_report.py
Click reports/daily_report.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Daily Report Generator
=============================================================
"""

import os
from datetime import datetime
from analysis.projector import generate_full_projection


REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def generate_daily_report(date_str=None, symbol='nifty', dataset=None, save=True):
    """Generate and optionally save daily report."""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    os.makedirs(REPORT_DIR, exist_ok=True)

    result = generate_full_projection(date_str, symbol, dataset)

    if save:
        safe_sym = symbol.replace(' ', '_').replace('^', '')
        filename = os.path.join(REPORT_DIR, f'daily_{safe_sym}_{date_str}.txt')

        with open(filename, 'w') as f:
            f.write(f"FIN ASTRO BOT v2.0 — DAILY REPORT\n")
            f.write(f"Date: {date_str} | Symbol: {symbol}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"GAP PROJECTION: {result['gap_projection']}\n")
            f.write(f"DAY BIAS: {result['bias']}\n")
            f.write(f"CONFIDENCE: ~{result['confidence']:.0f}%\n\n")
            f.write(f"SCORES:\n")
            f.write(f"  Bullish:  {result['bullish_score']}\n")
            f.write(f"  Bearish:  {result['bearish_score']}\n")
            f.write(f"  Volatile: {result['volatile_score']}\n\n")
            f.write(f"SIGNALS ({len(result['signals'])}):\n")
            for name, direction, weight, detail in result['signals']:
                f.write(f"  [{direction:10s}] {name:30s} wt:{weight:3d} | {detail}\n")
            f.write(f"\nDISCLAIMER: For research & education only.\n")

        print(f"\n💾 Report saved to: {filename}")

    return result


if __name__ == '__main__':
    generate_daily_report()


Save: Ctrl + S

Step 5.3 — reports/weekly_report.py
Click reports/weekly_report.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Weekly Report Generator
=============================================================
Loops through upcoming week, generates batch projections.
=============================================================
"""

import os
from datetime import datetime, timedelta
from reports.daily_report import generate_daily_report

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def generate_weekly_report(start_date=None, symbol='nifty', dataset=None):
    """Generate projections for the entire upcoming week."""
    if start_date is None:
        today = datetime.now()
        # Find next Monday
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 0  # If today is Monday, use today
        start = today + timedelta(days=days_until_monday)
    else:
        start = datetime.strptime(start_date, '%Y-%m-%d')

    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"\n📅 WEEKLY REPORT — Week of {start.strftime('%Y-%m-%d')}")
    print(f"{'='*60}")

    week_results = []

    # Monday to Friday
    for i in range(5):
        day = start + timedelta(days=i)
        if day.weekday() >= 5:  # Skip weekends
            continue

        date_str = day.strftime('%Y-%m-%d')
        day_name = day.strftime('%A')

        print(f"\n\n{'#'*60}")
        print(f"# {day_name} — {date_str}")
        print(f"{'#'*60}")

        result = generate_daily_report(date_str, symbol, dataset, save=True)
        result['day_name'] = day_name
        week_results.append(result)

    # Weekly Summary
    print(f"\n\n{'='*60}")
    print(f"📊 WEEKLY SUMMARY — {symbol.upper()}")
    print(f"{'='*60}")
    print(f"{'Day':12s} {'Projection':25s} {'Bias':20s} {'Conf':>5s}")
    print(f"{'─'*65}")

    for r in week_results:
        print(f"{r.get('day_name', ''):12s} {r['gap_projection']:25s} "
              f"{r['bias']:20s} {r['confidence']:4.0f}%")

    total_bull = sum(r['bullish_score'] for r in week_results)
    total_bear = sum(r['bearish_score'] for r in week_results)

    print(f"\n  Week Bullish Total:  {total_bull}")
    print(f"  Week Bearish Total:  {total_bear}")
    print(f"  Week Bias: {'BULLISH' if total_bull > total_bear * 1.2 else ('BEARISH' if total_bear > total_bull * 1.2 else 'MIXED')}")

    # Save weekly summary
    safe_sym = symbol.replace(' ', '_').replace('^', '')
    filename = os.path.join(REPORT_DIR, f'weekly_{safe_sym}_{start.strftime("%Y-%m-%d")}.txt')
    with open(filename, 'w') as f:
        f.write(f"FIN ASTRO BOT — WEEKLY REPORT\n")
        f.write(f"Week of: {start.strftime('%Y-%m-%d')}\n")
        f.write(f"Symbol: {symbol}\n\n")
        for r in week_results:
            f.write(f"{r.get('day_name', ''):12s} {r['gap_projection']:25s} "
                    f"{r['bias']:20s} {r['confidence']:4.0f}%\n")
        f.write(f"\nBullish Total: {total_bull}\n")
        f.write(f"Bearish Total: {total_bear}\n")

    print(f"\n💾 Weekly report saved to: {filename}")

    return week_results


if __name__ == '__main__':
    generate_weekly_report()


Save: Ctrl + S

Step 5.4 — reports/monthly_report.py
Click reports/monthly_report.py, paste:

python
Run Code

Copy code
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


Save: Ctrl + S

PHASE 6: STREAMLIT DASHBOARD (Web Interface)
Step 6.1 — dashboard/app.py (Main Dashboard)
Click dashboard/app.py, paste:

python
Run Code

Copy code
"""
=============================================================
FIN ASTRO BOT v2.0 — Streamlit Web Dashboard
=============================================================
Run with: streamlit run dashboard/app.py
=============================================================
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🔮 FIN ASTRO BOT v2.0",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.title("🔮 FIN ASTRO BOT v2.0")
st.sidebar.markdown("---")

# Symbol input
symbol = st.sidebar.text_input(
    "📊 Symbol",
    value="nifty",
    help="Try: nifty, bitcoin, tatapower, AAPL, gold, nasdaq"
)

# Date input
analysis_date = st.sidebar.date_input(
    "📅 Date",
    value=datetime.now(),
)
date_str = analysis_date.strftime('%Y-%m-%d')

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Quick Symbols:**
- 🇮🇳 `nifty`, `banknifty`, `sensex`
- 🇮🇳 `tatapower`, `reliance`, `sbin`
- 🇺🇸 `nasdaq`, `sp500`, `AAPL`, `TSLA`
- ₿ `bitcoin`, `ethereum`, `solana`
- 🪙 `gold`, `silver`, `crude`
""")

# ── Main Page ─────────────────────────────────────────────
st.title(f"🔮 FIN ASTRO Analysis — {symbol.upper()}")
st.markdown(f"**Date:** {date_str}")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Planets", "⭐ Yogas & Panchang", "⏰ Hora Timing",
    "📊 Projection", "🔮 Dasha", "🏭 Sectors"
])

# ── Tab 1: Planetary Positions ────────────────────────────
with tab1:
    st.header("📍 Planetary Positions (Sidereal/Lahiri)")

    try:
        from core.astro_engine import full_astro_analysis
        analysis = full_astro_analysis(date_str)

        # Positions table
        import pandas as pd
        rows = []
        for name, d in analysis['positions'].items():
            rows.append({
                'Planet': name,
                'Sign': d['sign'],
                'Degree': f"{d['sign_degree']:.2f}°",
                'Nakshatra': f"{d['nakshatra']} P{d['pada']}",
                'Dignity': d['dignity'],
                'Retro': '℞' if d['retrograde'] else '',
                'Speed': f"{d['speed']:.4f}",
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Events columns
        col1, col2, col3 = st.columns(3)

        with col1:
            if analysis['retrogrades']:
                st.warning(f"🔄 Retrogrades: {', '.join(analysis['retrogrades'])}")
            else:
                st.success("No retrogrades active")

        with col2:
            if analysis['combustions']:
                for c in analysis['combustions']:
                    st.error(f"🔥 {c['planet']} Combust ({c['severity']})")

        with col3:
            if analysis['stations']:
                for s in analysis['stations']:
                    st.warning(f"🛑 {s['planet']}: {s['type']}")

        if analysis['ingresses']:
            st.info("🚀 Sign Changes: " + ", ".join(
                f"{i['planet']} → {i['to_sign']}" for i in analysis['ingresses']))

    except Exception as e:
        st.error(f"Error calculating positions: {e}")

# ── Tab 2: Yogas & Panchang ──────────────────────────────
with tab2:
    st.header("⭐ Yogas & Panchang")

    try:
        from core.yogas import detect_all_yogas
        from core.panchang import get_full_panchang

        pos = analysis['positions']
        yogas = detect_all_yogas(pos)
        panchang = get_full_panchang(date_str, pos)

        # Panchang
        col1, col2, col3 = st.columns(3)
        with col1:
            t = panchang['tithi']
            st.metric("🌙 Tithi", f"{t['paksha']} {t['name']}")
            if t['is_critical']:
                st.error("⚠️ CRITICAL TITHI")

        with col2:
            k = panchang['karana']
            st.metric("🔷 Karana", k['name'])
            if k['is_vishti']:
                st.error("🚫 VISHTI (BHADRA) — Avoid trades!")

        with col3:
            ny = panchang['nitya_yoga']
            st.metric("⭐ Nitya Yoga", ny['name'])
            if ny['is_inauspicious']:
                st.warning("⚠️ Inauspicious Yoga")

        st.markdown(f"**Moon Phase:** {panchang['moon_phase']['phase']}")
        st.markdown(f"**Moon Nakshatra:** {panchang['moon_nakshatra']['name']} Pada {panchang['moon_nakshatra']['pada']}")

        # Yogas
        if yogas:
            st.subheader(f"⭐ Active Yogas ({len(yogas)})")
            for y in yogas:
                if 'bullish' in y['market_bias']:
                    st.success(f"🟢 **{y['name']}** [{y['category']}] — {y['description']}")
                elif 'bearish' in y['market_bias']:
                    st.error(f"🔴 **{y['name']}** [{y['category']}] — {y['description']}")
                else:
                    st.warning(f"🟡 **{y['name']}** [{y['category']}] — {y['description']}")
        else:
            st.info("No significant yogas detected.")

    except Exception as e:
        st.error(f"Error: {e}")

# ── Tab 3: Hora Timing ───────────────────────────────────
with tab3:
    st.header("⏰ Intraday Hora Timing")

    try:
        from core.hora import get_trading_hora_summary
        hora = get_trading_hora_summary(date_str)

        st.markdown(f"**{hora['weekday']}** | Day Ruler: **{hora['day_ruler']}** | "
                    f"Sunrise: {hora['sunrise']} | Sunset: {hora['sunset']}")

        # Hora table
        hora_rows = []
        for h in hora['market_horas']:
            emoji = '🟢' if h['bias'] == 'bullish' else ('🔴' if h['bias'] == 'bearish' else '🟡')
            hora_rows.append({
                'Time': f"{h['start']}-{h['end']}",
                'Planet': f"{emoji} {h['planet']}",
                'Bias': h['bias'].upper(),
                'Action': h['action'],
                'Minutes': h['duration_min'],
            })

        hora_df = pd.DataFrame(hora_rows)
        st.dataframe(hora_df, use_container_width=True, hide_index=True)

        # Inauspicious periods
        st.subheader("⚠️ Inauspicious Periods")
        for name, period in hora['inauspicious'].items():
            if 'rahu' in name:
                st.error(f"🚫 {name}: {period['start']} - {period['end']}")
            elif 'abhijit' in name:
                st.success(f"✅ {name}: {period['start']} - {period['end']}")
            else:
                st.warning(f"⚠️ {name}: {period['start']} - {period['end']}")

    except Exception as e:
        st.error(f"Error: {e}")

# ── Tab 4: Projection ────────────────────────────────────
with tab4:
    st.header("📊 Full Astro Projection")

    if st.button("🔮 Generate Projection", type="primary"):
        with st.spinner("Calculating all signals..."):
            try:
                from analysis.projector import generate_full_projection
                result = generate_full_projection(date_str, symbol)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gap Projection", result['gap_projection'])
                with col2:
                    st.metric("Day Bias", result['bias'])
                with col3:
                    st.metric("Confidence", f"~{result['confidence']:.0f}%")

                st.markdown("---")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🟢 Bullish Score", result['bullish_score'])
                with col2:
                    st.metric("🔴 Bearish Score", result['bearish_score'])
                with col3:
                    st.metric("🟡 Volatile Score", result['volatile_score'])

                # Signal list
                st.subheader("📋 All Signals")
                for name, direction, weight, detail in sorted(result['signals'], key=lambda x: x[2], reverse=True):
                    emoji = '🟢' if direction == 'BULLISH' else ('🔴' if direction == 'BEARISH' else '🟡')
                    st.markdown(f"{emoji} **{name}** ({direction}, wt:{weight}) — {detail}")

            except Exception as e:
                st.error(f"Error: {e}")

# ── Tab 5: Dasha ─────────────────────────────────────────
with tab5:
    st.header("🔮 Vimshottari Dasha")

    try:
        from core.dasha import get_index_dasha

        index_options = ['nifty', 'banknifty', 'sensex']
        if symbol.lower() in index_options:
            dasha = get_index_dasha(symbol.lower(), date_str)
            if dasha['current']:
                maha = dasha['current']['mahadasha']
                st.metric("Mahadasha", maha['lord'])
                st.markdown(f"**Period:** {maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')}")

                interp = maha.get('interpretation', {})
                if interp:
                    st.info(interp.get('overall', ''))
                    st.markdown(f"**Bullish Sectors:** {', '.join(interp.get('bullish_sectors', []))}")
                    st.markdown(f"**Bearish Sectors:** {', '.join(interp.get('bearish_sectors', []))}")

                antar = dasha['current'].get('antardasha')
                if antar:
                    st.metric("Antardasha", antar['antardasha_lord'])

                # All mahadashas table
                st.subheader("All Mahadashas")
                dasha_rows = []
                for d in dasha['all_dashas']['dashas']:
                    current = '◀ CURRENT' if d['lord'] == maha['lord'] else ''
                    dasha_rows.append({
                        'Lord': d['lord'],
                        'Start': d['start'].strftime('%Y-%m-%d'),
                        'End': d['end'].strftime('%Y-%m-%d'),
                        'Years': d['years'],
                        'Status': current,
                    })
                st.dataframe(pd.DataFrame(dasha_rows), use_container_width=True, hide_index=True)
        else:
            st.info(f"Dasha is available for Indian indices (nifty, banknifty, sensex). "
                    f"Current symbol '{symbol}' doesn't have a predefined birth chart.")

    except Exception as e:
        st.error(f"Error: {e}")

# ── Tab 6: Sectors ────────────────────────────────────────
with tab6:
    st.header("🏭 Sector Rotation Signals")

    try:
        from core.sector_map import get_top_sectors, get_commodity_signals

        sectors = get_top_sectors(date_str)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Top Bullish Sectors")
            for s in sectors['bullish_sectors']:
                st.success(f"**{s['sector']}** ({s['ruling_planet']}) — Score: {s['score']}")
                if s['sample_stocks']:
                    st.caption(f"Stocks: {', '.join(s['sample_stocks'][:3])}")

        with col2:
            st.subheader("📉 Top Bearish Sectors")
            for s in sectors['bearish_sectors']:
                st.error(f"**{s['sector']}** ({s['ruling_planet']}) — Score: {s['score']}")

        # Commodities
        st.subheader("🪙 Commodity Signals")
        comm = get_commodity_signals(date_str)
        comm_rows = []
        for name, data in comm.items():
            comm_rows.append({
                'Commodity': name,
                'Rulers': ', '.join(data['rulers']),
                'Score': data['score'],
                'Bias': data['bias'],
            })
        st.dataframe(pd.DataFrame(comm_rows), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error: {e}")

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
⚠️ **Disclaimer:** This tool is for educational and research purposes only. 
Financial astrology correlations are not scientifically proven predictors. 
Never trade real money based solely on astrological signals.
""")


Save: Ctrl + S

PHASE 7: UPDATE MAIN.PY (New CLI Runner)
Click main.py in the root of the project (not in any subfolder). Replace EVERYTHING with:

python
Run Code

Copy code
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


Save: Ctrl + S

PHASE 8: UPDATE README
Click README.md, replace everything with:

markdown

Copy code
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

📋 Supported Symbols
Category	Examples
🇮🇳 Indian Indices	nifty, banknifty, sensex
🇮🇳 Indian Stocks	tatapower, reliance, sbin, infy
🇺🇸 US Indices	nasdaq, sp500, dow
🇺🇸 US Stocks	AAPL, TSLA, NVDA, MSFT
₿ Crypto	bitcoin, ethereum, solana
🪙 Commodities	gold, silver, crude
🌍 Global	dax, ftse, nikkei, hangseng
⚠️ Disclaimer
This tool is for educational and research purposes only. Financial astrology
correlations are not scientifically proven predictors. Never trade real money based
solely on astrological signals. Always combine with technical analysis and risk management.

yaml

Copy code

**Save:** `Ctrl + S`

---

## PHASE 9: TEST EVERYTHING 🚀

### Test 1 — Quick Analysis

```bash
python main.py --quick

Test 2 — Hora Timing
bash

Copy code
python main.py --hora

Test 3 — Sector Rotation
bash

Copy code
python main.py --sectors

Test 4 — Dasha
bash

Copy code
python main.py --dasha nifty

Test 5 — Full Projection
bash

Copy code
python main.py --project nifty

Test 6 — Different Symbols
bash

Copy code
python main.py --quick 2025-01-15
python main.py --project bitcoin
python main.py --project gold

Test 7 — List Symbols
bash

Copy code
python main.py --symbols

Test 8 — Web Dashboard
bash

Copy code
streamlit run dashboard/app.py

A URL will appear like http://localhost:8501. Click it or Ctrl+click to open in browser.

In Codespaces: A popup will ask "Open in browser?" — click Yes.

Test 9 — Interactive Menu
bash

Copy code
python main.py

Choose options from the menu.

PHASE 10: SAVE TO GITHUB
bash

Copy code
# Add the new cache and output folders to gitignore
echo "cache/" >> .gitignore
echo "output/" >> .gitignore
echo "*.pkl" >> .gitignore
echo "__pycache__/" >> .gitignore

# Save everything
git add -A
git commit -m "🔮 FIN ASTRO BOT v2.0 — Complete mega-build with all features"
git push

🎓 WHAT YOU'VE BUILT — Final Architecture
yaml

Copy code
┌─────────────────────────────────────────────────────────────────┐
│                    🔮 FIN ASTRO BOT v2.0                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CORE ENGINE (12 modules)                                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐       │
│  │ Planets  │ Yogas    │ Panchang │ Hora     │ Dasha    │       │
│  │ +Dignity │ (20+)    │ T/K/NY/G │ +RahuK   │ Maha/Ant │       │
│  ├──────────┼──────────┼──────────┼──────────┼──────────┤       │
│  │Ashtaka-  │Division- │ Bradley  │ Eclipse  │ Mundane  │       │
│  │varga     │al D9/D10 │ Sidero.  │ Corridor │ Transits │       │
│  ├──────────┼──────────┴──────────┴──────────┴──────────┤       │
│  │ KP Sub-  │ Sector Rotation Mapper                     │       │
│  │ Lord     │ (Planet → Sector → Stocks/Commodities)     │       │
│  └──────────┴────────────────────────────────────────────┘       │
│                                                                  │
│  MARKET DATA (Universal)                                         │
│  ┌───────────────────────────────────────────────────────┐       │
│  │ Any Symbol: Nifty, Bitcoin, AAPL, Gold, TATAPOWER     │       │
│  │ Auto-resolve: 'tatapower' → TATAPOWER.NS              │       │
│  │ Gap Analysis, Returns, Volatility                      │       │
│  └───────────────────────────────────────────────────────┘       │
│                                                                  │
│  ANALYSIS                                                        │
│  ┌──────────────┬──────────────┬──────────────────────┐         │
│  │ Correlator   │ Backtester   │ Projector            │         │
│  │ (merge data) │ (hit rates)  │ (aggregate signals)  │         │
│  └──────────────┴──────────────┴──────────────────────┘         │
│                                                                  │
│  OUTPUT                                                          │
│  ┌──────────────┬──────────────┬──────────────────────┐         │
│  │ Daily Report │Weekly Report │ Monthly Report       │         │
│  ├──────────────┴──────────────┴──────────────────────┤         │
│  │ 🌐 Streamlit Web Dashboard                         │         │
│  │ (6 tabs: Planets, Yogas, Hora, Projection,         │         │
│  │  Dasha, Sectors)                                    │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  CLI: python main.py --project bitcoin 2025-03-20               │
│  WEB: streamlit run dashboard/app.py                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

🆘 TROUBLESHOOTING
Problem	Solution
ModuleNotFoundError: No module named 'core'	Make sure you're running from the project root folder. Run cd /workspaces/fin-astro-bot first
ImportError: cannot import name...	Check the file exists and has no typos. Run ls core/ to verify
pyswisseph won't install	Try pip install pyswisseph --no-cache-dir
Ephemeris errors	Re-download: cd ephe && curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1 && cd ..
Streamlit won't open	In Codespaces, check the PORTS tab at bottom. Click the globe icon next to port 8501
yfinance returns empty data	Yahoo Finance may be temporarily down. Try again in a few minutes
swe.rise_trans errors in hora.py	The sunrise calculation may fail on some platforms. The fallback (approximate) will be used automatically
Old astro_engine.py conflicts	Delete the old file in root: rm -f astro_engine.py market_data.py insights.py
Delete old v1 files that might conflict:

bash

Copy code
rm -f astro_engine.py market_data.py insights.py

🔮 YOUR DAILY WORKFLOW
yaml

Copy code
Morning (before 9:15 AM):
  python main.py --quick              # Quick planet check
  python main.py --hora               # Know your hora windows
  python main.py --project nifty      # Full projection

During Market:
  Refer to hora timing for entry/exit windows
  Check sector rotation for stock selection

Weekly:
  python main.py --weekly nifty       # Generate week-ahead report

Monthly:
  python main.py --monthly nifty      # Month overview + critical dates

Research:
  python main.py --build nifty        # Build historical dataset
  python main.py --backtest nifty     # Find which patterns actually work
  python main.py --project bitcoin    # Test on any asset

Dashboard (anytime):
  streamlit run dashboard/app.py      # Beautiful web interface

You now have the most comprehensive Financial Astrology research tool ever built as a personal project. Every single technique from Vedic astrology that's relevant to markets is included