from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px

from strategy_engine import analyze_pair, generate_strategy_plan, StrategyPlan

NAVBAR_ID = "main_nav"


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


# ---------------------------------------------------------
# UI PANELS
# ---------------------------------------------------------
def make_home_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Home",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    # ---------------- Header ----------------
                    ui.h1("Welcome to HedgeHub", class_="text-center", style="color:#00E6A8;"),
                    ui.h4(
                        "Smart Pairs Trading Analysis Platform",
                        class_="text-center",
                        style="color:#00E6A8; opacity:0.85;",
                    ),
                    ui.hr(),

                    # ---------------- Video ----------------
                    ui.div(
                        ui.tags.iframe(
                            src="https://www.youtube.com/embed/xeG0kFzV2WM",
                            width="100%",
                            height="380px",
                            style="border:none; border-radius:15px;",
                        ),
                        style="max-width:900px; margin:0 auto;",
                    ),

                    ui.hr(),

                    # ---------------- Feature Cards (MORE TEXT VERSION) ----------------
                    ui.div(
                        {
                            "style": """
                                display:flex;
                                justify-content:center;
                                gap:25px;
                                margin-top:20px;
                                padding-bottom:10px;
                            """
                        },

                        # ------- Card 1 -------
                        ui.card(
                            ui.h4("Analyze Pairs", style="color:#00E6A8; text-align:center;"),

                            ui.p(
                                "Identify statistically related pairs and evaluate long-term stability.",
                                style="color:#CCCCCC; text-align:center; font-size:14px;"
                            ),

                            ui.tags.ul(
                                ui.tags.li("Run cointegration and correlation tests"),
                                ui.tags.li("Visualize price spreads & divergence patterns"),
                                ui.tags.li("Detect pairs suitable for mean-reversion"),
                                style="color:#CCCCCC; font-size:14px;"
                            ),
                            style="padding:18px; width:300px; min-height:230px;"
                        ),

                        # ------- Card 2 -------
                        ui.card(
                            ui.h4("Generate Strategy", style="color:#00E6A8; text-align:center;"),

                            ui.p(
                                "Build a market-neutral long/short strategy from spread signals.",
                                style="color:#CCCCCC; text-align:center; font-size:14px;"
                            ),

                            ui.tags.ul(
                                ui.tags.li("Compute real-time Z-scores"),
                                ui.tags.li("Set entry/exit thresholds"),
                                ui.tags.li("Generate actionable long/short signals"),
                                style="color:#CCCCCC; font-size:14px;"
                            ),
                            style="padding:18px; width:300px; min-height:230px;"
                        ),

                        # ------- Card 3 -------
                        ui.card(
                            ui.h4("Market Insights", style="color:#00E6A8; text-align:center;"),

                            ui.p(
                                "Monitor external catalysts that may affect spread movements.",
                                style="color:#CCCCCC; text-align:center; font-size:14px;"
                            ),

                            ui.tags.ul(
                                ui.tags.li("Track news, sentiment & macro events"),
                                ui.tags.li("Identify narrative shifts in the market"),
                                ui.tags.li("Spot risk factors behind divergence"),
                                style="color:#CCCCCC; font-size:14px;"
                            ),
                            style="padding:18px; width:300px; min-height:230px;"
                        ),
                    ),

                    ui.hr(),

                    # ---------------- How Pairs Trading Works ----------------
                    ui.h3("How Pairs Trading Works", style="color:#00E6A8; text-align:center; margin-top:10px;"),

                    ui.p(
                        "Pairs trading identifies two assets that typically move together. "
                        "When their price relationship temporarily diverges, a market-neutral opportunity appears.",
                        style="text-align:center; color:#CCCCCC; max-width:850px; margin:0 auto 15px auto;"
                    ),

                    ui.tags.ol(
                        {
                            "style": """
                                max-width: 750px;
                                margin: 0 auto;
                                color: #CCCCCC;
                                line-height: 1.65;
                                font-size: 16px;
                                padding-left: 15px;
                            """
                        },
                        ui.tags.li("Select a pair of assets with correlated movements."),
                        ui.tags.li("Measure their spread to understand divergence."),
                        ui.tags.li("Convert the spread into a Z-score to standardize extremity."),
                        ui.tags.li("Generate long/short signals when thresholds are breached (e.g., ±2)."),
                        ui.tags.li("Exit positions when the spread reverts to the mean."),
                    ),

                    ui.p(
                        "Because the logic is statistical, this workflow applies to equities, ETFs, or any assets with sufficiently stable long-term relationships.",
                        style="text-align:center; color:#CCCCCC; max-width:850px; margin:15px auto;"
                    ),

                    ui.hr(),

                    # ---------------- CTA Button ----------------
                    ui.input_action_button(
                        "go_to_analysis",
                        "Start Analysis",
                        class_="btn btn-success btn-lg d-block mx-auto shadow-green",
                    ),
                ),
            )
        ),
    )



