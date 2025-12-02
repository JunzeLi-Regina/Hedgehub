from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


@dataclass
class PairResult:
    pair_ok: bool
    coint_pvalue: float
    hedge_ratio: float
    last_spread: float
    last_zscore: float
    signal: str
    explanation: str
    spread_series: pd.Series


def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    data = yf.download(
    ticker,
    start=start,
    end=end,
    progress=False,
    auto_adjust=False
)

    if "Adj Close" not in data.columns:
        raise ValueError(f"{ticker} downloaded no Adj Close data")
    return data["Adj Close"].dropna()


def estimate_hedge_ratio(prices_a: pd.Series, prices_b: pd.Series) -> float:
    x = sm.add_constant(prices_b.values)
    y = prices_a.values
    model = sm.OLS(y, x).fit()
    beta = float(model.params[1])
    return beta


def adf_test(series: pd.Series) -> float:
    result = adfuller(series.values)
    return float(result[1])  # p-value


def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    entry_z: float = 2.0,
) -> PairResult:

    # ---- Download prices ----
    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    # Align dates
    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    df.columns = ["A", "B"]

    prices_a = df["A"]
    prices_b = df["B"]

    # Hedge ratio
    beta = estimate_hedge_ratio(prices_a, prices_b)

    # Spread = A – βB
    spread = prices_a - beta * prices_b

    # ADF p-value
    pvalue = adf_test(spread)
    pair_ok = pvalue < 0.05

    # z-score
    mean_spread = spread.mean()
    std_spread = spread.std(ddof=1)
    last_spread = float(spread.iloc[-1])
    z = float((last_spread - mean_spread) / std_spread) if std_spread > 0 else 0.0

    # Generate trading signal
    if not pair_ok:
        signal = "no_trade"
        explanation = (
            f"The pair {ticker_a}/{ticker_b} does NOT pass the cointegration test "
            f"(p-value={pvalue:.3f}). The spread is not mean-reverting. "
            f"This pair is not recommended for pairs trading."
        )
    else:
        if z > entry_z:
            signal = "short_A_long_B"
            explanation = (
                f"The pair {ticker_a}/{ticker_b} is cointegrated (p-value={pvalue:.3f}).\n"
                f"Current z-score = {z:.2f} > {entry_z}. "
                f"→ Suggestion: SHORT {ticker_a} and LONG {ticker_b}."
            )
        elif z < -entry_z:
            signal = "long_A_short_B"
            explanation = (
                f"The pair {ticker_a}/{ticker_b} is cointegrated (p-value={pvalue:.3f}).\n"
                f"Current z-score = {z:.2f} < -{entry_z}. "
                f"→ Suggestion: LONG {ticker_a} and SHORT {ticker_b}."
            )
        else:
            signal = "no_trade"
            explanation = (
                f"The pair {ticker_a}/{ticker_b} is cointegrated (p-value={pvalue:.3f}).\n"
                f"Current z-score = {z:.2f}, within normal range. No trade signal."
            )

    return PairResult(
        pair_ok=pair_ok,
        coint_pvalue=pvalue,
        hedge_ratio=beta,
        last_spread=last_spread,
        last_zscore=z,
        signal=signal,
        explanation=explanation,
        spread_series=spread,
    )
