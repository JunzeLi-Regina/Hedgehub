from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple

import datetime as dt
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
from tiingo import TiingoClient
import yfinance as yf


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
    zscore_series: pd.Series
    threshold_series: pd.Series
    vix_series: pd.Series
    stats: Dict[str, Any]


_TIINGO_CLIENT: Optional[TiingoClient] = None
_TIINGO_KEY: Optional[str] = None


def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    start: Optional[str],
    end: Optional[str],
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    initial_capital: float = 100_000,
    shares_per_trade: int = 50,
    stop_loss_pct: float = 0.05,
    tiingo_api_key: Optional[str] = None,
) -> PairResult:
    if shares_per_trade <= 0:
        raise ValueError("Shares per trade must be positive.")
    if stop_loss_pct <= 0:
        raise ValueError("Stop loss percentage must be positive.")
    if exit_z <= 0:
        raise ValueError("Exit threshold must be greater than zero.")

    start_dt, end_dt = _resolve_dates(start, end)
    price_a, price_b = _fetch_price_series(
        ticker_a, ticker_b, start_dt, end_dt, tiingo_api_key
    )
    if price_a.empty or price_b.empty:
        raise ValueError("Unable to download overlapping price data for the pair.")

    hedge_ratio = _estimate_hedge_ratio(price_a, price_b)
    price_df = _prepare_dataframe(price_a, price_b)
    if price_df.empty or price_df["Z_Score"].dropna().empty:
        raise ValueError("Not enough data to compute rolling statistics for the pair.")

    stats = _compute_diagnostics(price_df, ticker_a, ticker_b)
    vix_series = _fetch_vix_series(price_df.index, start_dt, end_dt, tiingo_api_key)
    base_thresholds = _compute_thresholds(vix_series)
    threshold_series = base_thresholds * (entry_z / 2.0)
    price_df["VIX"] = vix_series
    price_df["EntryThreshold"] = threshold_series
    price_df["ExitBand"] = exit_z

    trade_data = price_df.dropna(subset=["Z_Score"]).copy()
    if trade_data.empty:
        raise ValueError("Insufficient data after rolling calculations for trading.")

    max_holding = (
        int(1.5 * stats["half_life"])
        if np.isfinite(stats["half_life"]) and stats["half_life"] > 0
        else 20
    )

    blotter, ledger = _run_trading_loop(
        trade_data,
        ticker_a,
        ticker_b,
        shares_per_trade,
        stop_loss_pct,
        initial_capital,
        max_holding,
    )
    performance = _compute_performance_metrics(ledger, blotter, initial_capital)

    spread_series = price_df["Log_Spread"].dropna()
    zscore_series = price_df["Z_Score"].dropna()
    last_spread = float(spread_series.iloc[-1])
    last_z = float(zscore_series.iloc[-1])

    entry_band = float(threshold_series.iloc[-1])
    if last_z >= entry_band:
        signal = f"short_{ticker_a}_long_{ticker_b}"
    elif last_z <= -entry_band:
        signal = f"long_{ticker_a}_short_{ticker_b}"
    else:
        signal = "no_trade"

    coint_pvalue = stats["coint_pvalue"]
    pair_ok = coint_pvalue < 0.05
    explanation = _build_explanation(
        ticker_a,
        ticker_b,
        pair_ok,
        coint_pvalue,
        last_z,
        entry_band,
        signal,
        stats,
    )

    summary = _build_summary(ticker_a, ticker_b, stats, performance, signal)

    price_history = pd.DataFrame(
        {
            ticker_a: price_df["Price_A"],
            ticker_b: price_df["Price_B"],
        }
    )

    return PairResult(
        pair_ok=pair_ok,
        coint_pvalue=coint_pvalue,
        hedge_ratio=hedge_ratio,
        last_spread=last_spread,
        last_zscore=last_z,
        signal=signal,
        explanation=explanation,
        spread_series=spread_series,
        summary=summary,
        performance=performance,
        blotter=blotter,
        ledger=ledger,
        price_history=price_history,
        entry_z=entry_z,
        exit_z=exit_z,
        initial_capital=initial_capital,
        shares_per_trade=shares_per_trade,
        stop_loss_pct=stop_loss_pct,
        zscore_series=zscore_series,
        threshold_series=threshold_series,
        vix_series=vix_series,
        stats=stats,
    )


