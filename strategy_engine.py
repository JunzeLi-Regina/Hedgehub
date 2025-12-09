from dataclasses import dataclass
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


@dataclass
class PairResult:
    pair_ok: bool
    mode: str
    signal: str
    explanation: str
    hedge_ratio: float
    coint_pvalue: float
    last_spread: float
    last_zscore: float
    spread_series: pd.Series


def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    data = yf.download(
        ticker, start=start, end=end,
        progress=False, auto_adjust=False
    )
    if "Adj Close" not in data.columns:
        raise ValueError(f"No Adj Close found for {ticker}")
    return data["Adj Close"].dropna()


def estimate_hedge_ratio(prices_a: pd.Series, prices_b: pd.Series) -> float:
    x = sm.add_constant(prices_b.values)
    y = prices_a.values
    model = sm.OLS(y, x).fit()
    return float(model.params[1])


def adf_test(series: pd.Series) -> float:
    return float(adfuller(series.values)[1])


def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    entry_z: float = 2.0,
    exit_z: float = 0.5
) -> PairResult:

    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    df.columns = ["A", "B"]

    beta = estimate_hedge_ratio(df["A"], df["B"])
    spread = df["A"] - beta * df["B"]

    pvalue = adf_test(spread)
    pair_ok = pvalue < 0.05

    mean_spread = spread.mean()
    std_spread = spread.std(ddof=1)
    last_spread = float(spread.iloc[-1])
    z = (last_spread - mean_spread) / std_spread if std_spread > 0 else 0.0

    if not pair_ok:
        explanation = (
            f"Cointegration test result: fail (ADF p-value = {pvalue:.3f}). "
            "The price relationship does not exhibit reliable mean-reverting behavior. "
            "You may stop here or continue with a trend-based momentum signal instead."
        )

        return PairResult(
            pair_ok=False,
            mode="mean_reversion",
            signal="no_pairs_trade_cointegration_failed",
            explanation=explanation,
            hedge_ratio=beta,
            coint_pvalue=pvalue,
            last_spread=last_spread,
            last_zscore=z,
            spread_series=spread,
        )

    entry_upper = mean_spread + entry_z * std_spread
    entry_lower = mean_spread - entry_z * std_spread
    exit_low = mean_spread - exit_z * std_spread
    exit_high = mean_spread + exit_z * std_spread

    if z > entry_z:
        signal = "short_A_long_B"
        explanation = (
            f"The spread is above the upper entry threshold (z = {z:.2f}). "
            f"Suggested action: short {ticker_a} and long {ticker_b}. "
            f"Exit if spread returns to the estimated neutral range: {exit_low:.2f} to {exit_high:.2f}."
        )

    elif z < -entry_z:
        signal = "long_A_short_B"
        explanation = (
            f"The spread is below the lower entry threshold (z = {z:.2f}). "
            f"Suggested action: long {ticker_a} and short {ticker_b}. "
            f"Exit if spread normalizes back into the estimated neutral range: {exit_low:.2f} to {exit_high:.2f}."
        )

    elif abs(z) <= exit_z:
        signal = "close_positions"
        explanation = (
            f"The spread has returned to the neutral zone (z = {z:.2f}). "
            "Suggested action: close open positions."
        )

    else:
        signal = "no_trade"
        explanation = (
            f"No entry signal detected (current z = {z:.2f}). "
            "Monitoring only; no new trade recommended at this stage."
        )

    return PairResult(
        pair_ok=True,
        mode="mean_reversion",
        signal=signal,
        explanation=explanation,
        hedge_ratio=beta,
        coint_pvalue=pvalue,
        last_spread=last_spread,
        last_zscore=z,
        spread_series=spread,
    )


def analyze_pair_momentum(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    high_pct: float = 0.9,
    low_pct: float = 0.1
) -> PairResult:

    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    df.columns = ["A", "B"]

    ratio = df["A"] / df["B"]

    cur = float(ratio.iloc[-1])
    high = float(ratio.quantile(high_pct))
    low = float(ratio.quantile(low_pct))
    stop_reference = float(ratio.quantile(0.5))

    if cur > high:
        signal = "momentum_buy_A_sell_B"
        explanation = (
            f"The price ratio indicates upward momentum beyond the breakout level. "
            f"Suggested action: buy {ticker_a} and sell {ticker_b}. "
            f"Suggested protective stop at {stop_reference:.4f}."
        )

    elif cur < low:
        signal = "momentum_buy_B_sell_A"
        explanation = (
            f"The price ratio indicates downward momentum below the lower threshold. "
            f"Suggested action: buy {ticker_b} and sell {ticker_a}. "
            f"Suggested protective stop at {stop_reference:.4f}."
        )

    else:
        signal = "hold_no_signal"
        explanation = (
            "No strong directional momentum detected. No trade is suggested at this time."
        )

    return PairResult(
        pair_ok=False,
        mode="momentum",
        signal=signal,
        explanation=explanation,
        hedge_ratio=0.0,
        coint_pvalue=0.0,
        last_spread=cur,
        last_zscore=0.0,
        spread_series=ratio,
    )