def make_pair_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Pair Analysis",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h3("Pair Analysis", style="color:#00E6A8;"),
                    ui.p("Input your stock pair and run a basic pair test.", style="color:#CCCCCC;"),
                    ui.input_text("stock_a", "Stock A (e.g., AAPL)", ""),
                    ui.input_text("stock_b", "Stock B (e.g., MSFT)", ""),
                    ui.input_date_range("date_range", "Date Range"),
                    ui.input_numeric(
                        "initial_capital",
                        "Initial Capital ($)",
                        1_000_000,
                        min=10_000,
                        step=10_000,
                    ),
                    ui.input_numeric(
                        "shares_per_trade",
                        "Shares per Trade",
                        100,
                        min=1,
                        step=10,
                    ),
                    ui.input_action_button(
                        "run_analysis",
                        "Run Pair Test",
                        class_="btn btn-outline-success",
                    ),
                    ui.hr(),
                    ui.h4("Results", style="color:#00E6A8;"),
                    ui.output_text_verbatim("pair_test_result"),
                    ui.hr(),
                    ui.h4("Performance Metrics", style="color:#00E6A8;"),
                    ui.p(
                        "These metrics summarize key portfolio stats for the selected pair. The table refreshes after each analysis.",
                        style="color:#CCCCCC;",
                    ),
                    ui.output_data_frame("performance_metrics"),
                    ui.hr(),
                    ui.h4("Visualizations", style="color:#00E6A8;"),
                    ui.p(
                        "Explore the price trend of each stock, the long spread between the pair, and the standardized Z-score signal.",
                        style="color:#CCCCCC;",
                    ),
                    ui.layout_columns(
                        ui.column(
                            12,
                            ui.card(
                                ui.h5("Price Trend", style="color:#00E6A8;"),
                                output_widget("price_trend_chart"),
                            ),
                        ),
                        ui.column(
                            12,
                            ui.card(
                                ui.h5("Long Spread", style="color:#00E6A8;"),
                                output_widget("spread_chart"),
                            ),
                        ),
                        ui.column(
                            12,
                            ui.card(
                                ui.h5("Z-Score", style="color:#00E6A8;"),
                                output_widget("zscore_chart"),
                            ),
                        ),
                    ),
                ),
            )
        ),
    )