def _resolve_dates(
    start: Optional[str], end: Optional[str]
) -> Tuple[dt.datetime, dt.datetime]:
    start_dt = pd.to_datetime(start) if start else None
    end_dt = pd.to_datetime(end) if end else None

    if not start_dt or not end_dt or start_dt >= end_dt:
        end_dt = dt.datetime.utcnow()
        start_dt = end_dt - dt.timedelta(days=365)

    return start_dt.to_pydatetime(), end_dt.to_pydatetime()


def _get_tiingo_client(api_key: Optional[str]) -> TiingoClient:
    key = api_key or os.getenv("TIINGO_API_KEY")
    if not key:
        raise ValueError("Tiingo API key is required for this analysis.")

    global _TIINGO_CLIENT, _TIINGO_KEY
    if _TIINGO_CLIENT is None or key != _TIINGO_KEY:
        _TIINGO_CLIENT = TiingoClient({"api_key": key})
        _TIINGO_KEY = key
    return _TIINGO_CLIENT


def _fetch_tiingo_series(
    ticker: str, start_dt: dt.datetime, end_dt: dt.datetime, api_key: Optional[str]
) -> pd.Series:
    client = _get_tiingo_client(api_key)
    df = client.get_dataframe(
        ticker,
        startDate=start_dt.strftime("%Y-%m-%d"),
        endDate=end_dt.strftime("%Y-%m-%d"),
        frequency="daily",
    )
    if df is None or df.empty:
        raise ValueError(f"Tiingo returned no data for {ticker}.")

    column = "adjClose" if "adjClose" in df.columns else "close"
    series = df[column].dropna()
    series.index = pd.to_datetime(series.index)
    return series.sort_index()


def _fetch_price_series(
    ticker_a: str,
    ticker_b: str,
    start_dt: dt.datetime,
    end_dt: dt.datetime,
    api_key: Optional[str],
) -> Tuple[pd.Series, pd.Series]:
    if api_key or os.getenv("TIINGO_API_KEY"):
        try:
            series_a = _fetch_tiingo_series(ticker_a, start_dt, end_dt, api_key)
            series_b = _fetch_tiingo_series(ticker_b, start_dt, end_dt, api_key)
        except Exception as exc:
            raise ValueError(f"Tiingo data fetch failed: {exc}") from exc
    else:
        data_a = yf.download(
            ticker_a,
            start=start_dt.strftime("%Y-%m-%d"),
            end=end_dt.strftime("%Y-%m-%d"),
            progress=False,
            auto_adjust=False,
        )
        data_b = yf.download(
            ticker_b,
            start=start_dt.strftime("%Y-%m-%d"),
            end=end_dt.strftime("%Y-%m-%d"),
            progress=False,
            auto_adjust=False,
        )
        if data_a.empty or data_b.empty:
            raise ValueError("Failed to download data via yfinance.")
        series_a = data_a["Adj Close"].dropna()
        series_b = data_b["Adj Close"].dropna()

    aligned = pd.concat([series_a, series_b], axis=1, join="inner").dropna()
    aligned.columns = ["Price_A", "Price_B"]
    return aligned["Price_A"], aligned["Price_B"]


def _estimate_hedge_ratio(prices_a: pd.Series, prices_b: pd.Series) -> float:
    x = sm.add_constant(prices_b.values)
    y = prices_a.values
    model = sm.OLS(y, x).fit()
    return float(model.params[1])


