"""
=============================================================
FIN ASTRO BOT v2.5 — Projection Engine
=============================================================
Aggregates astro, panchang, yoga, hora, mundane, KP and
historical-pattern signals into one projection.

Design goals in v2.5:
- Keep the original visible report output for daily/weekly use.
- Support quiet return_result=True mode for backtesting.
- Prevent float/int formatting crashes.
- Reduce structural bullish bias and weak sideways calls.
- Add a clear model_version and decision_trace for QA.
=============================================================
"""

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

from core.astro_engine import full_astro_analysis
from core.yogas import detect_all_yogas
from core.panchang import get_full_panchang
from core.hora import get_trading_hora_summary
from core.dasha import get_index_dasha
from core.kp_system import get_kp_analysis
from core.mundane import get_mundane_analysis

MODEL_VERSION = "v2.5-conservative-balanced-pipeline-2026-04-28"
Signal = Tuple[str, str, float, str]


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _print(verbose: bool, *args: Any, **kwargs: Any) -> None:
    if verbose:
        print(*args, **kwargs)


def _normalize_signal(direction: str) -> str:
    text = str(direction or "").upper()
    if "BEAR" in text:
        return "BEARISH"
    if "BULL" in text:
        return "BULLISH"
    if "VOL" in text or "TREND" in text:
        return "VOLATILE"
    return "NEUTRAL"


def _append_signal(signals: List[Signal], name: str, direction: str, weight: Any, detail: Any) -> None:
    direction = _normalize_signal(direction)
    if direction == "NEUTRAL":
        return
    signals.append((str(name), direction, _safe_float(weight), str(detail)))


def _get_col(dataset: Any, candidates: Iterable[str]) -> Optional[str]:
    if dataset is None or getattr(dataset, "empty", True):
        return None
    for col in candidates:
        if col in dataset.columns:
            return col
    return None


def get_market_regime(dataset: Any, target_date: str) -> str:
    """
    Returns UPTREND, DOWNTREND, CHOPPY, or UNKNOWN using only data
    available up to target_date. If target_date is beyond the cache, the
    latest cached day is used.
    """
    try:
        if dataset is None or dataset.empty:
            return "UNKNOWN"

        data = dataset.copy()
        data.index = data.index.tz_localize(None) if getattr(data.index, "tz", None) is not None else data.index
        data.index = data.index.astype("datetime64[ns]")
        target_ts = datetime.strptime(str(target_date), "%Y-%m-%d")
        data = data[data.index <= target_ts]
        if len(data) < 55:
            return "UNKNOWN"

        close_col = _get_col(data, ["Close", "close", "Adj Close", "Adj_Close"])
        if close_col is None:
            return "UNKNOWN"

        if "SMA_20" not in data.columns:
            data["SMA_20"] = data[close_col].rolling(20).mean()
        if "SMA_50" not in data.columns:
            data["SMA_50"] = data[close_col].rolling(50).mean()

        recent = data.tail(20)
        latest = data.iloc[-1]
        sma20 = _safe_float(latest.get("SMA_20"))
        sma50 = _safe_float(latest.get("SMA_50"))
        close = _safe_float(latest.get(close_col))
        if not close or not sma20 or not sma50:
            return "UNKNOWN"

        ret_col = _get_col(data, ["Daily_Return", "Return_Pct", "return_pct"])
        recent_return = 0.0
        if ret_col:
            recent_return = _safe_float(recent[ret_col].sum())
        else:
            first = _safe_float(recent[close_col].iloc[0])
            last = _safe_float(recent[close_col].iloc[-1])
            if first:
                recent_return = ((last / first) - 1) * 100

        vol_col = _get_col(data, ["Volatility_20d", "Volatility", "volatility"])
        volatility = _safe_float(latest.get(vol_col)) if vol_col else 0.0

        if close > sma20 > sma50 and recent_return > 0:
            return "UPTREND"
        if close < sma20 < sma50 and recent_return < 0:
            return "DOWNTREND"
        if volatility >= 1.25:
            return "CHOPPY"
        return "CHOPPY"
    except Exception:
        return "UNKNOWN"


