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