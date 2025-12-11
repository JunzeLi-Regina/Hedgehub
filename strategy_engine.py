from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


# ---------------------------------------------------------
# Performance metrics for backtest
# ---------------------------------------------------------
@dataclass
class PerformanceMetrics:
    initial_capital: float
    final_value: float
    total_return: float
    annualized_return: float
    annualized_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    total_trades: int


# ---------------------------------------------------------
# Main return object for pair analysis
# ---------------------------------------------------------
@dataclass
class PairResult:
    pair_ok: bool                      # Whether cointegration / mean reversion is valid
    mode: str                          # "mean_reversion" or "momentum"
    signal: str                        # Machine-friendly signal code
    explanation: str                   # Human-readable strategy explanation
    hedge_ratio: float
    coint_pvalue: float
    last_spread: float
    last_zscore: float
    spread_series: pd.Series

    # Extra fields used by UI
    prices: pd.DataFrame | None = None
    spread_zscores: pd.Series | None = None
    performance: PerformanceMetrics | None = None
    entry_z: float | None = None
    exit_z: float | None = None


@dataclass
class StrategyPlan:
    risk_level: str
    signal_type: str
    rationale: str
    entry_z: float
    exit_z: float
    spread_value: float
    zscore_value: float
    allocation_pct: float
    suggested_notional: float


_RISK_PRESETS: dict[str, dict[str, float]] = {
    "LOW": {"entry_z": 2.5, "exit_z": 0.75, "allocation_pct": 0.35},
    "MEDIUM": {"entry_z": 2.0, "exit_z": 0.5, "allocation_pct": 0.5},
    "HIGH": {"entry_z": 1.5, "exit_z": 0.35, "allocation_pct": 0.65},
}


def generate_strategy_plan(
    amount: float,
    risk_level: str,
    pair_result: PairResult | None = None,
    ticker_a: str | None = None,
    ticker_b: str | None = None,
) -> StrategyPlan:
    """Create simple strategy guidance based on risk appetite and latest spread stats."""

    def _clean_label(label: str | None, fallback: str) -> str:
        if not label:
            return fallback
        stripped = label.strip()
        return stripped.upper() if stripped else fallback

    label_a = _clean_label(ticker_a, "ASSET A")
    label_b = _clean_label(ticker_b, "ASSET B")

    preset_key = (risk_level or "MEDIUM").strip().upper()
    preset = _RISK_PRESETS.get(preset_key, _RISK_PRESETS["MEDIUM"])

    entry_z = float(preset["entry_z"])
    exit_z = float(preset["exit_z"])
    allocation_pct = float(preset["allocation_pct"])

    spread_value = 0.0
    zscore_value = 0.0
    rationale = "Configure Pair Analysis to unlock live spread context."

    if pair_result is not None:
        spread_value = float(pair_result.last_spread)
        zscore_value = float(pair_result.last_zscore)
        rationale = "Spread deviation versus long-term equilibrium."

    signal_type = "Wait for Entry"
    if zscore_value >= entry_z:
        signal_type = f"Short {label_a} Long {label_b}"
    elif zscore_value <= -entry_z:
        signal_type = f"Long {label_a} Short {label_b}"
    elif pair_result is None:
        signal_type = "Await Analysis"

    sanitized_amount = max(0.0, float(amount or 0.0))
    suggested_notional = sanitized_amount * allocation_pct

    return StrategyPlan(
        risk_level=preset_key.title(),
        signal_type=signal_type,
        rationale=rationale,
        entry_z=entry_z,
        exit_z=exit_z,
        spread_value=spread_value,
        zscore_value=zscore_value,
        allocation_pct=allocation_pct,
        suggested_notional=suggested_notional,
    )