def apply_foundation_adjustments(signals: List[Signal], market_regime: str) -> Tuple[List[Signal], List[str]]:
    """
    Applies conservative signal calibration without deleting the original
    astrology information. This is intentionally explainable and visible in
    decision_trace.
    """
    adjusted: List[Signal] = []
    trace: List[str] = []

    # Keep subjective high-impact yogas under control; they are useful as
    # context, but should not overpower historical/regime evidence alone.
    name_multipliers = {
        "Kala Sarpa": 0.55,
        "Kemadruma": 0.60,
        "Vashi": 0.65,
        "Mundane Transits": 0.75,
        "Good Nitya Yoga": 0.75,
        "Waxing Moon": 0.70,
        "Moon in ": 0.85,
        "Tithi:": 0.85,
        "Retrogrades": 0.85,
    }

    for name, direction, weight, detail in signals:
        w = _safe_float(weight)
        for key, mult in name_multipliers.items():
            if key.lower() in name.lower():
                w *= mult
                trace.append(f"Adjusted {name} x{mult:.2f}")
                break
        adjusted.append((name, direction, w, detail))

    # Regime calibration: this is the main anti-bias layer.
    regime_adjusted: List[Signal] = []
    for name, direction, weight, detail in adjusted:
        w = _safe_float(weight)
        if market_regime == "DOWNTREND":
            if direction == "BULLISH":
                w *= 0.72
            elif direction == "BEARISH":
                w *= 1.30
        elif market_regime == "UPTREND":
            if direction == "BULLISH":
                w *= 1.05
            elif direction == "BEARISH":
                w *= 0.88
        elif market_regime == "CHOPPY":
            if direction == "BULLISH":
                w *= 0.82
            elif direction == "BEARISH":
                w *= 1.05
            elif direction == "VOLATILE":
                w *= 1.18
        regime_adjusted.append((name, direction, w, detail))
    trace.append(f"Market regime calibration applied: {market_regime}")
    return regime_adjusted, trace


def add_calendar_context(signals: List[Signal], target_date: str) -> List[Signal]:
    """Small, non-dominant calendar context based on observed analysis."""
    try:
        dt = datetime.strptime(target_date, "%Y-%m-%d")
        weekday = dt.strftime("%A")
        month = dt.month
        if weekday == "Wednesday":
            _append_signal(signals, "Wednesday Calendar Context", "BULLISH", 2.0, "Small positive weekday context")
        if month in (5, 7):
            _append_signal(signals, "May/July Calendar Context", "BULLISH", 2.0, "Small positive month context")
        if month in (4, 5, 6, 7, 8, 9):
            _append_signal(signals, "Q2/Q3 Calendar Context", "BULLISH", 1.5, "Small positive quarter context")
    except Exception:
        pass
    return signals


