from dataclasses import dataclass
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yfinance as yf
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
    summary: str
    performance: Dict[str, Any]
    blotter: pd.DataFrame
    ledger: pd.DataFrame
    price_history: pd.DataFrame
    entry_z: float
    exit_z: float
    initial_capital: float
    shares_per_trade: int
    stop_loss_pct: float


def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
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
    exit_z: float = 0.5,
    initial_capital: float = 100_000,
    shares_per_trade: int = 50,
    stop_loss_pct: float = 0.05,
) -> PairResult:
    if exit_z >= entry_z:
        raise ValueError("Exit threshold must be smaller than entry threshold.")
    if shares_per_trade <= 0:
        raise ValueError("Shares per trade must be positive.")
    if stop_loss_pct <= 0:
        raise ValueError("Stop loss percentage must be positive.")

    # ---- Download prices ----
    prices_a = download_prices(ticker_a, start, end)
    prices_b = download_prices(ticker_b, start, end)

    # Align dates
    df = pd.concat([prices_a, prices_b], axis=1).dropna()
    if df.empty:
        raise ValueError("No overlapping price history for the selected tickers.")
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

    backtest = backtest_pair(
        prices_a=prices_a,
        prices_b=prices_b,
        spread=spread,
        beta=beta,
        entry_z=entry_z,
        exit_z=exit_z,
        initial_capital=initial_capital,
        shares_per_trade=shares_per_trade,
        stop_loss_pct=stop_loss_pct,
    )

    summary = build_summary(
        ticker_a=ticker_a,
        ticker_b=ticker_b,
        pair_ok=pair_ok,
        pvalue=pvalue,
        beta=beta,
        performance=backtest["performance"],
        signal=signal,
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
        summary=summary,
        performance=backtest["performance"],
        blotter=backtest["blotter"],
        ledger=backtest["ledger"],
        price_history=df,
        entry_z=entry_z,
        exit_z=exit_z,
        initial_capital=initial_capital,
        shares_per_trade=int(shares_per_trade),
        stop_loss_pct=stop_loss_pct,
    )


def backtest_pair(
    prices_a: pd.Series,
    prices_b: pd.Series,
    spread: pd.Series,
    beta: float,
    entry_z: float,
    exit_z: float,
    initial_capital: float,
    shares_per_trade: int,
    stop_loss_pct: float,
) -> Dict[str, Any]:
    shares = max(1, int(shares_per_trade))
    z_scores = compute_zscore(spread)
    ledger_rows = []
    blotter_rows = []
    position = 0  # 1 = long spread, -1 = short spread
    trade_pnl = 0.0
    cumulative_pnl = 0.0
    entry_info: Optional[Dict[str, Any]] = None
    stop_threshold = stop_loss_pct * initial_capital
    dates = spread.index

    for i, date in enumerate(dates):
        spread_value = float(spread.iat[i])
        z_value = float(z_scores.iat[i])
        price_a = float(prices_a.iat[i])
        price_b = float(prices_b.iat[i])

        if i == 0:
            daily_pnl = 0.0
        else:
            spread_change = float(spread_value - spread.iat[i - 1])
            daily_pnl = position * spread_change * shares
            cumulative_pnl += daily_pnl
            if position != 0:
                trade_pnl += daily_pnl

        exit_reason: Optional[str] = None
        if position != 0 and i > 0:
            if abs(z_value) <= exit_z:
                exit_reason = "Mean Reversion"
            elif trade_pnl <= -stop_threshold:
                exit_reason = "Stop Loss"

            if exit_reason and entry_info:
                blotter_rows.append(
                    {
                        "Entry Date": entry_info["entry_date"],
                        "Exit Date": date,
                        "Direction": entry_info["direction"],
                        "Entry Spread": entry_info["entry_spread"],
                        "Exit Spread": spread_value,
                        "Entry Z": entry_info["entry_z"],
                        "Exit Z": z_value,
                        "Entry Price A": entry_info["price_a"],
                        "Entry Price B": entry_info["price_b"],
                        "Exit Price A": price_a,
                        "Exit Price B": price_b,
                        "PnL ($)": round(trade_pnl, 2),
                        "Reason": exit_reason,
                    }
                )
                position = 0
                trade_pnl = 0.0
                entry_info = None

        if position == 0:
            if z_value >= entry_z:
                position = -1
                entry_info = {
                    "entry_date": date,
                    "entry_spread": spread_value,
                    "entry_z": z_value,
                    "direction": "Short Spread",
                    "price_a": price_a,
                    "price_b": price_b,
                }
            elif z_value <= -entry_z:
                position = 1
                entry_info = {
                    "entry_date": date,
                    "entry_spread": spread_value,
                    "entry_z": z_value,
                    "direction": "Long Spread",
                    "price_a": price_a,
                    "price_b": price_b,
                }

        ledger_rows.append(
            {
                "Date": date,
                "Position": position,
                "Spread": spread_value,
                "Z-Score": z_value,
                "Daily PnL": round(daily_pnl, 4),
                "Cumulative PnL": round(cumulative_pnl, 4),
                "Equity": round(initial_capital + cumulative_pnl, 4),
            }
        )

    # Force-close any open trade at the last observation
    if position != 0 and entry_info is not None:
        blotter_rows.append(
            {
                "Entry Date": entry_info["entry_date"],
                "Exit Date": dates[-1],
                "Direction": entry_info["direction"],
                "Entry Spread": entry_info["entry_spread"],
                "Exit Spread": float(spread.iat[-1]),
                "Entry Z": entry_info["entry_z"],
                "Exit Z": float(z_scores.iat[-1]),
                "Entry Price A": entry_info["price_a"],
                "Entry Price B": entry_info["price_b"],
                "Exit Price A": float(prices_a.iat[-1]),
                "Exit Price B": float(prices_b.iat[-1]),
                "PnL ($)": round(trade_pnl, 2),
                "Reason": "End of Sample",
            }
        )

    ledger_df = pd.DataFrame(ledger_rows)
    blotter_df = pd.DataFrame(blotter_rows)
    performance = compute_performance_metrics(ledger_df, blotter_df, initial_capital)

    return {
        "ledger": ledger_df,
        "blotter": blotter_df,
        "performance": performance,
    }