# ---------------------------------------------------------
# Mean-reversion backtest on spread
# ---------------------------------------------------------
def run_mean_reversion_backtest(
    price_frame: pd.DataFrame,
    beta: float,
    zscores: pd.Series,
    entry_z: float,
    exit_z: float,
    initial_capital: float = 1_000_000.0,
    allocation: float = 0.5,
) -> PerformanceMetrics:
    rows = price_frame.shape[0]
    if rows < 2 or zscores.empty:
        return PerformanceMetrics(
            initial_capital=initial_capital,
            final_value=initial_capital,
            total_return=0.0,
            annualized_return=0.0,
            annualized_volatility=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            total_trades=0,
        )

    allocation = max(0.0, min(1.0, allocation))
    exposure_scale = max(1.0, 1.0 + abs(beta))

    returns_a = price_frame["A"].pct_change().fillna(0.0)
    returns_b = price_frame["B"].pct_change().fillna(0.0)

    position = 0.0
    capital = initial_capital
    equity_curve = [capital]
    daily_returns: list[float] = []
    trades = 0

    for idx in range(1, rows):
        z = float(zscores.iloc[idx - 1])

        # Exit when spread reverts into neutral zone
        if position != 0.0 and abs(z) <= exit_z:
            position = 0.0

        # Open new position only when flat
        if position == 0.0:
            if z > entry_z:
                # Spread too wide: short A, long B
                position = -allocation
                trades += 1
            elif z < -entry_z:
                # Spread too tight: long A, short B
                position = allocation
                trades += 1

        spread_return = (returns_a.iloc[idx] - beta * returns_b.iloc[idx]) / exposure_scale
        day_return = position * spread_return
        daily_returns.append(day_return)
        capital *= (1 + day_return)
        equity_curve.append(capital)

    if not daily_returns:
        return PerformanceMetrics(
            initial_capital=initial_capital,
            final_value=initial_capital,
            total_return=0.0,
            annualized_return=0.0,
            annualized_volatility=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            total_trades=0,
        )

    equity_series = pd.Series(equity_curve, index=price_frame.index)
    daily_series = pd.Series(daily_returns, index=price_frame.index[1:])

    total_return = float(capital / initial_capital - 1.0)

    num_periods = len(daily_returns)
    growth_factor = 1.0 + total_return
    if num_periods > 0 and growth_factor > 0:
        annualized_return = growth_factor ** (252 / num_periods) - 1.0
    else:
        annualized_return = 0.0

    daily_vol = float(daily_series.std(ddof=1)) if num_periods > 1 else 0.0
    annualized_vol = daily_vol * math.sqrt(252)
    sharpe = annualized_return / annualized_vol if annualized_vol > 0 else 0.0

    running_max = equity_series.cummax()
    drawdowns = (equity_series / running_max) - 1.0
    max_drawdown = float(drawdowns.min()) if not drawdowns.empty else 0.0

    return PerformanceMetrics(
        initial_capital=initial_capital,
        final_value=capital,
        total_return=total_return,
        annualized_return=annualized_return,
        annualized_volatility=annualized_vol,
        sharpe_ratio=sharpe,
        max_drawdown=max_drawdown,
        total_trades=trades,
    )


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
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