def decide_projection(
    bullish_score: float,
    bearish_score: float,
    volatile_score: float,
    signal_count: int,
    market_regime: str,
) -> Tuple[str, str, float, List[str]]:
    """Balanced decision layer used by BOTH CLI reports and backtests."""
    trace: List[str] = []
    total = max(bullish_score + bearish_score + volatile_score, 0.0001)
    bull_share = bullish_score / total * 100
    bear_share = bearish_score / total * 100
    vol_share = volatile_score / total * 100
    dominance = abs(bullish_score - bearish_score) / total

    confidence = 38 + dominance * 42
    if signal_count < 10:
        confidence += 5
        trace.append("Signal count <10: confidence +5")
    elif signal_count > 18:
        confidence -= 6
        trace.append("Signal count >18: confidence -6")

    if market_regime == "DOWNTREND":
        confidence += 3
    elif market_regime == "CHOPPY":
        confidence -= 4

    gap_proj = "⚪ NO EDGE / SKIP"
    bias = "NO TRADE"

    # No pure SIDEWAYS calls: prior analysis showed SIDEWAYS had weak accuracy.
    if vol_share >= 44 and dominance < 0.20:
        gap_proj = "🔀 VOLATILE / NO CLEAR DIRECTION"
        bias = "VOLATILE"
        confidence = min(confidence, 52)
        trace.append("Volatile dominance with low directional edge")
    elif market_regime == "DOWNTREND" and bear_share >= 35 and bearish_score >= bullish_score * 0.92:
        gap_proj = "📉 GAP DOWN EXPECTED"
        bias = "BEARISH"
        confidence += 8
        trace.append("Bearish accepted because regime is DOWNTREND")
    elif bear_share >= 39 and bearish_score >= bullish_score * 1.10 and bearish_score >= volatile_score * 0.75:
        gap_proj = "📉 GAP DOWN EXPECTED"
        bias = "BEARISH"
        confidence += 4
        trace.append("Bearish accepted by score dominance")
    elif bull_share >= 44 and bullish_score >= bearish_score * 1.18 and bullish_score >= volatile_score * 0.85:
        gap_proj = "📈 GAP UP EXPECTED"
        bias = "BULLISH"
        confidence += 2
        trace.append("Bullish accepted by stricter anti-bias rule")
    elif bull_share >= 40 and market_regime == "UPTREND" and bullish_score >= bearish_score * 1.05:
        gap_proj = "📈 GAP UP EXPECTED"
        bias = "BULLISH"
        confidence += 4
        trace.append("Bullish accepted because regime is UPTREND")
    else:
        trace.append("No clean directional edge after calibration")

    # Low confidence directional calls become research-only/no-edge.
    if bias in ("BULLISH", "BEARISH") and confidence < 48:
        trace.append("Directional call below confidence floor; converted to NO EDGE")
        gap_proj = "⚪ NO EDGE / SKIP"
        bias = "NO TRADE"

    confidence = max(0, min(confidence, 82))
    trace.append(f"Shares B/B/V: {bull_share:.1f}/{bear_share:.1f}/{vol_share:.1f}; dominance {dominance:.2f}")
    return gap_proj, bias, confidence, trace


