# from shiny import App, ui, render, reactive
# from shinywidgets import output_widget, render_widget
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# from datetime import datetime, timedelta

# # Backend logic (需要实际的strategy_engine模块)
# # from strategy_engine import analyze_pair

# # 模拟analyze_pair函数
# class MockResult:
#     def __init__(self):
#         self.explanation = "Cointegration test completed successfully."
#         self.spread_series = pd.Series(np.random.randn(100).cumsum(), 
#                                       index=pd.date_range(start='2024-01-01', periods=100))
        
# def analyze_pair(ticker_a, ticker_b, start, end):
#     return MockResult()

# # ---------------------------------------------------------
# # UI PANELS
# # ---------------------------------------------------------

# def make_home_panel() -> ui.nav_panel:
#     return ui.nav_panel(
#         "Home",
#         ui.layout_columns(
#             ui.column(
#                 12,
#                 ui.card(
#                     ui.h1("Welcome to HedgeHub", class_="text-center", style="color:#00E6A8;"),
#                     ui.h4("Smart Pair Trading Analysis Platform", class_="text-center", style="color:#00E6A8;"),
#                     ui.hr(),

#                     ui.div(
#                         ui.h5("🎯 Platform Features", style="color:#00E6A8; text-align:center; margin: 30px 0;"),
#                         style="width: 100%;"
#                     ),

#                     ui.div(
#                         {
#                             "style": """
#                                 display: grid;
#                                 grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
#                                 gap: 20px;
#                                 margin: 30px 0;
#                             """
#                         },
#                         ui.card(
#                             ui.div("📊", style="font-size: 3em; text-align: center; margin-bottom: 15px;"),
#                             ui.h4("Advanced Analytics", style="color:#00E6A8; text-align:center;"),
#                             ui.p("Statistical cointegration testing with multiple methods",
#                                  style="text-align:center; color:#CCCCCC;"),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2); padding: 25px;"
#                         ),
#                         ui.card(
#                             ui.div("🤖", style="font-size: 3em; text-align: center; margin-bottom: 15px;"),
#                             ui.h4("AI-Powered Signals", style="color:#00E6A8; text-align:center;"),
#                             ui.p("Machine learning algorithms for optimal entry/exit points",
#                                  style="text-align:center; color:#CCCCCC;"),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2); padding: 25px;"
#                         ),
#                         ui.card(
#                             ui.div("⚡", style="font-size: 3em; text-align: center; margin-bottom: 15px;"),
#                             ui.h4("Real-time Monitoring", style="color:#00E6A8; text-align:center;"),
#                             ui.p("Live spread tracking and instant alert notifications",
#                                  style="text-align:center; color:#CCCCCC;"),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2); padding: 25px;"
#                         ),
#                         ui.card(
#                             ui.div("📈", style="font-size: 3em; text-align: center; margin-bottom: 15px;"),
#                             ui.h4("Risk Management", style="color:#00E6A8; text-align:center;"),
#                             ui.p("VaR, CVaR, and comprehensive risk metrics dashboard",
#                                  style="text-align:center; color:#CCCCCC;"),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2); padding: 25px;"
#                         )
#                     ),

#                     ui.hr(),
#                     ui.div(
#                         ui.input_action_button(
#                             "go_to_analysis",
#                             "🚀 Start Analysis",
#                             class_="btn btn-success btn-lg shadow-green",
#                             style="background: linear-gradient(135deg, #00E6A8 0%, #00B088 100%); border: none; padding: 15px 50px; font-size: 1.2em; font-weight: 600;"
#                         ),
#                         style="text-align: center; margin: 40px 0;"
#                     )
#                 )
#             )
#         )
#     )


# def make_pair_panel() -> ui.nav_panel:
#     return ui.nav_panel(
#         "Pair Analysis",
#         ui.layout_columns(
#             # 左侧输入区域
#             ui.column(
#                 4,
#                 ui.card(
#                     ui.h3("📊 Configuration", style="color:#00E6A8; margin-bottom: 20px;"),
                    
#                     # 股票选择区
#                     ui.card(
#                         ui.h5("🎯 Stock Selection", style="color:#00E6A8;"),
#                         ui.input_text(
#                             "stock_a", 
#                             "Stock A", 
#                             placeholder="e.g., AAPL",
#                             value=""
#                         ),
#                         ui.input_text(
#                             "stock_b", 
#                             "Stock B", 
#                             placeholder="e.g., MSFT",
#                             value=""
#                         ),
#                         style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2);"
#                     ),
                    
#                     # 时间范围选择
#                     ui.card(
#                         ui.h5("📅 Time Period", style="color:#00E6A8;"),
#                         ui.input_date_range(
#                             "date_range", 
#                             "Date Range",
#                             start=datetime.now() - timedelta(days=365),
#                             end=datetime.now()
#                         ),
#                         ui.input_select(
#                             "quick_period",
#                             "Quick Select",
#                             {
#                                 "1M": "1 Month",
#                                 "3M": "3 Months", 
#                                 "6M": "6 Months",
#                                 "1Y": "1 Year",
#                                 "2Y": "2 Years",
#                                 "custom": "Custom"
#                             },
#                             selected="1Y"
#                         ),
#                         style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2);"
#                     ),
                    
#                     # 高级参数
#                     ui.card(
#                         ui.h5("⚙️ Advanced Settings", style="color:#00E6A8;"),
#                         ui.input_numeric(
#                             "lookback_period",
#                             "Lookback Period (days)",
#                             value=30,
#                             min=10,
#                             max=90
#                         ),
#                         ui.input_slider(
#                             "confidence_level",
#                             "Confidence Level",
#                             min=90,
#                             max=99,
#                             value=95,
#                             post="%"
#                         ),
#                         ui.input_select(
#                             "cointegration_method",
#                             "Cointegration Test",
#                             ["Engle-Granger", "Johansen", "Phillips-Ouliaris"],
#                             selected="Engle-Granger"
#                         ),
#                         ui.input_checkbox(
#                             "use_log_prices",
#                             "Use Log Prices",
#                             value=True
#                         ),
#                         style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2);"
#                     ),
                    
#                     # 运行按钮
#                     ui.div(
#                         ui.input_action_button(
#                             "run_analysis", 
#                             "🚀 Run Analysis",
#                             class_="btn btn-success btn-lg w-100",
#                             style="background: linear-gradient(135deg, #00E6A8 0%, #00B088 100%); border: none; font-weight: 600;"
#                         ),
#                         style="margin-top: 20px;"
#                     )
#                 )
#             ),
            
#             # 右侧结果展示区域
#             ui.column(
#                 8,
#                 # 顶部状态卡片
#                 ui.card(
#                     ui.div(
#                         ui.output_ui("status_cards"),
#                         style="margin-bottom: 20px;"
#                     )
#                 ),
                
#                 # 主要分析结果标签页
#                 ui.navset_card_tab(
#                     # 价格走势标签页
#                     ui.nav_panel(
#                         "Price Movement",
#                         ui.div(
#                             output_widget("price_chart"),
#                             ui.hr(style="border-color: rgba(0,230,168,0.2);"),
#                             ui.output_ui("price_statistics")
#                         )
#                     ),
                    
#                     # 价差分析标签页
#                     ui.nav_panel(
#                         "Spread Analysis",
#                         ui.div(
#                             output_widget("spread_chart"),
#                             ui.hr(style="border-color: rgba(0,230,168,0.2);"),
#                             output_widget("spread_distribution")
#                         )
#                     ),
                    
#                     # 相关性分析标签页
#                     ui.nav_panel(
#                         "Correlation",
#                         ui.div(
#                             output_widget("correlation_chart"),
#                             ui.hr(style="border-color: rgba(0,230,168,0.2);"),
#                             output_widget("rolling_correlation")
#                         )
#                     ),
                    
#                     # 协整检验标签页
#                     ui.nav_panel(
#                         "Cointegration",
#                         ui.div(
#                             ui.output_text_verbatim("cointegration_result")
#                         )
#                     ),
                    
#                     # 交易信号标签页
#                     ui.nav_panel(
#                         "Trading Signals",
#                         ui.div(
#                             output_widget("signals_chart"),
#                             ui.hr(style="border-color: rgba(0,230,168,0.2);"),
#                             ui.output_data_frame("recent_signals")
#                         )
#                     ),
                    
#                     # 风险指标标签页
#                     ui.nav_panel(
#                         "Risk Metrics",
#                         ui.div(
#                             output_widget("risk_heatmap"),
#                             ui.hr(style="border-color: rgba(0,230,168,0.2);"),
#                             ui.output_ui("risk_metrics_cards")
#                         )
#                     )
#                 )
#             )
#         )
#     )


# def make_strategy_panel() -> ui.nav_panel:
#     return ui.nav_panel(
#         "Strategy",
#         ui.layout_columns(
#             ui.column(
#                 12,
#                 ui.card(
#                     ui.h3("💡 Strategy Configuration", style="color:#00E6A8;"),
#                     ui.p("Configure your trading strategy parameters.", style="color:#CCCCCC;"),
                    
#                     ui.layout_columns(
#                         ui.card(
#                             ui.input_numeric("investment_amount", "Investment Amount ($)", 10000),
#                             ui.input_select("risk_level", "Risk Level", ["Conservative", "Moderate", "Aggressive"]),
#                             ui.input_numeric("stop_loss", "Stop Loss (%)", 5, min=1, max=20),
#                             ui.input_numeric("take_profit", "Take Profit (%)", 10, min=5, max=50),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2);"
#                         ),
#                         ui.card(
#                             ui.input_select("rebalance_freq", "Rebalance Frequency", ["Daily", "Weekly", "Monthly"]),
#                             ui.input_slider("position_size", "Position Size (%)", 0, 100, 50),
#                             ui.input_checkbox("use_leverage", "Use Leverage", False),
#                             ui.input_numeric("leverage_ratio", "Leverage Ratio", 1, min=1, max=3),
#                             style="background: rgba(0,230,168,0.05); border: 1px solid rgba(0,230,168,0.2);"
#                         )
#                     ),

#                     ui.input_action_button("generate_strategy", "🎯 Generate Strategy",
#                                            class_="btn btn-success btn-lg",
#                                            style="background: linear-gradient(135deg, #00E6A8 0%, #00B088 100%); border: none;"),

