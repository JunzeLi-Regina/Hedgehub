from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px

# Backend logic
from strategy_engine import analyze_pair

NAVBAR_ID = "main_nav"

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
                    ui.h1("Welcome to HedgeHub", class_="text-center", style="color:#00E6A8;"),
                    ui.h4("Smart Pair Trading Analysis Platform", class_="text-center", style="color:#00E6A8;"),
                    ui.hr(),

                    ui.tags.iframe(
                        src="https://www.youtube.com/embed/dQw4w9WgXcQ",
                        width="100%", height="400px",
                        style="border:none;border-radius:15px;"
                    ),
                    ui.hr(),

                    ui.div(
                        {
                            "style": """
                                display: flex;
                                justify-content: center;
                                gap: 40px;
                                margin-top: 20px;
                                padding-bottom: 10px;
                            """
                        },
                        ui.card(
                            ui.h4("Analyze Pairs", style="color:#00E6A8; text-align:center;"),
                            ui.p("Test if two stocks form a cointegrated pair.",
                                 style="text-align:center; color:#CCCCCC;")
                        ),
                        ui.card(
                            ui.h4("Generate Strategy", style="color:#00E6A8; text-align:center;"),
                            ui.p("Get long/short suggestions based on signals.",
                                 style="text-align:center; color:#CCCCCC;")
                        ),
                        ui.card(
                            ui.h4("Market Insights", style="color:#00E6A8; text-align:center;"),
                            ui.p("Follow financial news and sentiment for your pair.",
                                 style="text-align:center; color:#CCCCCC;")
                        )
                    ),

                    ui.hr(),
                    ui.h3("How Pairs Trading Works", style="color:#00E6A8; text-align:center;"),
                    ui.p(
                        "Pairs trading looks for two historically related assets whose price relationship briefly drifts away from its long-run trend.",
                        style="text-align:center; color:#CCCCCC;"
                    ),
                    ui.tags.ol(
                        {
                            "style": """
                                max-width: 720px;
                                margin: 0 auto;
                                color: #CCCCCC;
                                line-height: 1.6;
                                text-align: left;
                            """
                        },
                        ui.tags.li("Select two instruments that tend to move together (correlated fundamentals or price history)."),
                        ui.tags.li("Track the spread—often the difference or ratio between the two prices—to understand their relationship."),
                        ui.tags.li("Standardize the spread into a Z-score so you know how extreme the current divergence is versus history."),
                        ui.tags.li("Enter a market-neutral trade when the Z-score breaches an entry threshold (e.g., ±2)."),
                        ui.tags.li("Exit when the spread mean-reverts, a stop triggers, or the holding period limit is reached.")
                    ),
                    ui.p(
                        "Because the logic is statistical, you can apply the workflow above to any qualified pair—equities, ETFs, or other assets—once you confirm the relationship is stable enough for mean reversion.",
                        style="text-align:center; color:#CCCCCC;"
                    ),
                    ui.hr(),
                    ui.input_action_button(
                        "go_to_analysis",
                        "Start Analysis",
                        class_="btn btn-success btn-lg d-block mx-auto shadow-green"
                    )
                )
            )
        )
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

                    ui.input_action_button("run_analysis", "Run Pair Test",
                                           class_="btn btn-outline-success"),
                    ui.hr(),

                    ui.h4("Performance Metrics", style="color:#00E6A8;"),
                    ui.p(
                        "These placeholders summarize key portfolio stats for the selected pair. The table will refresh once you run a new analysis.",
                        style="color:#CCCCCC;"
                    ),
                    ui.output_data_frame("performance_metrics"),
                    ui.hr(),

                    ui.h4("Results", style="color:#00E6A8;"),
                    ui.output_text_verbatim("pair_test_result"),
                    output_widget("pair_chart"),
                )
            )
        )
    )


def make_strategy_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Strategy",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h3("Strategy Suggestions", style="color:#00E6A8;"),
                    ui.p("Configure your preferences.", style="color:#CCCCCC;"),

                    ui.input_numeric("investment_amount", "Investment Amount ($)", 10000),
                    ui.input_select("risk_level", "Risk Level", ["Low", "Medium", "High"]),

                    ui.input_action_button("generate_strategy", "Generate Strategy",
                                           class_="btn btn-outline-success"),

                    ui.hr(),
                    ui.h4("Recommended Strategy", style="color:#00E6A8;"),
                    ui.output_text_verbatim("strategy_output"),
                    output_widget("strategy_chart")
                )
            )
        )
    )


def make_about_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "About",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h3("About HedgeHub", style="color:#00E6A8;"),
                    ui.p("Developed by Duke FinTech Students (2025).", style="color:#CCCCCC;"),
                    ui.p("Contact: jl1319@duke.edu", style="color:#CCCCCC;"),
                    ui.p("This platform is for educational purposes only and not financial advice.",
                         style="color:#CCCCCC;"),
                    ui.hr(),
                    ui.p("© 2025 HedgeHub Analytics", class_="text-center", style="color:#CCCCCC;")
                )
            )
        )
    )


# ---------------------------------------------------------
# GLOBAL CSS + Layout
# ---------------------------------------------------------