def make_strategy_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Strategy",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(

                    # -------------------------------------
                    # Title + Intro
                    # -------------------------------------
                    ui.h3("📈 Strategy Suggestions", 
                          style="color:#00E6A8; margin-bottom:8px;"),

                    ui.p(
                        "Generate a market-neutral long/short strategy tailored to your investment amount and risk preferences.",
                        style="color:#CCCCCC; margin-bottom:20px;"
                    ),

                    # -------------------------------------
                    # Section 1 — Preferences
                    # -------------------------------------
                    ui.h4("📝 1. Configure Your Preferences",
                          style="color:#00E6A8; margin-top:10px;"),

                    # Investment Amount
                    ui.input_numeric(
                        "investment_amount",
                        "💰 Investment Amount ($)",
                        10000,
                        min=1000,
                        max=1000000,
                        step=500
                    ),

                    ui.p(
                        "💡 Typical range for pair-trading portfolios: $1,000–$500,000. "
                        "More capital enables more stable position sizing and smoother equity curves.",
                        style="color:#AAAAAA; margin-top:4px; margin-bottom:18px;"
                    ),

                    # Risk Level
                    ui.input_select(
                        "risk_level",
                        "⚖️ Risk Level",
                        ["Low", "Medium", "High"]
                    ),

                    ui.tags.ul(
                        ui.tags.li("Low – Fewer trades, wider thresholds, smaller position sizes, minimal leverage."),
                        ui.tags.li("Medium – Balanced trade frequency and leverage."),
                        ui.tags.li("High – More aggressive signals, tighter thresholds, higher leverage and drawdown."),
                        style="color:#CCCCCC; font-size:14px; margin-top:4px;"
                    ),

                    ui.hr(),

                    # -------------------------------------
                    # Section 2 — Z-score Explanation
                    # -------------------------------------
                    ui.h4("📊 2. Understanding Z-score (Core Signal)",
                          style="color:#00E6A8; margin-top:10px;"),

                    ui.p(
                        "The Z-score measures how far the current price spread deviates from its historical average. "
                        "It standardizes spread movements to detect statistically abnormal divergence.",
                        style="color:#CCCCCC; margin-bottom:10px;"
                    ),

                    ui.tags.ul(
                        ui.tags.li("Z > 2 → Spread unusually wide → Short overpriced asset, long underpriced asset."),
                        ui.tags.li("Z < -2 → Spread unusually tight → Long overpriced asset, short underpriced asset."),
                        ui.tags.li("Higher-risk profiles use smaller Z-thresholds for more frequent signals."),
                        style="color:#CCCCCC; font-size:14px;"
                    ),

                    ui.p(
                        "Z-score defines when to enter and exit trades. Your selected risk level changes how sensitive these thresholds are.",
                        style="color:#AAAAAA; margin-top:6px; margin-bottom:18px;"
                    ),

                    ui.hr(),

                    # -------------------------------------
                    # Button
                    # -------------------------------------
                    ui.input_action_button(
                        "generate_strategy",
                        "🚀 Generate Strategy",
                        class_="btn btn-success btn-lg",
                        style="margin-top:10px; margin-bottom:15px;"
                    ),

                    ui.hr(),

                    # -------------------------------------
                    # Section 3 — Recommended Strategy Output
                    # -------------------------------------
                    ui.h4("📘 Recommended Strategy",
                          style="color:#00E6A8; margin-top:5px;"),

                    ui.p(
                        "Based on your inputs, the model generates recommended allocations, entry/exit thresholds, "
                        "expected trade behaviour, and a rationale for how the strategy adapts to your profile.",
                        style="color:#CCCCCC; margin-bottom:12px;"
                    ),

                    # Dynamic text returned by server
                    ui.div(
                        ui.output_text_verbatim("strategy_output"),
                        style="white-space:pre-line; color:#CCCCCC; margin-bottom:12px;"
                    ),

                    # Chart
                    output_widget("strategy_chart"),

                ),
            )
        ),
    )


def make_about_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "About",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    {"style": "max-width: 900px; margin: 0 auto; padding: 30px;"},
                    ui.h3("About HedgeHub", style="color:#00E6A8; text-align:center;"),

                    ui.p(
                        "HedgeHub is a smart pairs trading analytics platform built by Duke FinTech students. "
                        "It provides an intuitive, data-driven interface for exploring price relationships, testing "
                        "cointegration, analyzing spreads, and generating market-neutral trading insights.",
                        style="color:#CCCCCC; text-align:center;",
                    ),

                    ui.p(
                        "Pairs trading identifies two historically related assets whose price spread temporarily diverges. "
                        "When this spread reaches statistically extreme levels, a long/short strategy may profit from mean reversion. "
                        "HedgeHub helps users visualize these dynamics and evaluate strategy performance in an accessible way.",
                        style="color:#CCCCCC; text-align:center;",
                    ),

                    ui.hr(),

                    ui.h4("Team", style="color:#00E6A8; text-align:center;"),
                    ui.div(
                        {"style": "text-align:center; line-height: 1.8; color:#CCCCCC;"},
                        ui.p("Junze Li — Email: jl1319@duke.edu"),
                        ui.p("Celia Du — Email: xd90@duke.edu"),
                        ui.p("Zifei Yang — Email: zy204@duke.edu"),
                    ),

                    ui.hr(),

                    ui.p(
                        "This platform is for educational and research purposes only and does not constitute financial advice.",
                        style="color:#CCCCCC; text-align:center; font-size:0.9rem; opacity:0.8;",
                    ),

                    ui.p(
                        "© 2025 HedgeHub Analytics",
                        class_="text-center",
                        style="color:#CCCCCC; margin-top:10px;",
                    ),
                ),
            )
        ),
    )