def generate_full_projection(
    target_date: Optional[str] = None,
    symbol: str = "nifty",
    dataset: Any = None,
    return_result: bool = False,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Master projection function.

    Parameters are backward-compatible with old calls:
      generate_full_projection(date_str, symbol, dataset)
    New backtest/report calls can use:
      generate_full_projection(date_str, symbol, dataset, return_result=True, verbose=False)
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    _print(verbose, f"\n{'='*70}")
    _print(verbose, "🔮 FIN ASTRO BOT v2.5 — COMPLETE PROJECTION")
    _print(verbose, f"Decision Engine: {MODEL_VERSION}")
    _print(verbose, f"📅 Date: {target_date}  |  📊 Symbol: {symbol.upper()}")
    _print(verbose, f"{'='*70}")

    signals: List[Signal] = []

    analysis = full_astro_analysis(target_date)
    pos = analysis["positions"]

    _print(verbose, f"\n{'─'*50}")
    _print(verbose, "📍 PLANETARY POSITIONS (Sidereal/Lahiri)")
    _print(verbose, f"{'─'*50}")
    _print(verbose, f"{'Planet':10s} {'Sign':13s} {'Deg':>7s} {'Nakshatra':16s} {'Dignity':12s} {'R':3s}")
    _print(verbose, f"{'─'*70}")
    for name, d in pos.items():
        r = "℞" if d.get("retrograde") else ""
        _print(verbose, f"{name:10s} {d['sign']:13s} {d['sign_degree']:6.2f}° "
                        f"{d['nakshatra']:13s} P{d['pada']}  {d['dignity']:12s} {r}")

    for planet in ["Jupiter", "Venus", "Saturn", "Mars"]:
        dignity = pos[planet]["dignity"]
        if dignity == "Exalted":
            bias = "BULLISH" if planet in ["Jupiter", "Venus"] else "VOLATILE"
            _append_signal(signals, f"{planet} Exalted", bias, 12, f"{planet} at peak strength")
        elif dignity == "Debilitated":
            bias = "BEARISH" if planet in ["Jupiter", "Venus"] else "VOLATILE"
            _append_signal(signals, f"{planet} Debilitated", bias, 10, f"{planet} weakened")

    yogas = detect_all_yogas(pos)
    if yogas:
        _print(verbose, f"\n{'─'*50}")
        _print(verbose, f"⭐ ACTIVE YOGAS ({len(yogas)} found)")
        _print(verbose, f"{'─'*50}")
        for y in yogas:
            direction = _normalize_signal(y.get("market_bias", ""))
            emoji = "🟢" if direction == "BULLISH" else ("🔴" if direction == "BEARISH" else "🟡")
            _print(verbose, f"  {emoji} {y['name']} [{y['category']}]")
            _print(verbose, f"    {y['description']}")
            _print(verbose, f"    Bias: {str(y['market_bias']).upper()} | Weight: {_safe_float(y.get('weight')):.1f}")
            weight = _safe_float(y.get("weight"))
            if direction == "VOLATILE":
                weight *= 0.5
            _append_signal(signals, f"Yoga: {y['name']}", direction, weight, y.get("description", ""))

    panchang = get_full_panchang(target_date, pos)
    t = panchang["tithi"]
    k = panchang["karana"]
    ny = panchang["nitya_yoga"]
    v = panchang["vara"]
    mp = panchang["moon_phase"]

    _print(verbose, f"\n{'─'*50}")
    _print(verbose, "📅 PANCHANG")
    _print(verbose, f"{'─'*50}")
    _print(verbose, f"  Vara:        {v['name']} (Lord: {v['lord']})")
    _print(verbose, f"  Tithi:       {t['paksha']} {t['name']} (#{t['number']})")
    _print(verbose, f"  Karana:      {k['name']} ({k['nature']})")
    _print(verbose, f"  Nitya Yoga:  {ny['name']} ({ny['nature']})")
    _print(verbose, f"  Moon Phase:  {mp['phase']}")
    _print(verbose, f"  Moon Nak:    {panchang['moon_nakshatra']['name']} P{panchang['moon_nakshatra']['pada']}")

    if t.get("is_critical"):
        _append_signal(signals, "Critical Tithi", "VOLATILE", 15, f"{t['name']} — high risk day")
    if k.get("is_vishti"):
        _append_signal(signals, "Vishti Karana", "BEARISH", 18, "Bhadra Karana — avoid new trades")
    if ny.get("is_inauspicious"):
        _append_signal(signals, "Bad Nitya Yoga", "BEARISH", 14, f"{ny['name']} — inauspicious yoga")
    elif ny.get("nature") == "Shubha":
        _append_signal(signals, "Good Nitya Yoga", "BULLISH", 10, f"{ny['name']} — auspicious yoga")

    phase = mp.get("phase", "")
    if "New Moon" in phase:
        _append_signal(signals, "New Moon", "VOLATILE", 12, "Low energy, potential reversal")
    elif "Full Moon" in phase:
        _append_signal(signals, "Full Moon", "VOLATILE", 12, "Peak emotion, potential reversal")
    elif "Waxing" in phase:
        _append_signal(signals, "Waxing Moon", "BULLISH", 8, "Building momentum")
    elif "Waning" in phase:
        _append_signal(signals, "Waning Moon", "BEARISH", 8, "Declining momentum")

    for g in panchang.get("gandantas", []):
        if g.get("planet") == "Moon":
            _append_signal(signals, "Moon Gandanta", "VOLATILE", 20, f"Moon at {g.get('junction')} — extreme karmic zone")
            _print(verbose, f"\n  🔥 GANDANTA: Moon at {g.get('junction')} ({g.get('severity')})")

    if panchang.get("void_of_course", {}).get("is_voc"):
        _append_signal(signals, "Void of Course Moon", "VOLATILE", 10, "Market may drift aimlessly")
        _print(verbose, f"  🕳️ VOC Moon: {panchang['void_of_course'].get('note')}")

    try:
        hora = get_trading_hora_summary(target_date)
        _print(verbose, f"\n{'─'*50}")
        _print(verbose, "⏰ INTRADAY HORA TIMING")
        _print(verbose, f"{'─'*50}")
        _print(verbose, f"  Day Ruler: {hora['day_ruler']}")
        for h in hora.get("market_horas", []):
            emoji = "🟢" if h.get("bias") == "bullish" else ("🔴" if h.get("bias") == "bearish" else "🟡")
            _print(verbose, f"  {h['start']}-{h['end']} {emoji} {h['planet']:10s} {h['action']}")
        _print(verbose, "\n  ⚠️ Inauspicious Periods:")
        for name, period in hora.get("inauspicious", {}).items():
            if "rahu" in name or "abhijit" in name:
                _print(verbose, f"    {name}: {period['start']}-{period['end']}")
    except Exception as e:
        _print(verbose, f"  (Hora calculation skipped: {e})")

    for c in analysis.get("combustions", []):
        _print(verbose, f"\n  🔥 Combustion: {c.get('planet')} — {c.get('severity')} ({c.get('distance_from_sun')}° from Sun)")
    for w in analysis.get("planetary_wars", []):
        _print(verbose, f"\n  ⚔️ Planetary War: {w.get('planet1')} vs {w.get('planet2')} — Winner: {w.get('winner')}")
        _append_signal(signals, "Planetary War", "VOLATILE", 15, f"{w.get('planet1')} vs {w.get('planet2')}")
    for s in analysis.get("stations", []):
        _print(verbose, f"\n  🛑 Station: {s.get('planet')}: {s.get('type')}")
        _append_signal(signals, "Planet Station", "VOLATILE", 18, f"{s.get('planet')} {s.get('type')}")
    for ing in analysis.get("ingresses", []):
        _print(verbose, f"\n  🚀 Sign Change: {ing.get('planet')}: {ing.get('from_sign')} → {ing.get('to_sign')}")
        _append_signal(signals, "Sign Change", "VOLATILE", 10, f"{ing.get('planet')} enters {ing.get('to_sign')}")

    try:
        if symbol.lower() in ["nifty", "banknifty", "sensex"]:
            dasha = get_index_dasha(symbol.lower(), target_date)
            if dasha.get("current"):
                maha = dasha["current"]["mahadasha"]
                antar = dasha["current"].get("antardasha")
                _print(verbose, f"\n{'─'*50}")
                _print(verbose, f"🔮 DASHA PERIODS ({symbol.upper()})")
                _print(verbose, f"{'─'*50}")
                _print(verbose, f"  Mahadasha: {maha['lord']} ({maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')})")
                if antar:
                    _print(verbose, f"  Antardasha: {antar['antardasha_lord']} ({antar['start'].strftime('%Y-%m-%d')} to {antar['end'].strftime('%Y-%m-%d')})")
                overall = maha.get("interpretation", {}).get("overall", "")
                if "BULLISH" in overall.upper():
                    _append_signal(signals, "Mahadasha", "BULLISH", 15, f"{maha['lord']} Mahadasha — {overall}")
                elif "CHALLENGING" in overall.upper() or "BEARISH" in overall.upper():
                    _append_signal(signals, "Mahadasha", "BEARISH", 15, f"{maha['lord']} Mahadasha — {overall}")
    except Exception as e:
        _print(verbose, f"  (Dasha skipped: {e})")

    try:
        kp = get_kp_analysis(target_date)
        rp = kp["ruling_planets"]
        _print(verbose, f"\n{'─'*50}")
        _print(verbose, "🎯 KP RULING PLANETS")
        _print(verbose, f"{'─'*50}")
        _print(verbose, f"  Rulers: {', '.join(rp['unique_rulers'])}")
        _print(verbose, f"  Bullish/Bearish: {rp['bullish_count']}/{rp['bearish_count']}")
        _print(verbose, f"  Bias: {rp['bias']}")
        if rp.get("bias") in ("BULLISH", "BEARISH"):
            _append_signal(signals, "KP Ruling Planets", rp["bias"], 12, rp.get("note", ""))
    except Exception as e:
        _print(verbose, f"  (KP skipped: {e})")

    try:
        if symbol.lower() in ["nifty", "banknifty", "sensex"]:
            charts = ["nifty", "india"] if symbol.lower() in ["nifty", "banknifty"] else ["india"]
            mundane = get_mundane_analysis(target_date, charts)
            if mundane.get("key_aspects"):
                _print(verbose, f"\n{'─'*50}")
                _print(verbose, "🏛️ MUNDANE TRANSIT ASPECTS")
                _print(verbose, f"{'─'*50}")
                for asp in mundane["key_aspects"][:5]:
                    _print(verbose, f"  {asp}")
                if mundane.get("overall_bias") in ("BULLISH", "BEARISH"):
                    _append_signal(signals, "Mundane Transits", mundane["overall_bias"], 15, f"Score: {_safe_float(mundane.get('total_score')):+.0f}")
    except Exception as e:
        _print(verbose, f"  (Mundane skipped: {e})")

    if dataset is not None and not getattr(dataset, "empty", True):
        _print(verbose, f"\n{'─'*50}")
        _print(verbose, "📊 HISTORICAL PATTERN MATCHING")
        _print(verbose, f"{'─'*50}")
        moon_sign = pos["Moon"]["sign"]
        moon_nak = pos["Moon"]["nakshatra"]
        try:
            if "Moon_Sign" in dataset.columns:
                moon_data = dataset[dataset["Moon_Sign"] == moon_sign]
                if len(moon_data) >= 10:
                    avg_gap = _safe_float(moon_data["Gap_Pct"].mean())
                    bullish_pct = _safe_float((moon_data["Day_Direction"] == "Bullish").mean() * 100) if "Day_Direction" in moon_data else 50
                    direction = "BULLISH" if avg_gap > 0.04 else ("BEARISH" if avg_gap < -0.04 else "NEUTRAL")
                    conf = min(abs(bullish_pct - 50) * 1.0, 12)
                    _append_signal(signals, f"Moon in {moon_sign}", direction, conf, f"{len(moon_data)} days, Avg Gap: {avg_gap:+.3f}%, Bullish: {bullish_pct:.1f}%")
                    _print(verbose, f"  Moon in {moon_sign}: {len(moon_data)} days, Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")
            if "Moon_Nakshatra" in dataset.columns:
                nak_data = dataset[dataset["Moon_Nakshatra"] == moon_nak]
                if len(nak_data) >= 8:
                    avg_gap = _safe_float(nak_data["Gap_Pct"].mean())
                    bullish_pct = _safe_float((nak_data["Day_Direction"] == "Bullish").mean() * 100) if "Day_Direction" in nak_data else 50
                    direction = "BULLISH" if avg_gap > 0.05 else ("BEARISH" if avg_gap < -0.05 else "NEUTRAL")
                    conf = min(abs(bullish_pct - 50) * 0.8, 10)
                    _append_signal(signals, f"Moon in {moon_nak}", direction, conf, f"{len(nak_data)} days, Avg Gap: {avg_gap:+.3f}%")
                    _print(verbose, f"  Moon in {moon_nak}: {len(nak_data)} days, Avg Gap: {avg_gap:+.4f}%, Bullish: {bullish_pct:.1f}%")
            if "Tithi" in dataset.columns:
                tithi_name = panchang["tithi"]["name"]
                tithi_data = dataset[dataset["Tithi"] == tithi_name]
                if len(tithi_data) >= 8:
                    avg_gap = _safe_float(tithi_data["Gap_Pct"].mean())
                    direction = "BULLISH" if avg_gap > 0.05 else ("BEARISH" if avg_gap < -0.05 else "NEUTRAL")
                    _append_signal(signals, f"Tithi: {tithi_name}", direction, 5, f"Avg Gap: {avg_gap:+.3f}%")
            if "Retro_Count" in dataset.columns:
                retro_count = sum(1 for p in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"] if pos[p]["retrograde"])
                rc_data = dataset[dataset["Retro_Count"] == retro_count]
                if len(rc_data) >= 10:
                    avg_gap = _safe_float(rc_data["Gap_Pct"].mean())
                    direction = "BULLISH" if avg_gap > 0.05 else ("BEARISH" if avg_gap < -0.05 else "NEUTRAL")
                    _append_signal(signals, f"{retro_count} Retrogrades", direction, 5, f"Avg Gap: {avg_gap:+.3f}%")
        except Exception as e:
            _print(verbose, f"  (Historical matching skipped: {e})")

    signals = add_calendar_context(signals, target_date)
    market_regime = get_market_regime(dataset, target_date)
    signals, adjustment_trace = apply_foundation_adjustments(signals, market_regime)

    bullish_score = sum(_safe_float(w) for _, d, w, _ in signals if d == "BULLISH")
    bearish_score = sum(_safe_float(w) for _, d, w, _ in signals if d == "BEARISH")
    volatile_score = sum(_safe_float(w) for _, d, w, _ in signals if d == "VOLATILE")

    gap_proj, bias, confidence, decision_trace = decide_projection(
        bullish_score, bearish_score, volatile_score, len(signals), market_regime
    )
    decision_trace = adjustment_trace + decision_trace

    total = max(bullish_score + bearish_score + volatile_score, 0.0001)
    bull_pct = bullish_score / total * 100
    bear_pct = bearish_score / total * 100
    vol_pct = volatile_score / total * 100

    _print(verbose, f"\n{'='*70}")
    _print(verbose, f"🎯 SIGNAL AGGREGATION ({len(signals)} signals)")
    _print(verbose, f"Engine: {MODEL_VERSION}")
    _print(verbose, f"{'='*70}")
    for name, direction, weight, detail in sorted(signals, key=lambda x: _safe_float(x[2]), reverse=True):
        emoji = "🟢" if direction == "BULLISH" else ("🔴" if direction == "BEARISH" else "🟡")
        _print(verbose, f"  {emoji} {name:30s} {direction:10s} wt:{_safe_float(weight):5.1f} | {str(detail)[:50]}")

    _print(verbose, f"\n  Bullish:  {bullish_score:6.1f} ({bull_pct:.0f}%)")
    _print(verbose, f"  Bearish:  {bearish_score:6.1f} ({bear_pct:.0f}%)")
    _print(verbose, f"  Volatile: {volatile_score:6.1f} ({vol_pct:.0f}%)")
    _print(verbose, f"  Market Regime: {market_regime}")
    _print(verbose, "  Decision Trace:")
    for item in decision_trace[-8:]:
        _print(verbose, f"    - {item}")

    _print(verbose, f"\n{'='*70}")
    _print(verbose, f"  🎯 GAP PROJECTION:    {gap_proj}")
    _print(verbose, f"  📊 DAY BIAS:          {bias}")
    _print(verbose, f"  🔮 CONFIDENCE:        ~{confidence:.0f}%")
    _print(verbose, f"{'='*70}")
    _print(verbose, "\n⚠️  DISCLAIMER:")
    _print(verbose, "  This is for RESEARCH & EDUCATION only.")
    _print(verbose, "  Astro signals are probabilistic, not deterministic.")
    _print(verbose, "  Always combine with technical analysis & risk management.")
    _print(verbose, "  Never risk capital solely on astrological signals.")

    return {
        "model_version": MODEL_VERSION,
        "date": target_date,
        "symbol": symbol,
        "gap_projection": gap_proj,
        "bias": bias,
        "day_bias": bias,
        "confidence": confidence,
        "signals": signals,
        "signal_count": len(signals),
        "market_regime": market_regime,
        "decision_trace": " | ".join(decision_trace),
        "bullish_score": bullish_score,
        "bearish_score": bearish_score,
        "volatile_score": volatile_score,
    }


if __name__ == "__main__":
    generate_full_projection(datetime.now().strftime("%Y-%m-%d"), "nifty")
