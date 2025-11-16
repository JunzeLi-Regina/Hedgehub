from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px


# ---------- Panels ----------
def make_home_panel() -> ui.nav_panel:
    return ui.nav_panel(
        "Home",
        ui.layout_columns(
            ui.column(
                12,
                ui.card(
                    ui.h1("Welcome to HedgeHub", class_="text-center", style="color:#00E6A8;"),
                    ui.h4("Smart Pair Trading Analysis Platform", class_="text-center text-muted"),
                    ui.hr(),
                    ui.tags.iframe(
                        src="https://www.youtube.com/embed/dQw4w9WgXcQ",
                        width="100%", height="400px",
                        style="border:none;border-radius:15px;"
                    ),
                    ui.hr(),
                    ui.layout_columns(
                        ui.column(4, ui.card(ui.h4("Analyze Pairs", style="color:#00E6A8;"),
                                            ui.p("Test if two stocks form a cointegrated pair."))),
                        ui.column(4, ui.card(ui.h4("Generate Strategy", style="color:#00E6A8;"),
                                            ui.p("Get long/short suggestions based on signals."))),
                        ui.column(4, ui.card(ui.h4("Market Insights", style="color:#00E6A8;"),
                                            ui.p("Follow financial news and sentiment for your pair.")))
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
                    ui.p("Input your stock pair and run a basic pair test."),
                    ui.input_text("stock_a", "Stock A (e.g., AAPL)", ""),
                    ui.input_text("stock_b", "Stock B (e.g., MSFT)", ""),
                    ui.input_date_range("date_range", "Date Range"),
                    ui.input_action_button("run_analysis", "Run Pair Test", class_="btn btn-outline-success"),
                    ui.hr(),
                    ui.h4("Results", style="color:#00E6A8;"),
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
                    ui.h3("Strategy Suggestions", style="color:#00E6A8;"),
                    ui.p("Configure your preferences."),
                    ui.input_numeric("investment_amount", "Investment Amount ($)", 10000),
                    ui.input_select("risk_level", "Risk Level", ["Low", "Medium", "High"]),
                    ui.input_action_button("generate_strategy", "Generate Strategy", class_="btn btn-outline-success"),
                    ui.hr(),
                    ui.h4("Recommended Strategy", style="color:#00E6A8;"),
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
                    ui.h3("Market News and Sentiment", style="color:#00E6A8;"),
                    ui.input_action_button("refresh_news", "Refresh News", class_="btn btn-outline-success"),
                    ui.hr(),
                    ui.h4("Sentiment Summary", style="color:#00E6A8;"),
                    ui.output_data_frame("sentiment_summary"),
                    ui.hr(),
                    ui.h4("Recent News", style="color:#00E6A8;"),
                    ui.output_data_frame("news_table"),
                    ui.hr(),
                    ui.h4("Sentiment Over Time", style="color:#00E6A8;"),
                    output_widget("sentiment_chart")
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
                    ui.p("Developed by Duke FinTech Students (2025)."),
                    ui.p("Contact: jl1319@duke.edu"),
                    ui.p("This platform is for educational purposes only and not financial advice."),
                    ui.hr(),
                    ui.p("© 2025 HedgeHub Analytics", class_="text-muted text-center")
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
    title=ui.tags.div(
        {"class": "custom-navbar"},
        ui.tags.div(
            {"class": "nav-left"},
            ui.tags.span("🟢", style="font-size:1.4rem; margin-right:6px;"),
            ui.tags.span("HedgeHub", {"class": "brand-main"})
        )
    )
)


# ---------- Custom CSS ----------
app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600&display=swap",
            rel="stylesheet"
        ),
        ui.tags.style("""
            body {
                background: linear-gradient(180deg, #0F1A1A 0%, #062E2E 60%, #0F1A1A 100%);
                color: #E0E0E0;
                font-family: 'Inter', sans-serif;
            }

            /* ===== 导航栏整体 ===== */
            .navbar {
                background-color: #0F1A1A !important;
                border-bottom: 1px solid rgba(0,230,168,0.2);
                padding: 0.6rem 3rem !important;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            /* ===== 左侧Logo区 ===== */
            .nav-left {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .brand-main {
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                font-size: 1.5rem;
                color: #00E6A8;
                letter-spacing: 0.5px;
            }

            /* ===== 导航按钮 ===== */
            .nav-link {
                color: #C0C0C0 !important;
                font-weight: 500;
                margin: 0 14px !important;
                letter-spacing: 0.3px;
                transition: all 0.3s ease;
            }
            .nav-link.active {
                color: #00E6A8 !important;
                border-bottom: 2px solid #00E6A8;
                padding-bottom: 3px;
            }
            .nav-link:hover {
                color: #00E6A8 !important;
                text-shadow: 0 0 6px #00E6A8;
            }

            /* ===== 卡片与正文 ===== */
            .card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(192, 192, 192, 0.2);
                border-radius: 16px;
                box-shadow: 0 0 30px rgba(0, 230, 168, 0.08);
                transition: all 0.3s ease;
            }
            .card:hover {
                box-shadow: 0 0 35px rgba(0, 230, 168, 0.2);
            }

            /* ✅ 修复 About 文本颜色 */
            p {
                color: #D0D0D0 !important;
                font-size: 1rem;
                line-height: 1.6;
            }
            a, .text-muted {
                color: #A8F0D0 !important;
            }

            /* ===== 按钮 ===== */
            .btn {
                border-radius: 12px;
                color: white !important;
                transition: all 0.3s ease;
            }
            .btn-outline-success {
                border-color: #00E6A8;
                color: #00E6A8 !important;
            }
            .btn-outline-success:hover {
                background-color: #00E6A8;
                color: #062E2E !important;
                box-shadow: 0 0 25px #00E6A8;
            }
            .btn-success {
                background-color: #00E6A8;
                border: none;
            }
            .btn-success:hover {
                box-shadow: 0 0 30px #00E6A8;
                transform: scale(1.02);
            }

            /* ===== 标题 ===== */
            h1, h3, h4 {
                color: #00E6A8;
            }
        """)
    ),
    app_ui
)


# ---------- Server ----------
def server(input, output, session):
    @render.text
    def pair_test_result():
        return "Results will appear here after you run the analysis."

    @render_widget
    def pair_chart():
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1.0, 1.2, 1.1, 1.3, 1.25]})
        fig = px.line(df, x="x", y="y", title="Example Pair Chart", template="plotly_dark")
        fig.update_traces(line_color="#00E6A8")
        return fig

    @render.text
    def strategy_output():
        amt = input.investment_amount() or 0
        risk = input.risk_level() or "Medium"
        return f"Suggested base allocation for amount ${amt} with risk level {risk}."

    @render_widget
    def strategy_chart():
        df = pd.DataFrame({"day": [1, 2, 3, 4, 5], "balance": [100, 102, 104, 103, 106]})
        fig = px.line(df, x="day", y="balance", title="Strategy Performance (Demo)", template="plotly_dark")
        fig.update_traces(line_color="#00E6A8")
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
        fig = px.line(df, x="date", y=["Positive", "Negative"], title="Sentiment Over Time", template="plotly_dark")
        fig.update_traces(line_color="#00E6A8")
        return fig


# ---------- Run ----------
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