# ---------------------------------------------------------
# GLOBAL CSS + Layout
# ---------------------------------------------------------
app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600&display=swap",
            rel="stylesheet",
        ),
        ui.tags.style(
            """
            label { color: #CCCCCC !important; }
            #strategy_output, .shiny-output-text-verbatim { color: #CCCCCC !important; }
            #pair_test_result {
                color: #FFFFFF !important;
                background-color: transparent;
                border: none;
            }
            table, th, td, .dataframe, .dataframe th, .dataframe td {
                color: #CCCCCC !important;
                background: transparent !important;
            }
            tbody tr td { color: #CCCCCC !important; }
            body {
                background: linear-gradient(180deg, #0F1A1A 0%, #062E2E 60%, #0F1A1A 100%);
                color: #CCCCCC;
                font-family: 'Inter', sans-serif;
            }
            .navbar {
                background-color: #0F1A1A !important;
                border-bottom: 1px solid rgba(0,230,168,0.2);
                padding: 0.6rem 3rem !important;
            }
            .nav-left { display: flex; align-items: center; gap: 8px; }
            .brand-main {
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                font-size: 1.5rem;
                color: #00E6A8;
            }
            .nav-link { color: #FFFFFF !important; transition: all 0.3s; }
            .nav-link.active { color:#00E6A8 !important; border-bottom:2px solid #00E6A8; }
            .nav-link:hover { color:#00E6A8 !important; text-shadow:0 0 6px #00E6A8; }
            .card {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                padding: 20px;
            }
            h1, h3, h4 { color:#00E6A8; }
            p { color:#CCCCCC !important; }
        """
        ),
    ),
    ui.page_navbar(
        make_home_panel(),
        make_pair_panel(),
        make_strategy_panel(),
        make_about_panel(),
        title=ui.tags.div(
            {"class": "custom-navbar"},
            ui.tags.div(
                {"class": "nav-left"},
                ui.tags.span("🟢", style="font-size:1.4rem; margin-right:6px;"),
                ui.tags.span("HedgeHub", {"class": "brand-main"}),
            ),
        ),
        id=NAVBAR_ID,
    ),
)