#                     ui.hr(),
#                     ui.h4("📋 Strategy Output", style="color:#00E6A8;"),
#                     ui.output_text_verbatim("strategy_output"),
#                     output_widget("strategy_chart")
#                 )
#             )
#         )
#     )


# def make_news_panel() -> ui.nav_panel:
#     return ui.nav_panel(
#         "Market News",
#         ui.layout_columns(
#             ui.column(
#                 12,
#                 ui.card(
#                     ui.h3("📰 Market News & Sentiment", style="color:#00E6A8;"),
                    
#                     ui.layout_columns(
#                         ui.input_select("news_source", "News Source", 
#                                       ["All Sources", "Bloomberg", "Reuters", "CNBC", "WSJ"]),
#                         ui.input_select("sentiment_filter", "Sentiment Filter",
#                                       ["All", "Positive", "Neutral", "Negative"]),
#                         ui.input_action_button("refresh_news", "🔄 Refresh",
#                                              class_="btn btn-outline-success")
#                     ),

#                     ui.hr(),
#                     ui.h4("📊 Sentiment Overview", style="color:#00E6A8;"),
#                     ui.output_ui("sentiment_cards"),
                    
#                     ui.hr(),
#                     ui.h4("📈 Sentiment Trend", style="color:#00E6A8;"),
#                     output_widget("sentiment_chart"),

#                     ui.hr(),
#                     ui.h4("📄 Recent News", style="color:#00E6A8;"),
#                     ui.output_data_frame("news_table")
#                 )
#             )
#         )
#     )


# def make_about_panel() -> ui.nav_panel:
#     return ui.nav_panel(
#         "About",
#         ui.layout_columns(
#             ui.column(
#                 12,
#                 ui.card(
#                     ui.h3("ℹ️ About HedgeHub", style="color:#00E6A8;"),
#                     ui.hr(),
                    
#                     ui.div(
#                         ui.h5("🎓 Developed by Duke FinTech", style="color:#00E6A8;"),
#                         ui.p("A cutting-edge pair trading analysis platform built by students at Duke University's FinTech program.",
#                              style="color:#CCCCCC; margin: 20px 0;"),
                        
#                         ui.h5("📧 Contact Information", style="color:#00E6A8; margin-top: 30px;"),
#                         ui.p("Email: jl1319@duke.edu", style="color:#CCCCCC;"),
#                         ui.p("GitHub: github.com/duke-fintech/hedgehub", style="color:#CCCCCC;"),
                        
#                         ui.h5("⚠️ Disclaimer", style="color:#FFA500; margin-top: 30px;"),
#                         ui.p("This platform is for educational and research purposes only. Not financial advice. Always consult with qualified financial advisors before making investment decisions.",
#                              style="color:#CCCCCC; font-style: italic;"),
                        
#                         ui.hr(),
#                         ui.p("© 2025 HedgeHub Analytics | All Rights Reserved", 
#                              class_="text-center", 
#                              style="color:#999; margin-top: 30px;")
#                     )
#                 )
#             )
#         )
#     )


# # ---------------------------------------------------------
# # GLOBAL CSS + Layout
# # ---------------------------------------------------------

# app_ui = ui.page_fillable(
#     ui.tags.head(
#         ui.tags.link(
#             href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600&display=swap",
#             rel="stylesheet"
#         ),

#         ui.tags.style("""
#             /* ------ Global Styles ------ */
#             * {
#                 box-sizing: border-box;
#             }
            
#             body {
#                 background: linear-gradient(180deg, #0A1414 0%, #0F1F1F 50%, #0A1414 100%);
#                 color: #CCCCCC;
#                 font-family: 'Inter', sans-serif;
#                 min-height: 100vh;
#             }

#             /* ------ Fix all labels and text ------ */
#             label {
#                 color: #CCCCCC !important;
#                 font-weight: 500;
#             }

#             .shiny-output-text-verbatim {
#                 color: #00E6A8 !important;
#                 background: rgba(0,230,168,0.05) !important;
#                 border: 1px solid rgba(0,230,168,0.2) !important;
#                 border-radius: 8px;
#                 padding: 15px;
#                 font-family: 'Courier New', monospace;
#             }

#             /* ------ Tables ------ */
#             table, th, td, .dataframe, .dataframe th, .dataframe td {
#                 color: #CCCCCC !important;
#                 background: transparent !important;
#             }
            
#             .dataframe {
#                 border-radius: 8px;
#                 overflow: hidden;
#             }
            
#             .dataframe thead {
#                 background: rgba(0,230,168,0.1) !important;
#             }

#             /* ------ Navigation ------ */
#             .navbar {
#                 background: linear-gradient(90deg, #0A1414 0%, #0F1F1F 100%) !important;
#                 border-bottom: 2px solid rgba(0,230,168,0.3);
#                 padding: 1rem 2rem !important;
#                 box-shadow: 0 2px 20px rgba(0,230,168,0.1);
#             }

#             .nav-link { 
#                 color: #B0B0B0 !important; 
#                 transition: all 0.3s ease;
#                 font-weight: 500;
#                 position: relative;
#             }
            
#             .nav-link:hover { 
#                 color:#00E6A8 !important; 
#                 transform: translateY(-2px);
#             }
            
#             .nav-link.active { 
#                 color:#00E6A8 !important;
#             }
            
#             .nav-link.active::after {
#                 content: '';
#                 position: absolute;
#                 bottom: -2px;
#                 left: 0;
#                 right: 0;
#                 height: 3px;
#                 background: linear-gradient(90deg, transparent, #00E6A8, transparent);
#                 animation: glow 2s ease-in-out infinite;
#             }

#             /* ------ Cards ------ */
#             .card {
#                 background: rgba(255, 255, 255, 0.03) !important;
#                 border: 1px solid rgba(255, 255, 255, 0.1);
#                 border-radius: 12px;
#                 padding: 20px;
#                 backdrop-filter: blur(10px);
#                 transition: all 0.3s ease;
#             }
            
#             .card:hover {
#                 background: rgba(255, 255, 255, 0.05) !important;
#                 border-color: rgba(0,230,168,0.3);
#                 box-shadow: 0 4px 20px rgba(0,230,168,0.1);
#             }

#             /* ------ Headings ------ */
#             h1, h2, h3, h4, h5 { 
#                 color:#00E6A8;
#                 font-family: 'Poppins', sans-serif;
#             }
            
#             p { 
#                 color:#CCCCCC !important;
#                 line-height: 1.6;
#             }

#             /* ------ Buttons ------ */
#             .btn-success {
#                 background: linear-gradient(135deg, #00E6A8 0%, #00B088 100%);
#                 border: none;
#                 color: #0A1414;
#                 font-weight: 600;
#                 transition: all 0.3s ease;
#                 box-shadow: 0 4px 15px rgba(0,230,168,0.3);
#             }
            
#             .btn-success:hover {
#                 transform: translateY(-2px);
#                 box-shadow: 0 6px 25px rgba(0,230,168,0.5);
#             }
            
#             .btn-outline-success {
#                 border: 2px solid #00E6A8;
#                 color: #00E6A8;
#                 background: transparent;
#                 transition: all 0.3s ease;
#             }
            
#             .btn-outline-success:hover {
#                 background: rgba(0,230,168,0.1);
#                 transform: translateY(-2px);
#             }

#             /* ------ Inputs ------ */
#             input, select, textarea {
#                 background: rgba(255,255,255,0.05) !important;
#                 border: 1px solid rgba(0,230,168,0.3) !important;
#                 color: #CCCCCC !important;
#                 border-radius: 6px;
#                 padding: 8px 12px;
#                 transition: all 0.3s ease;
#             }
            
#             input:focus, select:focus, textarea:focus {
#                 background: rgba(255,255,255,0.08) !important;
#                 border-color: #00E6A8 !important;
#                 box-shadow: 0 0 10px rgba(0,230,168,0.3);
#                 outline: none;
#             }

#             /* ------ Tabs ------ */
#             .nav-tabs {
#                 border-bottom: 1px solid rgba(0,230,168,0.2);
#             }
            
#             .nav-tabs .nav-link {
#                 border: none;
#                 color: #999;
#                 background: transparent;
#                 transition: all 0.3s ease;
#             }
            
#             .nav-tabs .nav-link:hover {
#                 border: none;
#                 color: #00E6A8;
#                 background: rgba(0,230,168,0.05);
#             }
            
#             .nav-tabs .nav-link.active {
#                 background: rgba(0,230,168,0.1);
#                 border: none;
#                 border-bottom: 3px solid #00E6A8;
#                 color: #00E6A8;
#             }

#             /* ------ Animations ------ */
#             @keyframes glow {
#                 0%, 100% { opacity: 0.5; }
#                 50% { opacity: 1; }
#             }
            
#             @keyframes pulse {
#                 0%, 100% { transform: scale(1); }
#                 50% { transform: scale(1.05); }
#             }

#             /* ------ Scrollbar ------ */
#             ::-webkit-scrollbar {
#                 width: 10px;
#                 height: 10px;
#             }
            
#             ::-webkit-scrollbar-track {
#                 background: rgba(255,255,255,0.05);
#             }
            
#             ::-webkit-scrollbar-thumb {
#                 background: rgba(0,230,168,0.3);
#                 border-radius: 5px;
#             }
            
#             ::-webkit-scrollbar-thumb:hover {
#                 background: rgba(0,230,168,0.5);
#             }
#         """)
#     ),

#     ui.page_navbar(
#         make_home_panel(),
#         make_pair_panel(),
#         make_strategy_panel(),
#         make_news_panel(),
#         make_about_panel(),

#         title=ui.tags.div(
#             {"class": "custom-navbar"},
#             ui.tags.div(
#                 {"class": "nav-left", "style": "display: flex; align-items: center;"},
#                 ui.tags.span("💹", style="font-size:1.8rem; margin-right:10px; animation: pulse 2s infinite;"),
#                 ui.tags.span("HedgeHub", {"style": "font-family: 'Poppins', sans-serif; font-size: 1.5rem; font-weight: 600; color: #00E6A8;"})
#             )
#         )
#     )
# )


# # ---------------------------------------------------------
# # SERVER
# # ---------------------------------------------------------

# def server(input, output, session):
    
#     # 存储分析结果
#     analysis_results = reactive.Value({})
    
#     # ----- Pair Analysis Functions -----
    
