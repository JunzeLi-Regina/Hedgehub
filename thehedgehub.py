from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px

from strategy_engine import analyze_pair

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

    @reactive.effect
    @reactive.event(input.go_to_analysis)
    def _handle_home_cta():
        ui.update_navs(
            id=NAVBAR_ID,
            selected="Pair Analysis",
            session=session,
        )

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
        amt = input.investment_amount()
        risk = input.risk_level()
        return f"Suggested base allocation for ${amt} with risk level {risk}."

    @render_widget
    def strategy_chart():
        df = pd.DataFrame({"day": [1, 2, 3, 4], "balance": [100, 102, 104, 103]})
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