# ---------------------------------------------------------
# SERVER
# ---------------------------------------------------------
def server(input, output, session):
    analysis_result = reactive.Value(None)
    analysis_error = reactive.Value(
        "Enter stock tickers and a date range, then click Run Pair Test."
    )
    strategy_plan = reactive.Value(None)

    def _clean_ticker_label(value: str | None, fallback: str) -> str:
        label = (value or "").strip().upper()
        return label if label else fallback

    def _format_z(value: float) -> str:
        return f"{value:+.2f} Z"

    def _resolve_entry_exit(plan: StrategyPlan) -> tuple[str, str]:
        lower_signal = plan.signal_type.lower()
        entry = plan.entry_z
        exit_value = plan.exit_z

        if lower_signal.startswith("long"):
            entry = -abs(entry)
            exit_value = abs(exit_value)
        elif lower_signal.startswith("short"):
            entry = abs(entry)
            exit_value = -abs(exit_value)
        else:
            entry = plan.entry_z
            exit_value = plan.exit_z

        return _format_z(entry), _format_z(exit_value)

    def _info_row(label: str, value: str):
        return ui.tags.div(
            ui.tags.span(label, style="color:#7EE1C3; font-size:0.9rem; letter-spacing:0.04em;"),
            ui.tags.span(value, style="color:#FFFFFF; font-weight:600; font-size:1rem;"),
            style=(
                "display:flex; justify-content:space-between; align-items:center;"
                "padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.07);"
            ),
        )
        
    def _stat_chip(label: str, value: str, accent: str = "#00E6A8"):
        return ui.tags.div(
            ui.tags.small(label.upper(), style="color:rgba(255,255,255,0.65); letter-spacing:0.08em;"),
            ui.tags.span(
                value,
                style=f"color:#FFFFFF; font-weight:600; font-size:1.05rem; text-shadow:0 0 8px {accent};",
            ),
            style=(
                "min-width:160px; padding:12px 16px; border-radius:14px;"
                "background:rgba(15,26,26,0.85); border:1px solid rgba(255,255,255,0.08);"
                "box-shadow:0 10px 30px rgba(0,0,0,0.35); display:flex; flex-direction:column; gap:6px;"
            ),
        )

    def _build_strategy_modal(plan: StrategyPlan, has_pair_data: bool) -> ui.modal:
        entry_label, exit_label = _resolve_entry_exit(plan)
        snapshot_note = (
            "Run Pair Analysis to refresh live spread inputs."
            if not has_pair_data
            else ""
        )

        signal_section = ui.div(
            {
                "style": "flex:1 1 320px; background:linear-gradient(135deg, rgba(0,230,168,0.18), rgba(6,46,46,0.8));"
                "border:1px solid rgba(0,230,168,0.25); border-radius:18px; padding:20px; min-width:280px;"
            },
            ui.tags.span(
                "Signal Card",
                style="color:#00E6A8; font-weight:600; letter-spacing:0.08em; font-size:0.85rem;",
            ),
            ui.h4(plan.signal_type, style="color:#FFFFFF; margin:6px 0 18px 0;"),
            _info_row("Rationale", plan.rationale),
            _info_row("Entry Trigger", entry_label),
            _info_row("Exit Trigger", exit_label),
        )

        snapshot_children = [
            ui.h5("Market Snapshot", style="color:#00E6A8; margin-bottom:10px;"),
            _info_row("Spread", f"{plan.spread_value:.2f}"),
            _info_row("Z-score", _format_z(plan.zscore_value)),
        ]   
        
        if snapshot_note:
            snapshot_children.append(
                ui.tags.small(
                    snapshot_note,
                    style="color:#AAAAAA; display:block; margin-top:6px;",
                )
            )

        snapshot_section = ui.div(
            {
                "style": "flex:1 1 320px; background:rgba(255,255,255,0.04);"
                "border:1px solid rgba(255,255,255,0.15); border-radius:18px; padding:20px; min-width:280px;"
            },
            *snapshot_children,
        )

        chips = ui.tags.div(
            {
                "style": "display:flex; flex-wrap:wrap; gap:16px; margin-bottom:18px;"
            },
            _stat_chip("Risk", plan.risk_level),
            _stat_chip("Allocation", f"{plan.allocation_pct*100:.0f}%"),
            _stat_chip("Deploy", format_currency(plan.suggested_notional)),
        )

        footer = ui.tags.div(
            ui.tags.span(
                f"Deploy ≈{format_currency(plan.suggested_notional)} "
                f"({plan.allocation_pct * 100:.0f}% of capital)",
                style="color:#CCCCCC; font-size:0.95rem;",
            )
        )
        
        return ui.modal(
            ui.div(
                {
                    "style": "background:linear-gradient(145deg, rgba(15,26,26,0.95), rgba(6,46,46,0.92));"
                    "border-radius:22px; padding:10px; border:1px solid rgba(255,255,255,0.04);"
                    "box-shadow:0 25px 50px rgba(0,0,0,0.55);"
                },
                ui.div(
                    {
                        "style": "background:rgba(0,0,0,0.2); border-radius:18px; padding:24px;"
                    },
                    chips,
                    ui.tags.div(
                        {"style": "display:flex; flex-wrap:wrap; gap:20px;"},
                        signal_section,
                        snapshot_section,
                    ),
                ),
            ),
            title="Strategy Recommendation",
            easy_close=True,
            footer=footer,
            size="m",
        )
        
    @reactive.effect
    @reactive.event(input.go_to_analysis)
    def _handle_home_cta():
        ui.update_navs(
            id=NAVBAR_ID,
            selected="Pair Analysis",
            session=session,
        )

    @reactive.effect
    @reactive.event(input.generate_strategy)
    def _handle_strategy_generation():
        amount = float(input.investment_amount() or 0.0)
        risk_choice = input.risk_level() or "Medium"
        ticker_a = _clean_ticker_label(input.stock_a(), "ASSET A")
        ticker_b = _clean_ticker_label(input.stock_b(), "ASSET B")
        pair_data = analysis_result.get()

        plan = generate_strategy_plan(
            amount=amount,
            risk_level=risk_choice,
            pair_result=pair_data,
            ticker_a=ticker_a,
            ticker_b=ticker_b,
        )
        strategy_plan.set(plan)

        ui.modal_show(_build_strategy_modal(plan, has_pair_data=pair_data is not None))
        
    @reactive.effect
    @reactive.event(input.run_analysis)
    def _run_pair_analysis():
        ticker_a = (input.stock_a() or "").strip().upper()
        ticker_b = (input.stock_b() or "").strip().upper()
        date_range = input.date_range()

        if not ticker_a or not ticker_b or not date_range:
            analysis_result.set(None)
            analysis_error.set("Please enter both tickers and select a valid date range.")
            return

        start, end = date_range
        try:
            result = analyze_pair(
                ticker_a=ticker_a,
                ticker_b=ticker_b,
                start=str(start),
                end=str(end),
            )
        except Exception as err:
            analysis_result.set(None)
            analysis_error.set(f"Error: {err}")
        else:
            analysis_result.set(result)
            analysis_error.set("")

    @render.text
    def pair_test_result():
        result = analysis_result.get()
        error_message = analysis_error.get()

        if result is not None:
            return result.explanation
        if error_message:
            return error_message
        return "Enter stock tickers and a date range, then click Run Pair Test."

    @render.data_frame
    def performance_metrics():
        ticker_a = (input.stock_a() or "Stock A").upper()
        ticker_b = (input.stock_b() or "Stock B").upper()
        pair_label = f"{ticker_a}/{ticker_b}"
        user_capital = float(input.initial_capital() or 1_000_000.0)
        shares_per_trade = int(input.shares_per_trade() or 0)

        result = analysis_result.get()
        metrics = result.performance if result else None

        if result is None or metrics is None:
            waiting_note = analysis_error.get() or f"Waiting for trades from {pair_label}"
            data = [
                {
                    "Metric": "Initial Capital",
                    "Value": format_currency(user_capital),
                    "Notes": "Configured once analysis runs",
                },
                {
                    "Metric": "Shares per Trade",
                    "Value": f"{shares_per_trade:,}",
                    "Notes": "User-defined size per signal",
                },
                {
                    "Metric": "Final Value",
                    "Value": format_currency(user_capital),
                    "Notes": "Pending calculation",
                },
                {
                    "Metric": "Total Return",
                    "Value": "0.00%",
                    "Notes": "Calculated after live backtest",
                },
                {
                    "Metric": "Annualized Return",
                    "Value": "0.00%",
                    "Notes": "Calculated after live backtest",
                },
                {
                    "Metric": "Annualized Volatility",
                    "Value": "0.00%",
                    "Notes": "Calculated after live backtest",
                },
                {
                    "Metric": "Sharpe Ratio",
                    "Value": "0.00",
                    "Notes": "Calculated after live backtest",
                },
                {
                    "Metric": "Max Drawdown",
                    "Value": "0.00%",
                    "Notes": "Calculated after live backtest",
                },
                {
                    "Metric": "Total Trades",
                    "Value": "0",
                    "Notes": waiting_note,
                },
            ]
            return pd.DataFrame(data)

        scaled_final_value = user_capital * (1 + metrics.total_return)

        data = [
            {
                "Metric": "Initial Capital",
                "Value": format_currency(user_capital),
                "Notes": "Starting notional used for backtest",
            },
            {
                "Metric": "Shares per Trade",
                "Value": f"{shares_per_trade:,}",
                "Notes": "Size submitted on each entry signal",
            },
            {
                "Metric": "Final Value",
                "Value": format_currency(scaled_final_value),
                "Notes": f"Strategy valuation after testing {pair_label}",
            },
            {
                "Metric": "Total Return",
                "Value": format_percentage(metrics.total_return),
                "Notes": "Aggregate return over selected window",
            },
            {
                "Metric": "Annualized Return",
                "Value": format_percentage(metrics.annualized_return),
                "Notes": "Compounded using daily observations",
            },
            {
                "Metric": "Annualized Volatility",
                "Value": format_percentage(metrics.annualized_volatility),
                "Notes": "Scaled by sqrt(252) trading days",
            },
            {
                "Metric": "Sharpe Ratio",
                "Value": f"{metrics.sharpe_ratio:.2f}",
                "Notes": "Uses annualized return and volatility",
            },
            {
                "Metric": "Max Drawdown",
                "Value": format_percentage(metrics.max_drawdown),
                "Notes": "Worst peak-to-trough decline in equity curve",
            },
            {
                "Metric": "Total Trades",
                "Value": str(metrics.total_trades),
                "Notes": f"Entries generated by z-score triggers for {pair_label}",
            },
        ]
        return pd.DataFrame(data)

    def _style_figure(fig):
        fig.update_layout(
            plot_bgcolor="#0F1A1A",
            paper_bgcolor="#0F1A1A",
            font_color="#CCCCCC",
            legend_font_color="#CCCCCC",
        )
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        return fig

    @render_widget
    def price_trend_chart():
        result = analysis_result.get()
        prices = result.prices if result else None

        if prices is None or prices.empty:
            return px.line()

        price_df = prices.copy().reset_index()
        price_df.rename(columns={price_df.columns[0]: "date"}, inplace=True)
        value_cols = [c for c in price_df.columns if c != "date"]

        fig = px.line(
            price_df,
            x="date",
            y=value_cols,
            color_discrete_sequence=["#00E6A8", "#00A2FF"],
        )
        return _style_figure(fig)

    @render_widget
    def spread_chart():
        result = analysis_result.get()

        if result is None or result.spread_series.empty:
            return px.line()

        df = pd.DataFrame(
            {"date": result.spread_series.index, "spread": result.spread_series.values}
        )

        fig = px.line(df, x="date", y="spread", color_discrete_sequence=["#00E6A8"])
        fig.update_traces(line_width=2)
        return _style_figure(fig)

    @render_widget
    def zscore_chart():
        result = analysis_result.get()
        zscores = result.spread_zscores if result else None

        if zscores is None or zscores.empty:
            return px.line()

        df = pd.DataFrame({"date": zscores.index, "zscore": zscores.values})

        fig = px.line(df, x="date", y="zscore", color_discrete_sequence=["#00E6A8"])
        fig.update_traces(line_width=2)
        fig.add_hline(y=2, line_dash="dot", line_color="#FFB347", opacity=0.6)
        fig.add_hline(y=-2, line_dash="dot", line_color="#FFB347", opacity=0.6)
        fig.add_hline(y=0.5, line_dash="dash", line_color="#888888", opacity=0.4)
        fig.add_hline(y=-0.5, line_dash="dash", line_color="#888888", opacity=0.4)
        return _style_figure(fig)

    @render.text
    def strategy_output():
        plan = strategy_plan.get()
        if plan is None:
            amt = format_currency(float(input.investment_amount() or 0.0))
            risk = input.risk_level() or "Medium"
            return (
                f"Capital ready: {amt} | Risk level: {risk}. "
                "Click Generate Strategy to unlock tailored guidance."
            )

        allocation_pct = plan.allocation_pct * 100
        return (
            f"{plan.signal_type} — Risk {plan.risk_level}. "
            f"Allocate ≈{format_currency(plan.suggested_notional)} "
            f"({allocation_pct:.0f}% of capital). "
            f"Entry {plan.entry_z:.2f} Z / Exit {plan.exit_z:.2f} Z."
        )
        
    @render_widget
    def strategy_chart():
        plan = strategy_plan.get()

        if plan is None:
            df = pd.DataFrame({"day": [1, 2, 3, 4], "balance": [100, 102, 104, 103]})
        else:
            drift_map = {"Low": 0.0005, "Medium": 0.0009, "High": 0.0013}
            vol_map = {"Low": 0.0006, "Medium": 0.0011, "High": 0.0016}

            drift = drift_map.get(plan.risk_level, 0.0008)
            vol = vol_map.get(plan.risk_level, 0.0012)

            base = max(plan.suggested_notional, 1.0)
            days = list(range(1, 16))
            balances = []
            value = base
            for idx, _ in enumerate(days):
                oscillation = ((idx % 4) - 1.5) * vol
                value *= 1 + drift + oscillation
                balances.append(value)
            df = pd.DataFrame({"day": days, "balance": balances})
            
        fig = px.line(df, x="day", y="balance")
        fig.update_traces(line_color="#00E6A8")
        fig.update_layout(
            plot_bgcolor="#0F1A1A",
            paper_bgcolor="#0F1A1A",
            font_color="#CCCCCC",
        )
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        return fig


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
