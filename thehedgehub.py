from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px


# ---------- Panels (each returns a ui.nav_panel) ----------
def make_home_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Home",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h1("Welcome to HedgeHub", class_="text-center"),
                    ui.h4(
                        "Smart Pair Trading Analysis Platform",
                        class_="text-center text-muted"
                    ),
                    ui.hr(),
                    ui.tags.iframe(
                        src="https://www.youtube.com/embed/dQw4w9WgXcQ",
                        width="100%",
                        height="400px",
                        style="border:none;"
                    ),
                    ui.hr(),
                    ui.layout_columns(
                        ui.column(
                            4,
                            ui.card(
                                ui.h4("Analyze Pairs"),
                                ui.p("Test if two stocks form a cointegrated pair.")
                            )
                        ),
                        ui.column(
                            4,
                            ui.card(
                                ui.h4("Generate Strategy"),
                                ui.p("Get long/short suggestions based on signals.")
                            )
                        ),
                        ui.column(
                            4,
                            ui.card(
                                ui.h4("Market Insights"),
                                ui.p("Follow financial news and sentiment for your pair.")
                            )
                        )
                    ),
                    ui.hr(),
                    ui.layout_columns(
                        ui.column(
                            12,
                            ui.input_action_button(
                                "go_to_analysis",
                                "Start Analysis",
                                class_="btn-primary btn-lg d-block mx-auto"
                            )
                        )
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
                    ui.h3("Pair Analysis"),
                    ui.p("Input your stock pair and run a basic pair test."),
                    ui.input_text("stock_a", "Stock A (e.g., AAPL)", ""),
                    ui.input_text("stock_b", "Stock B (e.g., MSFT)", ""),
                    ui.input_date_range("date_range", "Date Range"),
                    ui.input_action_button(
                        "run_analysis",
                        "Run Pair Test",
                        class_="btn-success"
                    ),
                    ui.hr(),
                    ui.h4("Results"),
                    ui.output_text_verbatim("pair_test_result"),
                    output_widget("pair_chart")
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
                    ui.h3("Strategy Suggestions"),
                    ui.p("Configure your preferences."),
                    ui.input_numeric("investment_amount", "Investment Amount ($)", 10000),
                    ui.input_select("risk_level", "Risk Level", ["Low", "Medium", "High"]),
                    ui.input_action_button(
                        "generate_strategy",
                        "Generate Strategy",
                        class_="btn-warning"
                    ),
                    ui.hr(),
                    ui.h4("Recommended Strategy"),
                    ui.output_text_verbatim("strategy_output"),
                    output_widget("strategy_chart")
                )
            )
        )
    )


def make_news_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Market News",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h3("Market News and Sentiment"),
                    ui.p("News and sentiment for the selected pair."),
                    ui.input_action_button(
                        "refresh_news",
                        "Refresh News",
                        class_="btn-info"
                    ),
                    ui.hr(),
                    ui.h4("Sentiment Summary"),
                    ui.output_data_frame("sentiment_summary"),
                    ui.hr(),
                    ui.h4("Recent News"),
                    ui.output_data_frame("news_table"),
                    ui.hr(),
                    ui.h4("Sentiment Over Time"),
                    output_widget("sentiment_chart")
                )
            )
        )
    )


def make_about_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "About Us",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h3("About HedgeHub"),
                    ui.p("Developed by Duke FinTech Students (2025)."),
                    ui.p("Contact: jl1319@duke.edu"),
                    ui.p("This platform is for educational purposes only and not financial advice."),
                    ui.hr(),
                    ui.p("© 2025 HedgeHub Analytics")
                )
            )
        )
    )


# ---------- App UI ----------
app_ui = ui.page_navbar(
    make_home_panel(),
    make_pair_panel(),
    make_strategy_panel(),
    make_news_panel(),
    make_about_panel(),
    title="HedgeHub: Pair Trading Intelligence"
)


# ---------- Server (demo placeholders so UI renders) ----------
def server(input, output, session):
    @render.text
    def pair_test_result():
        return "Results will appear here after you run the analysis."

    @render_widget
    def pair_chart():
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1.0, 1.2, 1.1, 1.3, 1.25]})
        fig = px.line(df, x="x", y="y", title="Example Pair Chart")
        return fig

    @render.text
    def strategy_output():
        amt = input.investment_amount() if input.investment_amount() is not None else 0
        risk = input.risk_level() if input.risk_level() is not None else "Medium"
        return f"Suggested base allocation for amount ${amt} with risk level {risk}."

    @render_widget
    def strategy_chart():
        df = pd.DataFrame({"day": [1, 2, 3, 4, 5], "balance": [100, 102, 104, 103, 106]})
        fig = px.line(df, x="day", y="balance", title="Strategy Performance (Demo)")
        return fig

    @render.data_frame
    def news_table():
        data = [
            {"headline": "Apple releases new product", "source": "Bloomberg", "sentiment": "Positive", "publishedAt": "2025-11-15"},
            {"headline": "Microsoft announces AI upgrade", "source": "Reuters", "sentiment": "Neutral", "publishedAt": "2025-11-14"}
        ]
        return pd.DataFrame(data)

    @render.data_frame
    def sentiment_summary():
        df = pd.DataFrame({"Positive": [60], "Neutral": [30], "Negative": [10]})
        return df

    @render_widget
    def sentiment_chart():
        df = pd.DataFrame({
            "date": ["2025-11-12", "2025-11-13", "2025-11-14", "2025-11-15"],
            "Positive": [5, 7, 6, 8],
            "Negative": [2, 3, 2, 1]
        })
        fig = px.line(df, x="date", y=["Positive", "Negative"], title="Sentiment Over Time")
        return fig


# ---------- Run ----------
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()