#     # 状态卡片
#     @output
#     @render.ui
#     def status_cards():
#         if not analysis_results():
#             return ui.div(
#                 ui.h5("⏳ Waiting for analysis...", style="color: #999; text-align: center;")
#             )
        
#         return ui.layout_columns(
#             ui.card(
#                 ui.h6("Status", style="color: #999; margin: 0;"),
#                 ui.h4("✅ Strong Pair", style="color: #00E6A8; margin: 5px 0;"),
#                 style="background: rgba(0,230,168,0.05); text-align: center;"
#             ),
#             ui.card(
#                 ui.h6("P-Value", style="color: #999; margin: 0;"),
#                 ui.h4("0.0234", style="color: #00E6A8; margin: 5px 0;"),
#                 style="background: rgba(0,230,168,0.05); text-align: center;"
#             ),
#             ui.card(
#                 ui.h6("Correlation", style="color: #999; margin: 0;"),
#                 ui.h4("87.6%", style="color: #00E6A8; margin: 5px 0;"),
#                 style="background: rgba(0,230,168,0.05); text-align: center;"
#             ),
#             ui.card(
#                 ui.h6("Half-life", style="color: #999; margin: 0;"),
#                 ui.h4("15.2 days", style="color: #00E6A8; margin: 5px 0;"),
#                 style="background: rgba(0,230,168,0.05); text-align: center;"
#             )
#         )
    
#     # 价格走势图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def price_chart():
#         ticker_a = input.stock_a() or "AAPL"
#         ticker_b = input.stock_b() or "MSFT"
        
#         dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='D')
#         price_a = 100 * (1 + np.random.randn(len(dates)).cumsum() * 0.01)
#         price_b = 100 * (1 + np.random.randn(len(dates)).cumsum() * 0.01)
        
#         fig = make_subplots(
#             rows=2, cols=1,
#             row_heights=[0.7, 0.3],
#             shared_xaxes=True,
#             vertical_spacing=0.05,
#             subplot_titles=("Normalized Prices", "Price Ratio")
#         )
        
#         fig.add_trace(
#             go.Scatter(
#                 x=dates, 
#                 y=price_a/price_a[0]*100,
#                 name=ticker_a,
#                 line=dict(color='#00E6A8', width=2)
#             ),
#             row=1, col=1
#         )
        
#         fig.add_trace(
#             go.Scatter(
#                 x=dates,
#                 y=price_b/price_b[0]*100,
#                 name=ticker_b,
#                 line=dict(color='#FF6B6B', width=2)
#             ),
#             row=1, col=1
#         )
        
#         fig.add_trace(
#             go.Scatter(
#                 x=dates,
#                 y=price_a/price_b,
#                 name=f"{ticker_a}/{ticker_b}",
#                 line=dict(color='#FFA500', width=1.5),
#                 showlegend=False
#             ),
#             row=2, col=1
#         )
        
#         fig.update_layout(
#             height=600,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC'),
#             hovermode='x unified'
#         )
        
#         fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
#         fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
#         analysis_results.set({'status': 'completed'})
        
#         return fig
    
#     # 价差分析图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def spread_chart():
#         dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='D')
#         spread = np.random.randn(len(dates)).cumsum()
#         mean = spread.mean()
#         std = spread.std()
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=spread,
#             name='Spread',
#             line=dict(color='#00E6A8', width=2)
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=[mean]*len(dates),
#             name='Mean',
#             line=dict(color='white', width=1, dash='dash')
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=[mean + 2*std]*len(dates),
#             name='+2σ',
#             line=dict(color='#FF6B6B', width=1, dash='dot')
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=[mean - 2*std]*len(dates),
#             name='-2σ',
#             line=dict(color='#FF6B6B', width=1, dash='dot'),
#             fill='tonexty',
#             fillcolor='rgba(255,107,107,0.05)'
#         ))
        
#         fig.update_layout(
#             title="Spread with Trading Bands",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
#         fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
#         return fig
    
