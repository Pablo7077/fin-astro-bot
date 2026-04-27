"""
=============================================================
FIN ASTRO BOT v2.5 — Projection Backtester
=============================================================
Tests the final user-facing projection output against historical market data.
=============================================================
"""

import os
from typing import Any, Optional

import pandas as pd

from analysis.correlator import get_or_build_dataset
from analysis.projector import generate_full_projection, MODEL_VERSION

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def classify_gap(gap_pct: Any, threshold: float = 0.15) -> str:
    gap = _safe_float(gap_pct)
    if gap > threshold:
        return "GAP_UP"
    if gap < -threshold:
        return "GAP_DOWN"
    return "FLAT"


def classify_bias(row: pd.Series, threshold: float = 0.10) -> str:
    if "Day_Direction" in row and str(row.get("Day_Direction")) in ("Bullish", "Bearish", "Neutral"):
        val = str(row.get("Day_Direction"))
        return "BULLISH" if val == "Bullish" else ("BEARISH" if val == "Bearish" else "NEUTRAL")
    ret = _safe_float(row.get("Daily_Return", row.get("return_pct", 0)))
    if ret > threshold:
        return "BULLISH"
    if ret < -threshold:
        return "BEARISH"
    return "NEUTRAL"


def normalize_gap_prediction(value: Any) -> str:
    text = str(value or "").upper()
    if "NO EDGE" in text or "SKIP" in text or "NO TRADE" in text:
        return "NO_EDGE"
    if "GAP UP" in text or "GAP_UP" in text:
        return "GAP_UP"
    if "GAP DOWN" in text or "GAP_DOWN" in text:
        return "GAP_DOWN"
    if "FLAT" in text or "SIDEWAYS" in text:
        return "FLAT"
    if "VOLATILE" in text:
        return "VOLATILE"
    return "UNKNOWN"


def normalize_bias_prediction(value: Any) -> str:
    text = str(value or "").upper()
    if "NO EDGE" in text or "SKIP" in text or "NO TRADE" in text:
        return "NO_TRADE"
    if "BULLISH" in text:
        return "BULLISH"
    if "BEARISH" in text:
        return "BEARISH"
    if "VOLATILE" in text:
        return "VOLATILE"
    if "SIDEWAYS" in text or "NEUTRAL" in text:
        return "NEUTRAL"
    return "UNKNOWN"


def run_projection_backtest(
    symbol: str = "nifty",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_days: Optional[int] = None,
) -> pd.DataFrame:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dataset, display_name = get_or_build_dataset(symbol)
    if dataset is None or dataset.empty:
        raise RuntimeError(f"No dataset available for {symbol}. Run: python main.py --build {symbol} 2010-01-01")

    data = dataset.copy()
    data.index = pd.to_datetime(data.index)
    if start_date:
        data = data[data.index >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data.index <= pd.to_datetime(end_date)]
    if max_days:
        data = data.tail(int(max_days))

    print("\n🎯 PROJECTION BACKTEST")
    print("=" * 60)
    print(f"Symbol: {symbol} ({display_name})")
    print(f"Rows: {len(data)}")
    print(f"Model: {MODEL_VERSION}")

    rows = []
    for idx, (date, row) in enumerate(data.iterrows(), start=1):
        date_str = date.strftime("%Y-%m-%d")
        if idx == 1 or idx % 100 == 0:
            print(f"  Processing {idx}/{len(data)} — {date_str}")
        try:
            projection = generate_full_projection(date_str, symbol, data, return_result=True, verbose=False)
            predicted_gap = normalize_gap_prediction(projection.get("gap_projection"))
            predicted_bias = normalize_bias_prediction(projection.get("bias"))
            actual_gap = classify_gap(row.get("Gap_Pct", row.get("gap_pct")))
            actual_bias = classify_bias(row)

            gap_correct = None if predicted_gap in ("NO_EDGE", "VOLATILE", "UNKNOWN") else predicted_gap == actual_gap
            bias_correct = None if predicted_bias in ("NO_TRADE", "VOLATILE", "UNKNOWN") else predicted_bias == actual_bias

            rows.append({
                "date": date_str,
                "symbol": symbol,
                "model_version": projection.get("model_version", MODEL_VERSION),
                "predicted_gap": predicted_gap,
                "actual_gap": actual_gap,
                "gap_pct": row.get("Gap_Pct", row.get("gap_pct")),
                "gap_correct": gap_correct,
                "predicted_bias": predicted_bias,
                "actual_bias": actual_bias,
                "return_pct": row.get("Daily_Return", row.get("return_pct")),
                "bias_correct": bias_correct,
                "confidence": projection.get("confidence"),
                "signal_count": projection.get("signal_count"),
                "market_regime": projection.get("market_regime"),
                "bullish_score": projection.get("bullish_score"),
                "bearish_score": projection.get("bearish_score"),
                "volatile_score": projection.get("volatile_score"),
                "decision_trace": projection.get("decision_trace"),
                "error": "",
            })
        except Exception as e:
            rows.append({"date": date_str, "symbol": symbol, "model_version": MODEL_VERSION, "error": str(e)})

    result_df = pd.DataFrame(rows)
    safe_sym = symbol.replace(" ", "_").replace("^", "")
    output_file = os.path.join(OUTPUT_DIR, f"projection_backtest_{safe_sym}.csv")
    result_df.to_csv(output_file, index=False)

    print("\n==============================")
    print("PROJECTION BACKTEST COMPLETE")
    print("==============================")
    print(f"Saved to: {output_file}")

    if "gap_correct" in result_df:
        active_gap = result_df[result_df["gap_correct"].notna()]
        if len(active_gap):
            print(f"Active gap predictions: {len(active_gap)} / {len(result_df)}")
            print(f"Active gap accuracy: {active_gap['gap_correct'].mean() * 100:.2f}%")
    if "bias_correct" in result_df:
        active_bias = result_df[result_df["bias_correct"].notna()]
        if len(active_bias):
            print(f"Active bias predictions: {len(active_bias)} / {len(result_df)}")
            print(f"Active bias accuracy: {active_bias['bias_correct'].mean() * 100:.2f}%")

    if "confidence" in result_df:
        tmp = result_df.copy()
        tmp["confidence"] = pd.to_numeric(tmp["confidence"], errors="coerce")
        tmp["confidence_bucket"] = pd.cut(tmp["confidence"], bins=[0, 40, 50, 60, 70, 100], labels=["0-40", "40-50", "50-60", "60-70", "70+"])
        summary = tmp.groupby("confidence_bucket", observed=False).agg(
            days=("date", "count"),
            gap_accuracy=("gap_correct", "mean"),
            bias_accuracy=("bias_correct", "mean"),
        )
        print("\nAccuracy by confidence bucket:")
        print(summary)

    return result_df


if __name__ == "__main__":
    run_projection_backtest("nifty")