def _prepare_dataframe(price_a: pd.Series, price_b: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame({"Price_A": price_a, "Price_B": price_b}).dropna()
    df.index.name = "Date"
    df = df[df["Price_A"] > 0]
    df = df[df["Price_B"] > 0]

    df["Log_Spread"] = np.log(df["Price_A"]) - np.log(df["Price_B"])
    df["Roll_Mean"] = df["Log_Spread"].rolling(window=20).mean()
    df["Roll_Std"] = df["Log_Spread"].rolling(window=20).std()
    df["Z_Score"] = (df["Log_Spread"] - df["Roll_Mean"]) / df["Roll_Std"]
    return df


def _compute_diagnostics(
    df: pd.DataFrame, ticker_a: str, ticker_b: str
) -> Dict[str, Any]:
    correlation = df["Price_A"].corr(df["Price_B"])
    score, pvalue, _ = coint(df["Price_A"].astype(float), df["Price_B"].astype(float))

    adf_result = adfuller(df["Log_Spread"].dropna())
    half_life = _calculate_half_life(df["Log_Spread"])

    return {
        "correlation": float(correlation),
        "coint_stat": float(score),
        "coint_pvalue": float(pvalue),
        "adf_stat": float(adf_result[0]),
        "adf_pvalue": float(adf_result[1]),
        "half_life": float(half_life) if np.isfinite(half_life) else np.inf,
        "tickers": (ticker_a, ticker_b),
    }


def _calculate_half_life(spread: pd.Series) -> float:
    spread = spread.dropna()
    if spread.empty:
        return np.inf

    spread_lag = spread.shift(1).dropna()
    spread_diff = (spread - spread_lag).dropna()
    spread_lag = sm.add_constant(spread_lag.loc[spread_diff.index])

    model = sm.OLS(spread_diff, spread_lag).fit()
    rho = model.params.iloc[1]
    if rho >= 0:
        return np.inf
    return -np.log(2) / rho


def _fetch_vix_series(
    index: pd.Index,
    start_dt: dt.datetime,
    end_dt: dt.datetime,
    api_key: Optional[str],
) -> pd.Series:
    try:
        series = _fetch_tiingo_series("VIX", start_dt, end_dt, api_key)
    except Exception:
        return pd.Series(15.0, index=index)

    series = series.reindex(index, method="ffill").fillna(method="bfill")
    if series.isna().all():
        series[:] = 15.0
    return series


def _compute_thresholds(vix_series: pd.Series) -> pd.Series:
    conditions = [
        vix_series < 20,
        (vix_series >= 20) & (vix_series < 25),
        (vix_series >= 25) & (vix_series < 30),
        vix_series >= 30,
    ]
    choices = [2.0, 2.25, 2.5, 3.0]
    thresholds = np.select(conditions, choices, default=2.0)
    return pd.Series(thresholds, index=vix_series.index)


def _run_trading_loop(
    df: pd.DataFrame,
    ticker_a: str,
    ticker_b: str,
    shares_per_trade: int,
    stop_loss_pct: float,
    initial_capital: float,
    max_holding_days: int,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    blotter_rows = []
    ledger_rows = []

    cash = initial_capital
    position = 0
    entry_price_a = entry_price_b = 0.0
    entry_date: Optional[pd.Timestamp] = None
    entry_threshold = 0.0

    last_date = df.index[-1]

    for current_date, row in df.iterrows():
        price_a = float(row["Price_A"])
        price_b = float(row["Price_B"])
        z_score = float(row["Z_Score"])
        threshold = float(row["EntryThreshold"])
        exit_band = float(row["ExitBand"])
        vix_value = float(row["VIX"]) if "VIX" in row else np.nan

        # Exit logic
        exit_reason = None
        if position != 0 and entry_date is not None:
            hold_days = (current_date - entry_date).days
            reversion_exit = abs(z_score) <= exit_band
            time_exit = hold_days > max_holding_days

            if entry_price_a > 0 and entry_price_b > 0:
                rel_a = price_a / entry_price_a
                rel_b = price_b / entry_price_b
                stop_exit = abs((rel_a - rel_b) / 2.0) > stop_loss_pct
            else:
                stop_exit = False

            if reversion_exit:
                exit_reason = "Mean Reversion"
            elif stop_exit:
                exit_reason = "Stop Loss"
            elif time_exit:
                exit_reason = "Time Stop"

            if exit_reason:
                qty = abs(position)
                if position > 0:
                    pnl_a = qty * (price_a - entry_price_a)
                    pnl_b = qty * (entry_price_b - price_b)
                    direction = f"Long {ticker_a} / Short {ticker_b}"
                    pos_a = "LONG"
                    pos_b = "SHORT"
                else:
                    pnl_a = qty * (entry_price_a - price_a)
                    pnl_b = qty * (price_b - entry_price_b)
                    direction = f"Short {ticker_a} / Long {ticker_b}"
                    pos_a = "SHORT"
                    pos_b = "LONG"

                total_pnl = pnl_a + pnl_b
                cash += total_pnl

                blotter_rows.append(
                    {
                        "Entry Date": entry_date,
                        "Exit Date": current_date,
                        "Qty": qty,
                        "Direction": direction,
                        "Position A": pos_a,
                        "Position B": pos_b,
                        "Entry Price A": entry_price_a,
                        "Entry Price B": entry_price_b,
                        "Exit Price A": price_a,
                        "Exit Price B": price_b,
                        "PnL A ($)": round(pnl_a, 2),
                        "PnL B ($)": round(pnl_b, 2),
                        "PnL ($)": round(total_pnl, 2),
                        "Reason": exit_reason,
                    }
                )

                position = 0
                entry_price_a = entry_price_b = 0.0
                entry_date = None
                entry_threshold = 0.0

        # Entry logic
        if position == 0 and not np.isnan(z_score) and not np.isnan(threshold):
            if z_score >= threshold:
                position = -shares_per_trade
                entry_price_a = price_a
                entry_price_b = price_b
                entry_date = current_date
                entry_threshold = threshold
            elif z_score <= -threshold:
                position = shares_per_trade
                entry_price_a = price_a
                entry_price_b = price_b
                entry_date = current_date
                entry_threshold = threshold

        # Mark existing cash if no trade occurred
        if not blotter_rows and not ledger_rows:
            cash = initial_capital

        # Market value of open position
        if position > 0:
            value_a = position * price_a
            value_b = -position * price_b
        elif position < 0:
            value_a = position * price_a
            value_b = -position * price_b
        else:
            value_a = value_b = 0.0

        equity = cash + value_a + value_b

        ledger_rows.append(
            {
                "Date": current_date,
                "Position": position,
                "Cash": round(cash, 2),
                "Equity": round(equity, 2),
                "Price A": price_a,
                "Price B": price_b,
                "Z-Score": z_score,
                "Threshold": threshold,
                "VIX": vix_value,
            }
        )

    # Force-close at the end if still holding
    if position != 0 and entry_date is not None:
        last_row = df.loc[last_date]
        price_a = float(last_row["Price_A"])
        price_b = float(last_row["Price_B"])
        qty = abs(position)
        if position > 0:
            pnl_a = qty * (price_a - entry_price_a)
            pnl_b = qty * (entry_price_b - price_b)
            direction = f"Long {ticker_a} / Short {ticker_b}"
            pos_a = "LONG"
            pos_b = "SHORT"
        else:
            pnl_a = qty * (entry_price_a - price_a)
            pnl_b = qty * (price_b - entry_price_b)
            direction = f"Short {ticker_a} / Long {ticker_b}"
            pos_a = "SHORT"
            pos_b = "LONG"

        total_pnl = pnl_a + pnl_b
        cash += total_pnl
        blotter_rows.append(
            {
                "Entry Date": entry_date,
                "Exit Date": last_date,
                "Qty": qty,
                "Direction": direction,
                "Position A": pos_a,
                "Position B": pos_b,
                "Entry Price A": entry_price_a,
                "Entry Price B": entry_price_b,
                "Exit Price A": price_a,
                "Exit Price B": price_b,
                "PnL A ($)": round(pnl_a, 2),
                "PnL B ($)": round(pnl_b, 2),
                "PnL ($)": round(total_pnl, 2),
                "Reason": "End of Sample",
            }
        )

    blotter_df = pd.DataFrame(blotter_rows)
    ledger_df = pd.DataFrame(ledger_rows)
    return blotter_df, ledger_df


def _compute_performance_metrics(
    ledger: pd.DataFrame, blotter: pd.DataFrame, initial_capital: float
) -> Dict[str, Any]:
    if ledger.empty:
        return {
            "Total Return (%)": 0.0,
            "Annualized Return (%)": 0.0,
            "Annualized Volatility (%)": 0.0,
            "Sharpe Ratio": 0.0,
            "Max Drawdown (%)": 0.0,
            "Trades": 0,
            "Win Rate (%)": 0.0,
            "Stop-outs": 0,
            "Best Trade ($)": 0.0,
            "Worst Trade ($)": 0.0,
            "Final Equity ($)": initial_capital,
        }

    equity = ledger["Equity"]
    total_return = (equity.iloc[-1] / equity.iloc[0]) - 1
    daily_returns = equity.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0.0)
    avg_daily = daily_returns.mean()
    std_daily = daily_returns.std(ddof=1)
    annualized_return = ((1 + avg_daily) ** 252) - 1 if len(ledger) > 1 else 0.0
    annualized_vol = std_daily * np.sqrt(252) if std_daily > 0 else 0.0
    sharpe = (avg_daily / std_daily) * np.sqrt(252) if std_daily > 0 else 0.0

    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max.replace(0, np.nan)
    max_drawdown = drawdown.min() if not drawdown.isnull().all() else 0.0
    max_dd_pct = abs(float(max_drawdown)) * 100 if pd.notna(max_drawdown) else 0.0

    if blotter.empty:
        win_rate = 0.0
        best_trade = 0.0
        worst_trade = 0.0
        stopouts = 0
    else:
        trade_pnls = blotter["PnL ($)"]
        wins = (trade_pnls > 0).sum()
        win_rate = wins / len(trade_pnls) if len(trade_pnls) else 0.0
        best_trade = trade_pnls.max()
        worst_trade = trade_pnls.min()
        stopouts = int((blotter["Reason"] == "Stop Loss").sum())

    return {
        "Total Return (%)": round(total_return * 100, 2),
        "Annualized Return (%)": round(annualized_return * 100, 2),
        "Annualized Volatility (%)": round(annualized_vol * 100, 2),
        "Sharpe Ratio": round(float(sharpe), 2),
        "Max Drawdown (%)": round(max_dd_pct, 2),
        "Trades": int(len(blotter)),
        "Win Rate (%)": round(win_rate * 100, 2),
        "Stop-outs": int(stopouts),
        "Best Trade ($)": round(float(best_trade), 2),
        "Worst Trade ($)": round(float(worst_trade), 2),
        "Final Equity ($)": round(float(equity.iloc[-1]), 2),
    }


def _build_explanation(
    ticker_a: str,
    ticker_b: str,
    pair_ok: bool,
    coint_pvalue: float,
    last_z: float,
    entry_band: float,
    signal: str,
    stats: Dict[str, Any],
) -> str:
    if not pair_ok:
        return (
            f"The pair {ticker_a}/{ticker_b} fails the cointegration test "
            f"(p-value={coint_pvalue:.3f}). Spread is not mean-reverting."
        )

    if signal.startswith("short"):
        action = f"SHORT {ticker_a} / LONG {ticker_b}"
    elif signal.startswith("long"):
        action = f"LONG {ticker_a} / SHORT {ticker_b}"
    else:
        action = "No immediate trade"

    return (
        f"The pair {ticker_a}/{ticker_b} is cointegrated (p-value={coint_pvalue:.3f}). "
        f"Latest z-score = {last_z:.2f} with entry band {entry_band:.2f}. "
        f"Suggested stance: {action}. Correlation={stats['correlation']:.2f}, "
        f"ADF p-value={stats['adf_pvalue']:.4f}, half-life="
        f"{'∞' if not np.isfinite(stats['half_life']) else f'{stats['half_life']:.1f} days'}."
    )


def _build_summary(
    ticker_a: str,
    ticker_b: str,
    stats: Dict[str, Any],
    performance: Dict[str, Any],
    signal: str,
) -> str:
    summary_lines = [
        f"Pair: {ticker_a} vs {ticker_b}",
        (
            f"Correlation {stats['correlation']:.2f} | Cointegration p={stats['coint_pvalue']:.4f} "
            f"| ADF p={stats['adf_pvalue']:.4f}"
        ),
        (
            "Half-life: "
            + (
                "∞"
                if not np.isfinite(stats["half_life"])
                else f"{stats['half_life']:.1f} days"
            )
        ),
        (
            f"Trades: {performance['Trades']} | Win rate: {performance['Win Rate (%)']:.1f}% | "
            f"Stop-outs: {performance['Stop-outs']}"
        ),
        (
            f"Return: {performance['Total Return (%)']:.2f}% | Sharpe: {performance['Sharpe Ratio']:.2f} | "
            f"Max DD: {performance['Max Drawdown (%)']:.2f}%"
        ),
        f"Final equity: ${performance['Final Equity ($)']:,.0f} | Current signal: {signal}",
    ]
    return "\n".join(summary_lines)