#     # 价差分布图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def spread_distribution():
#         spread = np.random.randn(1000)
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Histogram(
#             x=spread,
#             nbinsx=30,
#             name='Distribution',
#             marker=dict(color='#00E6A8', line=dict(color='#00B088', width=1)),
#             opacity=0.7
#         ))
        
#         fig.update_layout(
#             title="Spread Distribution",
#             height=300,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         return fig
    
#     # 相关性图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def correlation_chart():
#         x = np.random.randn(500)
#         y = 0.7 * x + 0.3 * np.random.randn(500)
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=x,
#             y=y,
#             mode='markers',
#             name='Returns',
#             marker=dict(color='#00E6A8', size=5, opacity=0.6)
#         ))
        
#         z = np.polyfit(x, y, 1)
#         p = np.poly1d(z)
#         x_line = np.linspace(x.min(), x.max(), 100)
        
#         fig.add_trace(go.Scatter(
#             x=x_line,
#             y=p(x_line),
#             name='Regression',
#             line=dict(color='#FF6B6B', width=2)
#         ))
        
#         fig.update_layout(
#             title="Return Correlation",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
#         fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
#         return fig
    
#     # 滚动相关性
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def rolling_correlation():
#         dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='D')
#         correlation = 0.7 + 0.2 * np.sin(np.linspace(0, 4*np.pi, len(dates))) + 0.05 * np.random.randn(len(dates))
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=correlation,
#             name='30-day Rolling',
#             line=dict(color='#00E6A8', width=2),
#             fill='tozeroy',
#             fillcolor='rgba(0,230,168,0.1)'
#         ))
        
#         fig.update_layout(
#             title="Rolling Correlation",
#             height=350,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         return fig
    
#     # 交易信号图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def signals_chart():
#         dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='D')
#         z_score = np.random.randn(len(dates)).cumsum() * 0.5
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=z_score,
#             name='Z-Score',
#             line=dict(color='#00E6A8', width=2)
#         ))
        
#         fig.add_hline(y=2, line_dash="dash", line_color="#FF6B6B")
#         fig.add_hline(y=-2, line_dash="dash", line_color="#00E6A8")
#         fig.add_hline(y=0, line_dash="solid", line_color="white", line_width=0.5)
        
#         fig.update_layout(
#             title="Trading Signals",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         return fig
    
#     # 风险热力图
#     @output
#     @render_widget
#     @reactive.event(input.run_analysis)
#     def risk_heatmap():
#         metrics = ['Returns', 'Volatility', 'Sharpe', 'Max DD', 'VaR']
#         data = np.random.rand(5, 5)
#         np.fill_diagonal(data, 1)
#         data = (data + data.T) / 2
        
#         fig = go.Figure(data=go.Heatmap(
#             z=data,
#             x=metrics,
#             y=metrics,
#             colorscale='Viridis',
#             text=np.round(data, 2),
#             texttemplate='%{text}'
#         ))
        
#         fig.update_layout(
#             title="Risk Correlation Matrix",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         return fig
    
#     # 协整检验结果
#     @output
#     @render.text
#     @reactive.event(input.run_analysis)
#     def cointegration_result():
#         return f"""
# ╔════════════════════════════════════════════════════════════════╗
# ║                 COINTEGRATION TEST RESULTS                     ║
# ╠════════════════════════════════════════════════════════════════╣
# ║ Method: {input.cointegration_method()}                         ║
# ║ Confidence Level: {input.confidence_level()}%                  ║
# ╠════════════════════════════════════════════════════════════════╣
# ║ Test Statistic: -3.456                                        ║
# ║ P-Value: 0.0234                                               ║
# ║ Critical Values:                                              ║
# ║   1%: -3.961    5%: -3.365    10%: -3.066                    ║
# ╠════════════════════════════════════════════════════════════════╣
# ║ ✅ Result: Cointegration detected at 5% significance          ║
# ╚════════════════════════════════════════════════════════════════╝
#         """
    
#     # 最近信号表格
#     @output
#     @render.data_frame
#     @reactive.event(input.run_analysis)
#     def recent_signals():
#         return pd.DataFrame({
#             'Date': ['2024-11-25', '2024-11-26', '2024-11-27', '2024-11-28', '2024-11-29'],
#             'Signal': ['BUY', 'HOLD', 'SELL', 'BUY', 'HOLD'],
#             'Z-Score': ['-2.15', '0.34', '2.28', '-1.89', '0.12'],
#             'Confidence': ['High', 'Low', 'High', 'Medium', 'Low']
#         })
    
#     # 价格统计
#     @output
#     @render.ui
#     def price_statistics():
#         stock_a = input.stock_a() or "Stock A"
#         stock_b = input.stock_b() or "Stock B"
        
#         return ui.layout_columns(
#             ui.card(
#                 ui.h6(f"{stock_a}", style="color:#00E6A8;"),
#                 ui.p("Price: $150.23", style="color:#CCCCCC;"),
#                 ui.p("Change: +2.34%", style="color:#00E6A8;")
#             ),
#             ui.card(
#                 ui.h6(f"{stock_b}", style="color:#00E6A8;"),
#                 ui.p("Price: $280.45", style="color:#CCCCCC;"),
#                 ui.p("Change: +1.87%", style="color:#00E6A8;")
#             ),
#             ui.card(
#                 ui.h6("Pair Stats", style="color:#00E6A8;"),
#                 ui.p("Correlation: 0.876", style="color:#CCCCCC;"),
#                 ui.p("Beta: 1.234", style="color:#CCCCCC;")
#             )
#         )
    
#     # 风险指标卡片
#     @output
#     @render.ui
#     def risk_metrics_cards():
#         return ui.layout_columns(
#             ui.card(
#                 ui.h6("Risk", style="color:#FFA500;"),
#                 ui.p("VaR (95%): -2.34%", style="color:#CCCCCC;"),
#                 ui.p("Max DD: -8.5%", style="color:#FF6B6B;")
#             ),
#             ui.card(
#                 ui.h6("Performance", style="color:#00E6A8;"),
#                 ui.p("Sharpe: 1.45", style="color:#CCCCCC;"),
#                 ui.p("Sortino: 1.82", style="color:#CCCCCC;")
#             ),
#             ui.card(
#                 ui.h6("Stability", style="color:#00E6A8;"),
#                 ui.p("Stability: 0.92", style="color:#CCCCCC;"),
#                 ui.p("Omega: 1.38", style="color:#CCCCCC;")
#             )
#         )
    
#     # ----- Strategy Panel Functions -----
    
#     @output
#     @render.text
#     def strategy_output():
#         amt = input.investment_amount()
#         risk = input.risk_level()
#         return f"""
# Strategy Generated Successfully!
# ════════════════════════════════════
# Investment: ${amt:,}
# Risk Level: {risk}
# Expected Return: 12.5% annually
# Sharpe Ratio: 1.45
# Maximum Drawdown: -8.5%
# ════════════════════════════════════
# Recommended Allocation:
# - Long Position: 60% ({0.6*amt:,.0f})
# - Short Position: 40% ({0.4*amt:,.0f})
#         """

#     @output
#     @render_widget
#     def strategy_chart():
#         days = np.arange(1, 101)
#         balance = 10000 * (1 + 0.001 * days + 0.01 * np.random.randn(100).cumsum())
        
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x=days,
#             y=balance,
#             name='Portfolio Value',
#             line=dict(color='#00E6A8', width=2),
#             fill='tozeroy',
#             fillcolor='rgba(0,230,168,0.1)'
#         ))
        
#         fig.update_layout(
#             title="Projected Portfolio Performance",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC')
#         )
        
#         return fig

#     # ----- News Panel Functions -----
    
#     @output
#     @render.ui
#     def sentiment_cards():
#         return ui.layout_columns(
#             ui.card(
#                 ui.h3("😊 60%", style="color:#00E6A8; text-align:center;"),
#                 ui.p("Positive", style="text-align:center;")
#             ),
#             ui.card(
#                 ui.h3("😐 30%", style="color:#FFA500; text-align:center;"),
#                 ui.p("Neutral", style="text-align:center;")
#             ),
#             ui.card(
#                 ui.h3("😔 10%", style="color:#FF6B6B; text-align:center;"),
#                 ui.p("Negative", style="text-align:center;")
#             )
#         )
    
#     @output
#     @render.data_frame
#     def news_table():
#         return pd.DataFrame({
#             "Time": ["10:30", "09:15", "08:45", "Yesterday", "Yesterday"],
#             "Headline": [
#                 "Tech stocks rally on AI optimism",
#                 "Fed signals potential rate pause",
#                 "Energy sector gains amid supply concerns",
#                 "Market closes higher for third day",
#                 "Earnings beat expectations across sectors"
#             ],
#             "Source": ["Bloomberg", "Reuters", "CNBC", "WSJ", "FT"],
#             "Sentiment": ["Positive", "Neutral", "Positive", "Positive", "Positive"],
#             "Impact": ["High", "High", "Medium", "Low", "Medium"]
#         })

#     @output
#     @render_widget
#     def sentiment_chart():
#         dates = pd.date_range(start='2024-11-01', end='2024-11-30', freq='D')
#         positive = 50 + 10 * np.sin(np.linspace(0, 2*np.pi, 30)) + np.random.randn(30) * 5
#         neutral = 30 + 5 * np.cos(np.linspace(0, 2*np.pi, 30)) + np.random.randn(30) * 3
#         negative = 20 - 5 * np.sin(np.linspace(0, 2*np.pi, 30)) + np.random.randn(30) * 2
        
#         fig = go.Figure()
        
#         fig.add_trace(go.Scatter(
#             x=dates, y=positive,
#             name='Positive',
#             line=dict(color='#00E6A8', width=2)
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=dates, y=neutral,
#             name='Neutral',
#             line=dict(color='#FFA500', width=2)
#         ))
        
#         fig.add_trace(go.Scatter(
#             x=dates, y=negative,
#             name='Negative',
#             line=dict(color='#FF6B6B', width=2)
#         ))
        
#         fig.update_layout(
#             title="Sentiment Trend (30 Days)",
#             height=400,
#             plot_bgcolor='#0F1A1A',
#             paper_bgcolor='#0F1A1A',
#             font=dict(color='#CCCCCC'),
#             yaxis_title="Percentage (%)"
#         )
        
#         return fig


# # ---------------------------------------------------------
# # RUN APP
# # ---------------------------------------------------------

# app = App(app_ui, server)

# if __name__ == "__main__":
#     app.run()

from shiny import App, ui, render, reactive, req
from shinywidgets import output_widget, render_widget
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import OLS
import warnings
warnings.filterwarnings('ignore')

# ========================================================
# HELPER FUNCTIONS & CALCULATIONS
# ========================================================

class PairTradingEngine:
    """配对交易核心引擎"""
    
    def __init__(self):
        self.data = {}
        self.signals = pd.DataFrame()
        
    def fetch_data(self, ticker1, ticker2, start_date, end_date):
        """获取股票数据"""
        try:
            stock1 = yf.download(ticker1, start=start_date, end=end_date, progress=False)
            stock2 = yf.download(ticker2, start=start_date, end=end_date, progress=False)
            
            if len(stock1) == 0 or len(stock2) == 0:
                return None, "Failed to fetch data. Please check tickers."
            
            # 对齐数据
            df = pd.DataFrame({
                f'{ticker1}_price': stock1['Close'],
                f'{ticker2}_price': stock2['Close'],
                f'{ticker1}_returns': stock1['Close'].pct_change(),
                f'{ticker2}_returns': stock2['Close'].pct_change()
            }).dropna()
            
            self.data = {
                'ticker1': ticker1,
                'ticker2': ticker2,
                'prices': df,
                'start': start_date,
                'end': end_date
            }
            
            return df, None
            
        except Exception as e:
            return None, str(e)
    
    def test_cointegration(self, prices_df, ticker1, ticker2):
        """协整检验"""
        try:
            price1 = prices_df[f'{ticker1}_price']
            price2 = prices_df[f'{ticker2}_price']
            
            # Engle-Granger协整检验
            score, p_value, _ = coint(price1, price2)
            
            # 计算hedge ratio
            model = OLS(price1, price2).fit()
            hedge_ratio = model.params[0]
            
            # 计算spread
            spread = price1 - hedge_ratio * price2
            
            # ADF检验spread的平稳性
            adf_result = adfuller(spread)
            
            # 计算半衰期
            spread_lag = spread.shift(1)
            spread_diff = spread - spread_lag
            spread_model = OLS(spread_diff[1:], spread_lag[1:]).fit()
            halflife = -np.log(2) / spread_model.params[0] if spread_model.params[0] < 0 else np.inf
            
            results = {
                'p_value': p_value,
                'test_statistic': score,
                'hedge_ratio': hedge_ratio,
                'spread': spread,
                'adf_statistic': adf_result[0],
                'adf_pvalue': adf_result[1],
                'halflife': halflife,
                'cointegrated': p_value < 0.05,
                'spread_mean': spread.mean(),
                'spread_std': spread.std()
            }
            
            return results
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_signals(self, spread, entry_threshold=2, exit_threshold=0.5):
        """生成交易信号"""
        z_score = (spread - spread.mean()) / spread.std()
        
        signals = pd.DataFrame(index=spread.index)
        signals['spread'] = spread
        signals['z_score'] = z_score
        signals['position'] = 0
        
        # 生成信号
        signals.loc[z_score > entry_threshold, 'position'] = -1  # Short spread
        signals.loc[z_score < -entry_threshold, 'position'] = 1  # Long spread
        signals.loc[abs(z_score) < exit_threshold, 'position'] = 0  # Exit
        
        # 前向填充保持持仓
        signals['position'] = signals['position'].replace(0, np.nan).ffill().fillna(0)
        
        # 标记交易点
        signals['trade'] = signals['position'].diff()
        signals.loc[signals['trade'] > 0, 'signal'] = 'BUY'
        signals.loc[signals['trade'] < 0, 'signal'] = 'SELL'
        signals.loc[signals['position'] == 0, 'signal'] = 'EXIT'
        
        self.signals = signals
        return signals
    
    def backtest(self, prices_df, signals, ticker1, ticker2, initial_capital=100000):
        """回测策略"""
        portfolio = pd.DataFrame(index=signals.index)
        
        # 价格数据
        portfolio['price1'] = prices_df[f'{ticker1}_price']
        portfolio['price2'] = prices_df[f'{ticker2}_price']
        
        # 持仓
        portfolio['position'] = signals['position']
        
        # 计算每日收益
        portfolio['returns1'] = portfolio['price1'].pct_change()
        portfolio['returns2'] = portfolio['price2'].pct_change()
        
        # 策略收益（long-short portfolio）
        portfolio['strategy_returns'] = (
            portfolio['position'].shift(1) * (portfolio['returns1'] - portfolio['returns2'])
        )
        
        # 累计收益
        portfolio['cumulative_returns'] = (1 + portfolio['strategy_returns']).cumprod()
        portfolio['cumulative_value'] = initial_capital * portfolio['cumulative_returns']
        
        # 计算统计指标
        total_return = portfolio['cumulative_returns'].iloc[-1] - 1
        annualized_return = (1 + total_return) ** (252 / len(portfolio)) - 1
        volatility = portfolio['strategy_returns'].std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
        
        # 最大回撤
        cum_returns = portfolio['cumulative_returns']
        running_max = cum_returns.expanding().max()
        drawdown = (cum_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # 交易统计
        trades = signals[signals['trade'] != 0]
        num_trades = len(trades)
        
        metrics = {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'num_trades': num_trades,
            'final_value': portfolio['cumulative_value'].iloc[-1]
        }
        
        return portfolio, metrics

# 初始化引擎
engine = PairTradingEngine()

# ========================================================
# UI COMPONENTS
# ========================================================

def make_sidebar():
    """创建侧边栏配置面板"""
    return ui.sidebar(
        ui.h3("⚙️ Configuration", style="color: #00E6A8;"),
        
        # 股票选择
        ui.card(
            ui.h5("📈 Stock Selection", style="color: #00E6A8;"),
            ui.input_text("ticker1", "Stock 1", value="AAPL", placeholder="e.g., AAPL"),
            ui.input_text("ticker2", "Stock 2", value="MSFT", placeholder="e.g., MSFT"),
            ui.input_action_button(
                "suggest_pairs", 
                "🔍 Suggest Pairs", 
                class_="btn btn-sm btn-outline-info w-100 mt-2"
            ),
            style="background: rgba(0,230,168,0.05);"
        ),
        
        # 时间范围
        ui.card(
            ui.h5("📅 Time Period", style="color: #00E6A8;"),
            ui.input_date_range(
                "date_range",
                "Date Range",
                start=datetime.now() - timedelta(days=365),
                end=datetime.now()
            ),
            ui.input_radio_buttons(
                "period_preset",
                "Quick Select",
                {
                    "3m": "3 Months",
                    "6m": "6 Months",
                    "1y": "1 Year",
                    "2y": "2 Years",
                    "5y": "5 Years",
                    "custom": "Custom"
                },
                selected="1y"
            ),
            style="background: rgba(0,230,168,0.05);"
        ),
        
        # 策略参数
        ui.card(
            ui.h5("🎯 Strategy Parameters", style="color: #00E6A8;"),
            ui.input_slider(
                "entry_threshold",
                "Entry Z-Score",
                min=1.0,
                max=3.0,
                value=2.0,
                step=0.1
            ),
            ui.input_slider(
                "exit_threshold",
                "Exit Z-Score",
                min=0.0,
                max=1.0,
                value=0.5,
                step=0.1
            ),
            ui.input_numeric(
                "lookback_period",
                "Lookback Period (days)",
                value=60,
                min=20,
                max=252
            ),
            ui.input_select(
                "signal_type",
                "Signal Type",
                ["Z-Score", "Bollinger Bands", "Kalman Filter"],
                selected="Z-Score"
            ),
            style="background: rgba(0,230,168,0.05);"
        ),
        
        # 风险管理
        ui.card(
            ui.h5("⚠️ Risk Management", style="color: #00E6A8;"),
            ui.input_numeric(
                "initial_capital",
                "Initial Capital ($)",
                value=100000,
                min=1000
            ),
            ui.input_slider(
                "position_size",
                "Position Size (%)",
                min=10,
                max=100,
                value=50,
                step=5
            ),
            ui.input_numeric(
                "stop_loss",
                "Stop Loss (%)",
                value=5,
                min=1,
                max=20
            ),
            ui.input_checkbox(
                "use_leverage",
                "Enable Leverage",
                value=False
            ),
            ui.panel_conditional(
                "input.use_leverage",
                ui.input_slider(
                    "leverage_ratio",
                    "Leverage Ratio",
                    min=1,
                    max=5,
                    value=2,
                    step=0.5
                )
            ),
            style="background: rgba(0,230,168,0.05);"
        ),
        
        # 执行按钮
        ui.div(
            ui.input_action_button(
                "run_analysis",
                "🚀 Run Analysis",
                class_="btn btn-success btn-lg w-100",
                style="background: linear-gradient(135deg, #00E6A8, #00B088); border: none; font-weight: 600;"
            ),
            ui.input_action_button(
                "reset_all",
                "↻ Reset",
                class_="btn btn-outline-secondary btn-sm w-100 mt-2"
            ),
            style="margin-top: 20px;"
        ),
        
        width="300px",
        style="background: #0F1A1A; border-right: 1px solid rgba(0,230,168,0.2);"
    )

def make_main_panel():
    """创建主面板"""
    return [
        # 顶部状态栏
        ui.div(
            ui.output_ui("status_bar"),
            style="margin-bottom: 20px;"
        ),
        
        # 标签页内容
        ui.navset_card_tab(
            # 数据概览
            ui.nav_panel(
                "📊 Data Overview",
                ui.layout_columns(
                    ui.column(
                        12,
                        output_widget("price_comparison_chart"),
                        ui.hr(),
                        ui.output_ui("data_statistics")
                    )
                )
            ),
            
            # 协整分析
            ui.nav_panel(
                "🔬 Cointegration Analysis",
                ui.layout_columns(
                    ui.column(
                        8,
                        output_widget("spread_chart"),
                        output_widget("zscore_chart")
                    ),
                    ui.column(
                        4,
                        ui.output_ui("cointegration_results"),
                        output_widget("spread_histogram"),
                        output_widget("qq_plot")
                    )
                )
            ),
            
            # 交易信号
            ui.nav_panel(
                "📈 Trading Signals",
                ui.layout_columns(
                    ui.column(
                        12,
                        output_widget("signal_chart"),
                        ui.hr(),
                        ui.output_data_frame("signal_table"),
                        ui.output_ui("current_signal_card")
                    )
                )
            ),
            
            # 回测结果
            ui.nav_panel(
                "💰 Backtest Results",
                ui.layout_columns(
                    ui.column(
                        8,
                        output_widget("portfolio_chart"),
                        output_widget("drawdown_chart")
                    ),
                    ui.column(
                        4,
                        ui.output_ui("backtest_metrics"),
                        output_widget("monthly_returns_heatmap")
                    )
                )
            ),
            
            # 风险分析
            ui.nav_panel(
                "⚠️ Risk Analysis",
                ui.layout_columns(
                    ui.column(
                        6,
                        output_widget("var_chart"),
                        output_widget("rolling_volatility_chart")
                    ),
                    ui.column(
                        6,
                        output_widget("correlation_heatmap"),
                        ui.output_ui("risk_metrics_table")
                    )
                )
            ),
            
            # 实时监控
            ui.nav_panel(
                "🔴 Live Monitor",
                ui.layout_columns(
                    ui.column(
                        12,
                        ui.output_ui("live_status"),
                        output_widget("live_spread_chart"),
                        ui.output_ui("alert_panel")
                    )
                )
            )
        ),
        
        # 底部操作栏
        ui.div(
            ui.layout_columns(
                ui.download_button(
                    "download_report",
                    "📥 Download Report",
                    class_="btn btn-outline-success"
                ),
                ui.download_button(
                    "export_signals",
                    "📊 Export Signals",
                    class_="btn btn-outline-info"
                ),
                ui.input_action_button(
                    "save_strategy",
                    "💾 Save Strategy",
                    class_="btn btn-outline-warning"
                ),
                ui.input_action_button(
                    "schedule_alerts",
                    "🔔 Set Alerts",
                    class_="btn btn-outline-danger"
                )
            ),
            style="margin-top: 20px; padding: 15px; background: rgba(0,230,168,0.05); border-radius: 8px;"
        )
    ]

# ========================================================
# UI LAYOUT
# ========================================================

app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap",
            rel="stylesheet"
        ),
        ui.tags.style("""
            /* Global Styles */
            body {
                background: linear-gradient(135deg, #0A1414 0%, #0F1F1F 100%);
                color: #CCCCCC;
                font-family: 'Inter', sans-serif;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5 {
                color: #00E6A8;
                font-weight: 600;
            }
            
            /* Cards */
            .card {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(0, 230, 168, 0.2) !important;
                border-radius: 12px;
                backdrop-filter: blur(10px);
            }
            
            .card:hover {
                background: rgba(255, 255, 255, 0.05) !important;
                box-shadow: 0 8px 32px rgba(0, 230, 168, 0.1);
            }
            
            /* Inputs */
            input, select, textarea {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(0, 230, 168, 0.3) !important;
                color: #CCCCCC !important;
                border-radius: 6px;
            }
            
            input:focus, select:focus {
                border-color: #00E6A8 !important;
                box-shadow: 0 0 0 0.2rem rgba(0, 230, 168, 0.25) !important;
            }
            
            /* Labels */
            label {
                color: #CCCCCC !important;
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            /* Buttons */
            .btn-success {
                background: linear-gradient(135deg, #00E6A8, #00B088);
                border: none;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(0, 230, 168, 0.3);
            }
            
            .btn-success:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 25px rgba(0, 230, 168, 0.4);
            }
            
            /* Tables */
            table {
                color: #CCCCCC !important;
            }
            
            thead {
                background: rgba(0, 230, 168, 0.1) !important;
            }
            
            tbody tr:hover {
                background: rgba(0, 230, 168, 0.05) !important;
            }
            
            /* Nav Tabs */
            .nav-tabs .nav-link {
                color: #999;
                border: none;
                background: transparent;
            }
            
            .nav-tabs .nav-link:hover {
                color: #00E6A8;
                background: rgba(0, 230, 168, 0.05);
            }
            
            .nav-tabs .nav-link.active {
                color: #00E6A8;
                background: rgba(0, 230, 168, 0.1);
                border-bottom: 3px solid #00E6A8;
            }
            
            /* Status Cards */
            .status-card {
                background: linear-gradient(135deg, rgba(0, 230, 168, 0.1), rgba(0, 230, 168, 0.05));
                border: 1px solid rgba(0, 230, 168, 0.3);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }
            
            /* Alerts */
            .alert-success {
                background: rgba(0, 230, 168, 0.2);
                border: 1px solid #00E6A8;
                color: #00E6A8;
            }
            
            .alert-danger {
                background: rgba(255, 107, 107, 0.2);
                border: 1px solid #FF6B6B;
                color: #FF6B6B;
            }
            
            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.05);
            }
            
            ::-webkit-scrollbar-thumb {
                background: rgba(0, 230, 168, 0.3);
                border-radius: 5px;
            }
            
            /* Animation */
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            .pulse {
                animation: pulse 2s infinite;
            }
            
            /* Code/Monospace */
            .mono {
                font-family: 'JetBrains Mono', monospace;
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 4px;
            }
        """)
    ),
    
    ui.layout_sidebar(
        make_sidebar(),
        ui.div(
            ui.h1(
                "🎯 HedgeHub Pro - Pairs Trading Platform",
                style="color: #00E6A8; margin-bottom: 10px;"
            ),
            ui.p(
                "Advanced statistical arbitrage and pairs trading analysis",
                style="color: #999; font-size: 0.9rem; margin-bottom: 20px;"
            ),
            *make_main_panel()
        )
    )
)