app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600&display=swap",
            rel="stylesheet"
        ),

        # -------- CSS FIXES HERE --------
        ui.tags.style("""

            /* ------ Fix all input labels ------ */
            label {
                color: #CCCCCC !important;
            }

            /* ------ Fix strategy output text ------ */
            #strategy_output, .shiny-output-text-verbatim {
                color: #CCCCCC !important;
            }
            
            /* ------ Pair Analysis result text: make it white ------ */
            #pair_test_result {
                color: #FFFFFF !important;
                background-color: transparent;
                border: none;
            }

            /* ------ Fix all table cells ------ */
            table, th, td, .dataframe, .dataframe th, .dataframe td {
                color: #CCCCCC !important;
                background: transparent !important;
            }

            tbody tr td {
                color: #CCCCCC !important;
            }

            /* ------ Main Theme ------ */
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

            .nav-link { color: #C0C0C0 !important; transition: all 0.3s; }
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

        """)
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
                ui.tags.span("HedgeHub", {"class": "brand-main"})
            )
        ),
        id=NAVBAR_ID,
    )
)


# ---------------------------------------------------------
# SERVER
# ---------------------------------------------------------

def server(input, output, session):

    last_pair_inputs = reactive.Value(None)
    last_pair_result = reactive.Value(None)

    def _fetch_pair_result():
        ticker_a = input.stock_a()
        ticker_b = input.stock_b()
        date_range = input.date_range()

        if not ticker_a or not ticker_b or not date_range:
            return None, "Please enter stock tickers and date range."

        key = (ticker_a, ticker_b, tuple(str(d) for d in date_range))
        cached_key = last_pair_inputs.get()
        cached_result = last_pair_result.get()

        if cached_key == key and cached_result is not None:
            return cached_result, None

        start, end = date_range
        try:
            result = analyze_pair(
                ticker_a=ticker_a,
                ticker_b=ticker_b,
                start=str(start),
                end=str(end)
            )
        except Exception as e:
            last_pair_inputs.set(None)
            last_pair_result.set(None)
            return None, f"Error: {e}"

        last_pair_inputs.set(key)
        last_pair_result.set(result)
        return result, None

    # ----- Navbar interactions -----
    @reactive.effect
    @reactive.event(input.go_to_analysis)
    def _handle_home_cta():
        ui.update_navs(
            id=NAVBAR_ID,
            selected="Pair Analysis",
            session=session,
        )

    # ----- Pair analysis -----
    @render.text
    @reactive.event(input.run_analysis)
    def pair_test_result():
        result, error = _fetch_pair_result()
        if error:
            return error
        return result.explanation


    @render_widget
    @reactive.event(input.run_analysis)
    def pair_chart():
        result, error = _fetch_pair_result()
        if error or result is None:
            return px.line()

        df = pd.DataFrame({
            "date": result.spread_series.index,
            "spread": result.spread_series.values
        })

        fig = px.line(df, x="date", y="spread")
        fig.update_traces(line_color="#00E6A8")

        fig.update_layout(
            plot_bgcolor="#0F1A1A",
            paper_bgcolor="#0F1A1A",
            font_color="#CCCCCC"
        )

        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)

        return fig


    @render.data_frame
    @reactive.event(input.run_analysis)
    def performance_metrics():
        result, error = _fetch_pair_result()
        if error or result is None:
            return pd.DataFrame(
                [{"Metric": "Status", "Value": error or "Unavailable", "Notes": "Unable to compute metrics"}]
            )

        perf = getattr(result, "performance", None) or {}

        def fmt_currency(value):
            if value is None:
                return "N/A"
            return f"${value:,.2f}"

        def fmt_percent(value):
            if value is None:
                return "N/A"
            return f"{value * 100:.2f}%"

        def fmt_ratio(value):
            if value is None:
                return "N/A"
            return f"{value:.2f}"

        rows = [
            {
                "Metric": "Initial Capital",
                "Value": fmt_currency(perf.get("initial_capital")),
                "Notes": "Base capital allocated to the pair strategy",
            },
            {
                "Metric": "Final Value",
                "Value": fmt_currency(perf.get("final_value")),
                "Notes": "Marked-to-market portfolio equity at the end of the sample",
            },
            {
                "Metric": "Total Return",
                "Value": fmt_percent(perf.get("total_return")),
                "Notes": "Overall growth relative to initial capital",
            },
            {
                "Metric": "Annualized Return",
                "Value": fmt_percent(perf.get("annualized_return")),
                "Notes": "Return scaled to a 252-trading-day year",
            },
            {
                "Metric": "Annualized Volatility",
                "Value": fmt_percent(perf.get("annualized_volatility")),
                "Notes": "Standard deviation of daily equity changes (annualized)",
            },
            {
                "Metric": "Sharpe Ratio",
                "Value": fmt_ratio(perf.get("sharpe_ratio")),
                "Notes": "Return per unit of volatility (risk-free assumed 0%)",
            },
            {
                "Metric": "Max Drawdown",
                "Value": fmt_percent(perf.get("max_drawdown")),
                "Notes": "Largest peak-to-trough decline during the sample",
            },
            {
                "Metric": "Total Trades",
                "Value": perf.get("total_trades", 0),
                "Notes": "Number of simulated entry events triggered by Z-score thresholds",
            },
        ]

        return pd.DataFrame(rows)


    # ----- Strategy panel -----
    @render.text
    def strategy_output():
        amt = input.investment_amount()
        risk = input.risk_level()
        return f"Suggested base allocation for ${amt} with risk level {risk}."


    @render_widget
    def strategy_chart():
        df = pd.DataFrame({"day":[1,2,3,4], "balance":[100,102,104,103]})

        fig = px.line(df, x="day", y="balance")
        fig.update_traces(line_color="#00E6A8")

        fig.update_layout(
            plot_bgcolor="#0F1A1A",
            paper_bgcolor="#0F1A1A",
            font_color="#CCCCCC"
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