def compute_zscore(spread: pd.Series) -> pd.Series:
    std_spread = spread.std(ddof=1)
    if std_spread == 0 or np.isnan(std_spread):
        return pd.Series(np.zeros(len(spread)), index=spread.index)
    mean_spread = spread.mean()
    return (spread - mean_spread) / std_spread


def compute_performance_metrics(
    ledger: pd.DataFrame, blotter: pd.DataFrame, initial_capital: float
) -> Dict[str, Any]:
    if ledger.empty:
        return {
            "Total Return (%)": 0.0,
            "Annualized Return (%)": 0.0,
            "Sharpe Ratio": 0.0,
            "Max Drawdown (%)": 0.0,
            "Trades": 0,
            "Win Rate (%)": 0.0,
            "Avg Trade ($)": 0.0,
            "Best Trade ($)": 0.0,
            "Worst Trade ($)": 0.0,
            "Stop-outs": 0,
            "Final Equity ($)": initial_capital,
        }

    equity = ledger["Equity"]
    total_return = (equity.iloc[-1] / equity.iloc[0]) - 1 if len(equity) > 0 else 0.0

    daily_returns = (
        equity.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0.0)
    )
    avg_daily = daily_returns.mean()
    std_daily = daily_returns.std(ddof=1)
    annualized_return = (1 + avg_daily) ** 252 - 1 if len(ledger) > 1 else 0.0
    sharpe = (avg_daily / std_daily) * np.sqrt(252) if std_daily > 0 else 0.0

    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max.replace(0, np.nan)
    max_drawdown = drawdown.min() if not drawdown.isnull().all() else 0.0
    if pd.isna(max_drawdown):
        max_dd_pct = 0.0
    else:
        max_dd_pct = abs(float(max_drawdown)) * 100

    if blotter.empty:
        win_rate = 0.0
        avg_trade = 0.0
        best_trade = 0.0
        worst_trade = 0.0
        stopouts = 0
    else:
        trade_pnls = blotter["PnL ($)"]
        wins = (trade_pnls > 0).sum()
        win_rate = wins / len(trade_pnls) if len(trade_pnls) > 0 else 0.0
        avg_trade = trade_pnls.mean()
        best_trade = trade_pnls.max()
        worst_trade = trade_pnls.min()
        stopouts = int((blotter["Reason"] == "Stop Loss").sum())

    return {
        "Total Return (%)": round(total_return * 100, 2),
        "Annualized Return (%)": round(annualized_return * 100, 2),
        "Sharpe Ratio": round(float(sharpe), 2),
        "Max Drawdown (%)": round(max_dd_pct, 2),
        "Trades": int(len(blotter)),
        "Win Rate (%)": round(win_rate * 100, 2),
        "Avg Trade ($)": round(float(avg_trade), 2),
        "Best Trade ($)": round(float(best_trade), 2),
        "Worst Trade ($)": round(float(worst_trade), 2),
        "Stop-outs": int(stopouts),
        "Final Equity ($)": round(float(equity.iloc[-1]), 2),
    }


def build_summary(
    ticker_a: str,
    ticker_b: str,
    pair_ok: bool,
    pvalue: float,
    beta: float,
    performance: Dict[str, Any],
    signal: str,
) -> str:
    status = "PASSED" if pair_ok else "FAILED"
    summary_lines = [
        f"Pair: {ticker_a}/{ticker_b}",
        f"Cointegration p-value: {pvalue:.4f} ({status}) • Hedge ratio β = {beta:.3f}",
        (
            f"Trades executed: {performance['Trades']} • Win rate: "
            f"{performance['Win Rate (%)']:.1f}% • Stop-outs: {performance['Stop-outs']}"
        ),
        (
            f"Total return: {performance['Total Return (%)']:.2f}% • Sharpe: "
            f"{performance['Sharpe Ratio']:.2f} • Max drawdown: "
            f"{performance['Max Drawdown (%)']:.2f}%"
        ),
        f"Current signal: {signal}",
    ]
    return "\n".join(summary_lines)