# ========================================================
# SERVER LOGIC
# ========================================================

def server(input, output, session):
    
    # Reactive values
    analysis_data = reactive.Value({})
    current_signals = reactive.Value(pd.DataFrame())
    backtest_results = reactive.Value({})
    
    # ==================== Event Handlers ====================
    
    @reactive.Effect
    @reactive.event(input.run_analysis)
    def run_full_analysis():
        """执行完整分析"""
        with ui.Progress(min=0, max=5) as p:
            p.set(message="Fetching data...", detail="Please wait...")
            
            # 获取数据
            ticker1 = input.ticker1()
            ticker2 = input.ticker2()
            dates = input.date_range()
            
            if not ticker1 or not ticker2 or not dates:
                ui.notification_show("Please enter both tickers and date range", type="error")
                return
            
            # Fetch data
            p.inc(1, message="Downloading price data...")
            df, error = engine.fetch_data(ticker1, ticker2, dates[0], dates[1])
            
            if error:
                ui.notification_show(f"Error: {error}", type="error")
                return
            
            # Test cointegration
            p.inc(1, message="Testing cointegration...")
            coint_results = engine.test_cointegration(df, ticker1, ticker2)
            
            # Generate signals
            p.inc(1, message="Generating trading signals...")
            signals = engine.generate_signals(
                coint_results['spread'],
                entry_threshold=input.entry_threshold(),
                exit_threshold=input.exit_threshold()
            )
            
            # Run backtest
            p.inc(1, message="Running backtest...")
            portfolio, metrics = engine.backtest(
                df, signals, ticker1, ticker2,
                initial_capital=input.initial_capital()
            )
            
            # Store results
            p.inc(1, message="Analysis complete!")
            analysis_data.set({
                'data': df,
                'cointegration': coint_results,
                'signals': signals,
                'portfolio': portfolio,
                'metrics': metrics,
                'ticker1': ticker1,
                'ticker2': ticker2
            })
            
            current_signals.set(signals)
            backtest_results.set({'portfolio': portfolio, 'metrics': metrics})
            
            ui.notification_show("Analysis completed successfully!", type="success")
    
    @reactive.Effect
    @reactive.event(input.period_preset)
    def update_date_range():
        """更新日期范围"""
        preset = input.period_preset()
        end = datetime.now()
        
        if preset == "3m":
            start = end - timedelta(days=90)
        elif preset == "6m":
            start = end - timedelta(days=180)
        elif preset == "1y":
            start = end - timedelta(days=365)
        elif preset == "2y":
            start = end - timedelta(days=730)
        elif preset == "5y":
            start = end - timedelta(days=1825)
        else:
            return
        
        ui.update_date_range("date_range", start=start, end=end)
    
    # ==================== Status Bar ====================
    
    @output
    @render.ui
    def status_bar():
        if not analysis_data():
            return ui.div(
                ui.h5("⏳ Ready to analyze. Configure parameters and click 'Run Analysis'.",
                      style="color: #999; text-align: center;")
            )
        
        data = analysis_data()
        coint = data.get('cointegration', {})
        metrics = data.get('metrics', {})
        
        if coint.get('cointegrated'):
            status_color = "#00E6A8"
            status_text = "✅ Cointegrated"
        else:
            status_color = "#FF6B6B"
            status_text = "❌ Not Cointegrated"
        
        return ui.layout_columns(
            ui.div(
                ui.h6("Pair Status", style="color: #999; margin: 0;"),
                ui.h4(status_text, style=f"color: {status_color}; margin: 5px 0;"),
                class_="status-card"
            ),
            ui.div(
                ui.h6("P-Value", style="color: #999; margin: 0;"),
                ui.h4(f"{coint.get('p_value', 0):.4f}", style="color: #00E6A8; margin: 5px 0;"),
                class_="status-card"
            ),
            ui.div(
                ui.h6("Sharpe Ratio", style="color: #999; margin: 0;"),
                ui.h4(f"{metrics.get('sharpe_ratio', 0):.2f}", style="color: #00E6A8; margin: 5px 0;"),
                class_="status-card"
            ),
            ui.div(
                ui.h6("Total Return", style="color: #999; margin: 0;"),
                ui.h4(f"{metrics.get('total_return', 0)*100:.1f}%", 
                      style=f"color: {'#00E6A8' if metrics.get('total_return', 0) > 0 else '#FF6B6B'}; margin: 5px 0;"),
                class_="status-card"
            ),
            ui.div(
                ui.h6("Max Drawdown", style="color: #999; margin: 0;"),
                ui.h4(f"{metrics.get('max_drawdown', 0)*100:.1f}%", style="color: #FF6B6B; margin: 5px 0;"),
                class_="status-card"
            ),
            ui.div(
                ui.h6("Half-life", style="color: #999; margin: 0;"),
                ui.h4(f"{coint.get('halflife', 0):.1f} days", style="color: #00E6A8; margin: 5px 0;"),
                class_="status-card"
            )
        )
    
    # ==================== Data Overview Tab ====================
    
    @output
    @render_widget
    def price_comparison_chart():
        if not analysis_data():
            return go.Figure()
        
        data = analysis_data()
        df = data['data']
        ticker1 = data['ticker1']
        ticker2 = data['ticker2']
        
        fig = make_subplots(
            rows=3, cols=1,
            row_heights=[0.4, 0.4, 0.2],
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=("Normalized Prices", "Individual Prices", "Volume")
        )
        
        # Normalized prices
        norm1 = df[f'{ticker1}_price'] / df[f'{ticker1}_price'].iloc[0] * 100
        norm2 = df[f'{ticker2}_price'] / df[f'{ticker2}_price'].iloc[0] * 100
        
        fig.add_trace(
            go.Scatter(
                x=df.index, y=norm1,
                name=ticker1,
                line=dict(color='#00E6A8', width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index, y=norm2,
                name=ticker2,
                line=dict(color='#FF6B6B', width=2)
            ),
            row=1, col=1
        )
        
        # Individual prices with dual y-axis
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'{ticker1}_price'],
                name=f'{ticker1} Price',
                line=dict(color='#00E6A8', width=1.5),
                yaxis='y2'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'{ticker2}_price'],
                name=f'{ticker2} Price',
                line=dict(color='#FF6B6B', width=1.5),
                yaxis='y3'
            ),
            row=2, col=1
        )
        
        # Volume comparison (simulated)
        volume_diff = np.random.randn(len(df)) * 1000000
        colors = ['#00E6A8' if v > 0 else '#FF6B6B' for v in volume_diff]
        
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=abs(volume_diff),
                name='Volume Diff',
                marker_color=colors,
                opacity=0.5
            ),
            row=3, col=1
        )
        
        fig.update_layout(
            height=700,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render.ui
    def data_statistics():
        if not analysis_data():
            return ui.div()
        
        data = analysis_data()
        df = data['data']
        ticker1 = data['ticker1']
        ticker2 = data['ticker2']
        
        # Calculate statistics
        stats1 = {
            'Mean Return': f"{df[f'{ticker1}_returns'].mean()*100:.3f}%",
            'Volatility': f"{df[f'{ticker1}_returns'].std()*np.sqrt(252)*100:.1f}%",
            'Skewness': f"{df[f'{ticker1}_returns'].skew():.3f}",
            'Kurtosis': f"{df[f'{ticker1}_returns'].kurtosis():.3f}"
        }
        
        stats2 = {
            'Mean Return': f"{df[f'{ticker2}_returns'].mean()*100:.3f}%",
            'Volatility': f"{df[f'{ticker2}_returns'].std()*np.sqrt(252)*100:.1f}%",
            'Skewness': f"{df[f'{ticker2}_returns'].skew():.3f}",
            'Kurtosis': f"{df[f'{ticker2}_returns'].kurtosis():.3f}"
        }
        
        correlation = df[f'{ticker1}_returns'].corr(df[f'{ticker2}_returns'])
        
        return ui.layout_columns(
            ui.card(
                ui.h5(f"📊 {ticker1} Statistics", style="color: #00E6A8;"),
                ui.tags.table(
                    ui.tags.tbody(
                        *[ui.tags.tr(
                            ui.tags.td(k, style="color: #999;"),
                            ui.tags.td(v, style="color: #CCCCCC; text-align: right;")
                        ) for k, v in stats1.items()]
                    ),
                    style="width: 100%;"
                )
            ),
            ui.card(
                ui.h5(f"📊 {ticker2} Statistics", style="color: #00E6A8;"),
                ui.tags.table(
                    ui.tags.tbody(
                        *[ui.tags.tr(
                            ui.tags.td(k, style="color: #999;"),
                            ui.tags.td(v, style="color: #CCCCCC; text-align: right;")
                        ) for k, v in stats2.items()]
                    ),
                    style="width: 100%;"
                )
            ),
            ui.card(
                ui.h5("🔗 Correlation", style="color: #00E6A8; text-align: center;"),
                ui.h2(f"{correlation:.3f}", style="color: #00E6A8; text-align: center;"),
                ui.p(f"Rolling 30d: {df[f'{ticker1}_returns'].rolling(30).corr(df[f'{ticker2}_returns']).iloc[-1]:.3f}",
                     style="color: #999; text-align: center;")
            )
        )
    
    # ==================== Cointegration Tab ====================
    
    @output
    @render_widget
    def spread_chart():
        if not analysis_data():
            return go.Figure()
        
        data = analysis_data()
        spread = data['cointegration']['spread']
        mean = spread.mean()
        std = spread.std()
        
        fig = go.Figure()
        
        # Spread line
        fig.add_trace(go.Scatter(
            x=spread.index,
            y=spread,
            name='Spread',
            line=dict(color='#00E6A8', width=2)
        ))
        
        # Mean line
        fig.add_trace(go.Scatter(
            x=spread.index,
            y=[mean]*len(spread),
            name='Mean',
            line=dict(color='white', width=1, dash='dash')
        ))
        
        # Standard deviation bands
        for i, (mult, color) in enumerate([(1, '#FFA500'), (2, '#FF6B6B')]):
            fig.add_trace(go.Scatter(
                x=spread.index,
                y=[mean + mult*std]*len(spread),
                name=f'+{mult}σ',
                line=dict(color=color, width=1, dash='dot'),
                showlegend=True
            ))
            
            fig.add_trace(go.Scatter(
                x=spread.index,
                y=[mean - mult*std]*len(spread),
                name=f'-{mult}σ',
                line=dict(color=color, width=1, dash='dot'),
                fill='tonexty' if i == 0 else None,
                fillcolor=f'rgba({255 if mult==2 else 255}, {107 if mult==2 else 165}, {107 if mult==2 else 0}, 0.05)',
                showlegend=True
            ))
        
        fig.update_layout(
            title="Spread Analysis",
            height=400,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            hovermode='x unified',
            xaxis_title="Date",
            yaxis_title="Spread Value"
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render_widget
    def zscore_chart():
        if not analysis_data():
            return go.Figure()
        
        data = analysis_data()
        signals = data['signals']
        z_score = signals['z_score']
        
        fig = go.Figure()
        
        # Z-score line with gradient fill
        fig.add_trace(go.Scatter(
            x=z_score.index,
            y=z_score,
            name='Z-Score',
            line=dict(color='#00E6A8', width=2),
            fill='tozeroy',
            fillcolor='rgba(0,230,168,0.1)'
        ))
        
        # Trading thresholds
        entry = input.entry_threshold()
        exit = input.exit_threshold()
        
        fig.add_hline(y=entry, line_dash="dash", line_color="#FF6B6B",
                     annotation_text=f"Short Entry ({entry}σ)")
        fig.add_hline(y=-entry, line_dash="dash", line_color="#00E6A8",
                     annotation_text=f"Long Entry ({-entry}σ)")
        fig.add_hline(y=exit, line_dash="dot", line_color="#FFA500",
                     annotation_text=f"Exit ({exit}σ)")
        fig.add_hline(y=-exit, line_dash="dot", line_color="#FFA500",
                     annotation_text=f"Exit ({-exit}σ)")
        fig.add_hline(y=0, line_color="white", line_width=0.5)
        
        fig.update_layout(
            title="Z-Score Evolution",
            height=350,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Date",
            yaxis_title="Z-Score"
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render.ui
    def cointegration_results():
        if not analysis_data():
            return ui.div()
        
        coint = analysis_data()['cointegration']
        
        status_color = "#00E6A8" if coint['cointegrated'] else "#FF6B6B"
        status_icon = "✅" if coint['cointegrated'] else "❌"
        
        return ui.card(
            ui.h5("🔬 Cointegration Test Results", style="color: #00E6A8;"),
            ui.hr(),
            
            ui.div(
                ui.h4(f"{status_icon} {'Cointegrated' if coint['cointegrated'] else 'Not Cointegrated'}",
                      style=f"color: {status_color}; text-align: center; margin: 15px 0;"),
                style="background: rgba(0,230,168,0.05); border-radius: 8px; padding: 10px;"
            ),
            
            ui.tags.table(
                ui.tags.tbody(
                    ui.tags.tr(
                        ui.tags.td("P-Value:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['p_value']:.6f}", 
                                  style=f"color: {status_color}; text-align: right; font-weight: bold;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Test Statistic:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['test_statistic']:.4f}", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Hedge Ratio:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['hedge_ratio']:.4f}", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Half-life:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['halflife']:.1f} days", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("ADF Statistic:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['adf_statistic']:.4f}", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("ADF P-Value:", style="color: #999; padding: 5px;"),
                        ui.tags.td(f"{coint['adf_pvalue']:.6f}", style="color: #CCCCCC; text-align: right;")
                    )
                ),
                style="width: 100%; margin-top: 15px;"
            ),
            
            style="height: 100%;"
        )
    
    @output
    @render_widget
    def spread_histogram():
        if not analysis_data():
            return go.Figure()
        
        spread = analysis_data()['cointegration']['spread']
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=spread,
            nbinsx=30,
            name='Spread Distribution',
            marker=dict(
                color='#00E6A8',
                line=dict(color='#00B088', width=1)
            ),
            opacity=0.7
        ))
        
        # Add normal distribution overlay
        x_range = np.linspace(spread.min(), spread.max(), 100)
        norm_dist = ((1 / (spread.std() * np.sqrt(2 * np.pi))) *
                    np.exp(-0.5 * ((x_range - spread.mean()) / spread.std())**2))
        norm_dist = norm_dist * len(spread) * (spread.max() - spread.min()) / 30
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=norm_dist,
            name='Normal Fit',
            line=dict(color='#FFA500', width=2)
        ))
        
        fig.update_layout(
            title="Spread Distribution",
            height=250,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            showlegend=True,
            xaxis_title="Spread",
            yaxis_title="Frequency"
        )
        
        return fig
    
    @output
    @render_widget
    def qq_plot():
        if not analysis_data():
            return go.Figure()
        
        spread = analysis_data()['cointegration']['spread']
        
        # Calculate QQ plot points
        sorted_spread = np.sort(spread)
        n = len(sorted_spread)
        theoretical_quantiles = np.array([np.percentile(np.random.randn(10000), i*100/n) for i in range(1, n+1)])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=sorted_spread,
            mode='markers',
            name='QQ Points',
            marker=dict(color='#00E6A8', size=4)
        ))
        
        # Add reference line
        min_val = min(theoretical_quantiles.min(), sorted_spread.min())
        max_val = max(theoretical_quantiles.max(), sorted_spread.max())
        
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Reference Line',
            line=dict(color='#FF6B6B', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Q-Q Plot",
            height=250,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Theoretical Quantiles",
            yaxis_title="Sample Quantiles"
        )
        
        return fig
    
    # ==================== Trading Signals Tab ====================
    
    @output
    @render_widget
    def signal_chart():
        if not analysis_data():
            return go.Figure()
        
        data = analysis_data()
        signals = data['signals']
        df = data['data']
        ticker1 = data['ticker1']
        ticker2 = data['ticker2']
        
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],
            shared_xaxes=True,
            vertical_spacing=0.05
        )
        
        # Price chart with signals
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'{ticker1}_price'] / df[f'{ticker1}_price'].iloc[0] * 100,
                name=ticker1,
                line=dict(color='#00E6A8', width=1.5)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'{ticker2}_price'] / df[f'{ticker2}_price'].iloc[0] * 100,
                name=ticker2,
                line=dict(color='#FF6B6B', width=1.5)
            ),
            row=1, col=1
        )
        
        # Add buy/sell markers
        buy_signals = signals[signals['signal'] == 'BUY']
        sell_signals = signals[signals['signal'] == 'SELL']
        
        if len(buy_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=df.loc[buy_signals.index, f'{ticker1}_price'] / df[f'{ticker1}_price'].iloc[0] * 100,
                    mode='markers',
                    name='Buy',
                    marker=dict(color='#00E6A8', size=10, symbol='triangle-up')
                ),
                row=1, col=1
            )
        
        if len(sell_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=df.loc[sell_signals.index, f'{ticker1}_price'] / df[f'{ticker1}_price'].iloc[0] * 100,
                    mode='markers',
                    name='Sell',
                    marker=dict(color='#FF6B6B', size=10, symbol='triangle-down')
                ),
                row=1, col=1
            )
        
        # Position chart
        fig.add_trace(
            go.Scatter(
                x=signals.index,
                y=signals['position'],
                name='Position',
                line=dict(color='#FFA500', width=2),
                fill='tozeroy',
                fillcolor='rgba(255,165,0,0.1)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            hovermode='x unified',
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1,
                        showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(title_text="Normalized Price", row=1, col=1,
                        showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(title_text="Position", row=2, col=1,
                        showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render.data_frame
    def signal_table():
        if not current_signals():
            return pd.DataFrame()
        
        signals = current_signals()
        
        # Get last 10 trading signals
        trade_signals = signals[signals['signal'].notna()].tail(10)
        
        if len(trade_signals) == 0:
            return pd.DataFrame({'Message': ['No trading signals generated']})
        
        display_df = pd.DataFrame({
            'Date': trade_signals.index.strftime('%Y-%m-%d'),
            'Signal': trade_signals['signal'],
            'Z-Score': trade_signals['z_score'].round(3),
            'Spread': trade_signals['spread'].round(2),
            'Position': trade_signals['position'].astype(int)
        })
        
        return display_df
    
    @output
    @render.ui
    def current_signal_card():
        if not current_signals() or len(current_signals()) == 0:
            return ui.div()
        
        signals = current_signals()
        last_signal = signals.iloc[-1]
        
        position = last_signal['position']
        z_score = last_signal['z_score']
        
        if position == 1:
            signal_text = "LONG SPREAD"
            signal_color = "#00E6A8"
            signal_icon = "📈"
        elif position == -1:
            signal_text = "SHORT SPREAD"
            signal_color = "#FF6B6B"
            signal_icon = "📉"
        else:
            signal_text = "NO POSITION"
            signal_color = "#999"
            signal_icon = "⏸️"
        
        return ui.card(
            ui.h4("Current Signal", style="color: #00E6A8; text-align: center;"),
            ui.hr(),
            ui.div(
                ui.h2(f"{signal_icon} {signal_text}",
                      style=f"color: {signal_color}; text-align: center; margin: 20px 0;"),
                ui.p(f"Z-Score: {z_score:.3f}", style="text-align: center; color: #CCCCCC;"),
                ui.p(f"Last Update: {signals.index[-1].strftime('%Y-%m-%d %H:%M')}",
                     style="text-align: center; color: #999; font-size: 0.9rem;"),
                class_="pulse" if position != 0 else ""
            ),
            style=f"background: linear-gradient(135deg, {signal_color}20, transparent);"
        )
    
    # ==================== Backtest Results Tab ====================
    
    @output
    @render_widget
    def portfolio_chart():
        if not backtest_results():
            return go.Figure()
        
        portfolio = backtest_results()['portfolio']
        
        fig = go.Figure()
        
        # Portfolio value
        fig.add_trace(go.Scatter(
            x=portfolio.index,
            y=portfolio['cumulative_value'],
            name='Portfolio Value',
            line=dict(color='#00E6A8', width=2),
            fill='tozeroy',
            fillcolor='rgba(0,230,168,0.1)'
        ))
        
        # Initial capital line
        initial = input.initial_capital()
        fig.add_hline(y=initial, line_dash="dash", line_color="#999",
                     annotation_text=f"Initial Capital: ${initial:,.0f}")
        
        fig.update_layout(
            title="Portfolio Performance",
            height=400,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render_widget
    def drawdown_chart():
        if not backtest_results():
            return go.Figure()
        
        portfolio = backtest_results()['portfolio']
        
        # Calculate drawdown
        cum_returns = portfolio['cumulative_returns']
        running_max = cum_returns.expanding().max()
        drawdown = ((cum_returns - running_max) / running_max) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown,
            name='Drawdown',
            line=dict(color='#FF6B6B', width=2),
            fill='tozeroy',
            fillcolor='rgba(255,107,107,0.2)'
        ))
        
        # Mark maximum drawdown
        max_dd_idx = drawdown.idxmin()
        max_dd_val = drawdown.min()
        
        fig.add_trace(go.Scatter(
            x=[max_dd_idx],
            y=[max_dd_val],
            mode='markers',
            name=f'Max DD: {max_dd_val:.2f}%',
            marker=dict(color='#FF0000', size=10, symbol='x')
        ))
        
        fig.update_layout(
            title="Drawdown Analysis",
            height=350,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render.ui
    def backtest_metrics():
        if not backtest_results():
            return ui.div()
        
        metrics = backtest_results()['metrics']
        
        return ui.card(
            ui.h4("📊 Performance Metrics", style="color: #00E6A8; text-align: center;"),
            ui.hr(),
            
            ui.div(
                ui.h3(f"{metrics['total_return']*100:.2f}%",
                      style=f"color: {'#00E6A8' if metrics['total_return'] > 0 else '#FF6B6B'}; text-align: center;"),
                ui.p("Total Return", style="color: #999; text-align: center; font-size: 0.9rem;"),
                style="background: rgba(0,230,168,0.05); border-radius: 8px; padding: 15px; margin: 10px 0;"
            ),
            
            ui.tags.table(
                ui.tags.tbody(
                    ui.tags.tr(
                        ui.tags.td("Annual Return:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{metrics['annualized_return']*100:.2f}%",
                                  style=f"color: {'#00E6A8' if metrics['annualized_return'] > 0 else '#FF6B6B'}; text-align: right; font-weight: bold;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Volatility:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{metrics['volatility']*100:.2f}%",
                                  style="color: #FFA500; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Sharpe Ratio:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{metrics['sharpe_ratio']:.3f}",
                                  style=f"color: {'#00E6A8' if metrics['sharpe_ratio'] > 1 else '#FFA500'}; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Max Drawdown:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{metrics['max_drawdown']*100:.2f}%",
                                  style="color: #FF6B6B; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("# Trades:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{metrics['num_trades']}",
                                  style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Final Value:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"${metrics['final_value']:,.2f}",
                                  style="color: #00E6A8; text-align: right; font-weight: bold;")
                    )
                ),
                style="width: 100%; margin-top: 15px;"
            )
        )
    
    @output
    @render_widget
    def monthly_returns_heatmap():
        if not backtest_results():
            return go.Figure()
        
        portfolio = backtest_results()['portfolio']
        
        # Calculate monthly returns
        monthly_returns = portfolio['strategy_returns'].resample('M').apply(lambda x: (1+x).prod()-1)
        
        # Reshape for heatmap
        years = monthly_returns.index.year.unique()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        heatmap_data = []
        for year in years:
            year_data = []
            for month in range(1, 13):
                try:
                    ret = monthly_returns[(monthly_returns.index.year == year) & 
                                         (monthly_returns.index.month == month)].iloc[0]
                    year_data.append(ret * 100)
                except:
                    year_data.append(np.nan)
            heatmap_data.append(year_data)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=months,
            y=years,
            colorscale='RdYlGn',
            zmid=0,
            text=[[f'{v:.1f}%' if not np.isnan(v) else '' for v in row] for row in heatmap_data],
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Return %")
        ))
        
        fig.update_layout(
            title="Monthly Returns Heatmap",
            height=300,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC')
        )
        
        return fig
    
    # ==================== Risk Analysis Tab ====================
    
    @output
    @render_widget
    def var_chart():
        if not backtest_results():
            return go.Figure()
        
        portfolio = backtest_results()['portfolio']
        returns = portfolio['strategy_returns'].dropna()
        
        # Calculate VaR and CVaR
        confidence_levels = [0.99, 0.95, 0.90]
        var_values = [np.percentile(returns, (1-cl)*100) for cl in confidence_levels]
        cvar_values = [returns[returns <= var].mean() for var in var_values]
        
        fig = go.Figure()
        
        # Returns histogram
        fig.add_trace(go.Histogram(
            x=returns * 100,
            nbinsx=50,
            name='Returns Distribution',
            marker=dict(color='#00E6A8', line=dict(color='#00B088', width=1)),
            opacity=0.7
        ))
        
        # Add VaR lines
        colors = ['#FF0000', '#FF6B6B', '#FFA500']
        for i, (cl, var, cvar) in enumerate(zip(confidence_levels, var_values, cvar_values)):
            fig.add_vline(x=var*100, line_dash="dash", line_color=colors[i],
                         annotation_text=f"VaR {cl*100:.0f}%: {var*100:.2f}%")
        
        fig.update_layout(
            title="Value at Risk Analysis",
            height=350,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Daily Returns (%)",
            yaxis_title="Frequency"
        )
        
        return fig
    
    @output
    @render_widget
    def rolling_volatility_chart():
        if not backtest_results():
            return go.Figure()
        
        portfolio = backtest_results()['portfolio']
        
        # Calculate rolling volatility
        rolling_vol_30 = portfolio['strategy_returns'].rolling(30).std() * np.sqrt(252) * 100
        rolling_vol_60 = portfolio['strategy_returns'].rolling(60).std() * np.sqrt(252) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=rolling_vol_30.index,
            y=rolling_vol_30,
            name='30-day Volatility',
            line=dict(color='#00E6A8', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=rolling_vol_60.index,
            y=rolling_vol_60,
            name='60-day Volatility',
            line=dict(color='#FFA500', width=2)
        ))
        
        # Add average line
        avg_vol = rolling_vol_30.mean()
        fig.add_hline(y=avg_vol, line_dash="dash", line_color="#999",
                     annotation_text=f"Average: {avg_vol:.1f}%")
        
        fig.update_layout(
            title="Rolling Volatility",
            height=350,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Date",
            yaxis_title="Annualized Volatility (%)"
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render_widget
    def correlation_heatmap():
        if not analysis_data():
            return go.Figure()
        
        data = analysis_data()
        df = data['data']
        ticker1 = data['ticker1']
        ticker2 = data['ticker2']
        
        # Calculate rolling correlations
        windows = [5, 10, 20, 30, 60]
        corr_matrix = []
        
        for w in windows:
            corr = df[f'{ticker1}_returns'].rolling(w).corr(df[f'{ticker2}_returns']).iloc[-1]
            corr_matrix.append([corr])
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=['Correlation'],
            y=[f'{w}d' for w in windows],
            colorscale='Viridis',
            text=[[f'{v:.3f}' for v in row] for row in corr_matrix],
            texttemplate='%{text}',
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Rolling Correlation Matrix",
            height=350,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC')
        )
        
        return fig
    
    @output
    @render.ui
    def risk_metrics_table():
        if not backtest_results():
            return ui.div()
        
        portfolio = backtest_results()['portfolio']
        returns = portfolio['strategy_returns'].dropna()
        
        # Calculate risk metrics
        var_95 = np.percentile(returns, 5) * 100
        cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        max_daily_loss = returns.min() * 100
        max_daily_gain = returns.max() * 100
        
        return ui.card(
            ui.h5("📊 Risk Metrics Summary", style="color: #00E6A8;"),
            ui.hr(),
            ui.tags.table(
                ui.tags.tbody(
                    ui.tags.tr(
                        ui.tags.td("VaR (95%):", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{var_95:.2f}%", style="color: #FF6B6B; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("CVaR (95%):", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{cvar_95:.2f}%", style="color: #FF6B6B; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Skewness:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{skewness:.3f}", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Kurtosis:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{kurtosis:.3f}", style="color: #CCCCCC; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Max Daily Loss:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{max_daily_loss:.2f}%", style="color: #FF6B6B; text-align: right;")
                    ),
                    ui.tags.tr(
                        ui.tags.td("Max Daily Gain:", style="color: #999; padding: 8px;"),
                        ui.tags.td(f"{max_daily_gain:.2f}%", style="color: #00E6A8; text-align: right;")
                    )
                ),
                style="width: 100%;"
            )
        )
    
    # ==================== Live Monitor Tab ====================
    
    @output
    @render.ui
    def live_status():
        return ui.card(
            ui.layout_columns(
                ui.div(
                    ui.h5("🔴 LIVE", style="color: #FF0000; text-align: center;", class_="pulse"),
                    ui.p("Market Open", style="color: #00E6A8; text-align: center;")
                ),
                ui.div(
                    ui.h5("Last Update", style="color: #999; text-align: center;"),
                    ui.p(datetime.now().strftime("%H:%M:%S"), 
                         style="color: #CCCCCC; text-align: center; font-family: 'JetBrains Mono', monospace;")
                ),
                ui.div(
                    ui.h5("Auto Refresh", style="color: #999; text-align: center;"),
                    ui.p("5 seconds", style="color: #CCCCCC; text-align: center;")
                )
            ),
            style="background: rgba(255,0,0,0.05); border: 1px solid rgba(255,0,0,0.2);"
        )
    
    @output
    @render_widget
    def live_spread_chart():
        # Simulated live data
        times = pd.date_range(end=datetime.now(), periods=100, freq='5min')
        spread = np.random.randn(100).cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=times,
            y=spread,
            name='Live Spread',
            line=dict(color='#00E6A8', width=2),
            mode='lines'
        ))
        
        # Add last point marker
        fig.add_trace(go.Scatter(
            x=[times[-1]],
            y=[spread[-1]],
            mode='markers',
            name='Current',
            marker=dict(color='#00E6A8', size=12, symbol='circle'),
            showlegend=False
        ))
        
        fig.update_layout(
            title="Live Spread Monitor",
            height=400,
            plot_bgcolor='#0F1A1A',
            paper_bgcolor='#0F1A1A',
            font=dict(color='#CCCCCC'),
            xaxis_title="Time",
            yaxis_title="Spread Value"
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        return fig
    
    @output
    @render.ui
    def alert_panel():
        alerts = [
            {"time": "14:32:15", "type": "Entry Signal", "message": "Z-Score crossed -2.0 threshold", "color": "#00E6A8"},
            {"time": "14:28:03", "type": "Risk Alert", "message": "Spread volatility increasing", "color": "#FFA500"},
            {"time": "14:15:47", "type": "Exit Signal", "message": "Position closed at target", "color": "#00E6A8"}
        ]
        
        alert_cards = []
        for alert in alerts:
            alert_cards.append(
                ui.div(
                    ui.layout_columns(
                        ui.span(alert['time'], style="font-family: 'JetBrains Mono', monospace; color: #999;"),
                        ui.span(alert['type'], style=f"color: {alert['color']}; font-weight: bold;"),
                        ui.span(alert['message'], style="color: #CCCCCC;")
                    ),
                    style=f"padding: 10px; margin: 5px 0; background: rgba(255,255,255,0.02); "
                          f"border-left: 3px solid {alert['color']}; border-radius: 5px;"
                )
            )
        
        return ui.card(
            ui.h5("🔔 Recent Alerts", style="color: #00E6A8;"),
            ui.hr(),
            *alert_cards
        )

# ========================================================
# RUN APP
# ========================================================

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()