# ---------------------------------------------------------
# Mean-reversion pair analysis (primary engine)
# ---------------------------------------------------------
def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
) -> PairResult:
    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    df.columns = ["A", "B"]

    # For plotting in UI, keep user-friendly tickers
    display_prices = df.rename(columns={"A": ticker_a.upper(), "B": ticker_b.upper()})

    # Hedge ratio and spread
    beta = estimate_hedge_ratio(df["A"], df["B"])
    spread = df["A"] - beta * df["B"]

    # Cointegration / mean-reversion test
    pvalue = adf_test(spread)
    pair_ok = pvalue < 0.05

    mean_spread = spread.mean()
    std_spread = spread.std(ddof=1)

    last_spread = float(spread.iloc[-1])
    if std_spread > 0:
        last_z = float((last_spread - mean_spread) / std_spread)
        zscores = (spread - mean_spread) / std_spread
    else:
        last_z = 0.0
        zscores = pd.Series(0.0, index=spread.index)

    # Always compute backtest once, so performance table can show something
    performance = run_mean_reversion_backtest(
        price_frame=df,
        beta=beta,
        zscores=zscores,
        entry_z=entry_z,
        exit_z=exit_z,
    )

    # If cointegration fails → no mean-reversion strategy
    if not pair_ok:
        explanation = (
            f"Cointegration test failed (ADF p-value = {pvalue:.3f}). "
            "The price relationship does not show stable mean reversion. "
            "Mean-reversion pairs trading is not recommended for this pair."
        )

        return PairResult(
            pair_ok=False,
            mode="mean_reversion",
            signal="no_pairs_trade_cointegration_failed",
            explanation=explanation,
            hedge_ratio=beta,
            coint_pvalue=pvalue,
            last_spread=last_spread,
            last_zscore=last_z,
            spread_series=spread,
            prices=display_prices,
            spread_zscores=zscores,
            performance=performance,
            entry_z=entry_z,
            exit_z=exit_z,
        )

    # Cointegration passes → construct entry/exit zones and signal
    entry_upper = mean_spread + entry_z * std_spread
    entry_lower = mean_spread - entry_z * std_spread
    exit_low = mean_spread - exit_z * std_spread
    exit_high = mean_spread + exit_z * std_spread

    if last_z > entry_z:
        signal = "short_A_long_B"
        explanation = (
            f"Current z-score is {last_z:.2f}, above the entry threshold {entry_z:.2f}. "
            f"Suggested action: short {ticker_a} and long {ticker_b}. "
            f"Exit when the spread moves back into the neutral range between {exit_low:.4f} and {exit_high:.4f}."
        )
    elif last_z < -entry_z:
        signal = "long_A_short_B"
        explanation = (
            f"Current z-score is {last_z:.2f}, below the entry threshold -{entry_z:.2f}. "
            f"Suggested action: long {ticker_a} and short {ticker_b}. "
            f"Exit when the spread moves back into the neutral range between {exit_low:.4f} and {exit_high:.4f}."
        )
    elif abs(last_z) <= exit_z:
        signal = "close_positions"
        explanation = (
            f"Current z-score is {last_z:.2f}, inside the neutral exit band ±{exit_z:.2f}. "
            "Suggested action: close existing positions and lock in profits or losses."
        )
    else:
        signal = "no_trade"
        explanation = (
            f"Current z-score is {last_z:.2f}. "
            "The spread is not at an extreme level, so no new trade is recommended."
        )

    return PairResult(
        pair_ok=True,
        mode="mean_reversion",
        signal=signal,
        explanation=explanation,
        hedge_ratio=beta,
        coint_pvalue=pvalue,
        last_spread=last_spread,
        last_zscore=last_z,
        spread_series=spread,
        prices=display_prices,
        spread_zscores=zscores,
        performance=performance,
        entry_z=entry_z,
        exit_z=exit_z,
    )


# ---------------------------------------------------------
# Momentum-based analysis (used only when user chooses)
# ---------------------------------------------------------
def analyze_pair_momentum(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    high_pct: float = 0.9,
    low_pct: float = 0.1,
) -> PairResult:
    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    df.columns = ["A", "B"]
    display_prices = df.rename(columns={"A": ticker_a.upper(), "B": ticker_b.upper()})

    ratio = df["A"] / df["B"]

    cur = float(ratio.iloc[-1])
    high = float(ratio.quantile(high_pct))
    low = float(ratio.quantile(low_pct))
    stop_reference = float(ratio.quantile(0.5))

    if cur > high:
        signal = "momentum_buy_A_sell_B"
        explanation = (
            "The price ratio A/B is above the upper breakout level, indicating upward momentum in A "
            "relative to B. Suggested action: buy {a} and sell {b}. Suggested protective stop near ratio {stop:.4f}."
        ).format(a=ticker_a, b=ticker_b, stop=stop_reference)
    elif cur < low:
        signal = "momentum_buy_B_sell_A"
        explanation = (
            "The price ratio A/B is below the lower threshold, indicating relative strength in {b} "
            "and weakness in {a}. Suggested action: buy {b} and sell {a}. Suggested protective stop near ratio {stop:.4f}."
        ).format(a=ticker_a, b=ticker_b, stop=stop_reference)
    else:
        signal = "hold_no_signal"
        explanation = (
            "The price ratio A/B is within its typical range. No strong momentum signal is detected, "
            "so no trade is suggested at this time."
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
        prices=display_prices,
        spread_zscores=None,
        performance=None,
        entry_z=None,
        exit_z=None,
    )
