from dataclasses import dataclass
from typing import Dict, Any
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
    performance: Dict[str, Any]


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


def simulate_pairs_strategy(
    spread: pd.Series,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    initial_capital: float = 1_000_000.0,
    trade_size: int = 100,
) -> Dict[str, Any]:
    if spread.empty:
        return {
            "initial_capital": initial_capital,
            "final_value": initial_capital,
            "total_return": 0.0,
            "annualized_return": 0.0,
            "annualized_volatility": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "total_trades": 0,
        }

    mean_spread = spread.mean()
    std_spread = spread.std(ddof=1)
    if std_spread == 0:
        z_scores = pd.Series(0.0, index=spread.index)
    else:
        z_scores = (spread - mean_spread) / std_spread

    position = 0  # 1 = long spread, -1 = short spread
    equity = initial_capital
    equity_curve = [equity]
    total_trades = 0

    for i in range(1, len(spread)):
        z_signal = float(z_scores.iloc[i - 1])

        if position == 0:
            if z_signal > entry_z:
                position = -1
                total_trades += 1
            elif z_signal < -entry_z:
                position = 1
                total_trades += 1
        else:
            if abs(z_signal) <= exit_z:
                position = 0

        spread_change = float(spread.iloc[i] - spread.iloc[i - 1])
        pnl = position * spread_change * trade_size
        equity += pnl
        equity_curve.append(equity)

    equity_series = pd.Series(equity_curve, index=spread.index)
    total_return = (equity_series.iloc[-1] / equity_series.iloc[0]) - 1

    num_days = max(1, len(equity_series) - 1)
    if (1 + total_return) > 0:
        annualized_return = (1 + total_return) ** (252 / num_days) - 1
    else:
        annualized_return = -1.0

    daily_returns = equity_series.pct_change().dropna()
    if len(daily_returns) > 1:
        annualized_volatility = float(daily_returns.std(ddof=1) * np.sqrt(252))
    elif len(daily_returns) == 1:
        annualized_volatility = float(abs(daily_returns.iloc[0]) * np.sqrt(252))
    else:
        annualized_volatility = 0.0

    sharpe_ratio = (
        annualized_return / annualized_volatility if annualized_volatility > 0 else 0.0
    )

    running_max = equity_series.cummax()
    drawdowns = equity_series / running_max - 1
    max_drawdown = float(drawdowns.min()) if not drawdowns.empty else 0.0

    return {
        "initial_capital": float(initial_capital),
        "final_value": float(equity_series.iloc[-1]),
        "total_return": float(total_return),
        "annualized_return": float(annualized_return),
        "annualized_volatility": float(annualized_volatility),
        "sharpe_ratio": float(sharpe_ratio),
        "max_drawdown": max_drawdown,
        "total_trades": int(total_trades),
    }


def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    start: str,
    end: str,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    initial_capital: float = 1_000_000.0,
    trade_size: int = 100,
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

    performance = simulate_pairs_strategy(
        spread=spread,
        entry_z=entry_z,
        exit_z=exit_z,
        initial_capital=initial_capital,
        trade_size=trade_size,
    )

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
        performance=performance,
    )
