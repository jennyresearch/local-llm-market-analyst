import os
import streamlit as st
import yfinance as yf
from datetime import date
import market_analyst as ma
import datetime as datetime


#-----Select LLM Provider------------#
provider = st.sidebar.selectbox("LLM Provider", ["ollama", "openai"])
os.environ["LLM_PROVIDER"] = provider

api_key_ready = True
if provider == "openai":
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        api_key_ready = False

if not api_key_ready:
    st.sidebar.info("Enter your OpenAI API key above to run the analysis.")
    run_analysis = False
else:
    run_analysis = st.sidebar.button("Run LLM Technical Analysis")

#------Contents in the app---------------#
st.title("📈 Stock Analysis App")
st.header("Analyze Stock Data with LLMs")

user_input = st.text_input("Enter Stock Ticker (Capitalized)", "AAPL")
ticker = user_input

#-----Input date preparation------------#
curent_price, currency = ma.get_stock_price(ticker)
price_history = ma.historical_prices(ticker)
lastest_date = price_history.tail(1)["Date"].iloc[0].strftime("%Y-%m-%d")
st.write(f"Current price of {ticker} is {curent_price} {currency} as of {lastest_date}")

#---------------------#
# Market Indicators Overview
st.markdown(
    """
### Market Indicators Overview
| Indicator | Measures            | Key Use                   | Signal Triggers                       |
|-----------|---------------------|---------------------------|---------------------------------------|
| **MA**    | Trend (avg. price)  | Support / resistance zones| Golden Cross / Death Cross            |
| **RSI**   | Momentum (0–100)    | Overbought / Oversold     | RSI > 70 (sell), RSI < 30 (buy)       |
| **MACD**  | Trend + Momentum    | Entry / exit signals      | MACD line crosses Signal line         |
    """
)

#--------Charts--------#
st.subheader("📊 Price Charts")
fig_candle = ma.plot_candlestick_chart(price_history, ticker, currency)
st.plotly_chart(fig_candle, use_container_width=True)

fig_sma = ma.plot_SMA(price_history, ticker)
st.plotly_chart(fig_sma, use_container_width=True)

fig_rsi = ma.plot_RSI(price_history, ticker)
st.plotly_chart(fig_rsi, use_container_width=True)

fig_macd = ma.plot_MACD(price_history, ticker)
st.plotly_chart(fig_macd, use_container_width=True)

#--------LLM Analysis--------#
st.subheader("🤖 LLM Analysis")
if run_analysis:
    with st.spinner(f"Analyzing {ticker}... this may take ~20 seconds."):
        start_time = datetime.datetime.now()
        result = ma.ticker_analysis(ticker, curent_price, price_history)
        end_time = datetime.datetime.now()
    st.markdown(result)
    st.caption(f"Prompt processing time: {end_time - start_time}")