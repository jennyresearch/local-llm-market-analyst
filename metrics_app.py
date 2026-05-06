import streamlit as st
import market_analyst as ma


# Set page configuration
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 450px;
            max-width: 450px;
            width: 450px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


#------Contents in the app---------------#
# sidebar content
st.sidebar.markdown(ma.indicator_description())

# hearder
st.title("📈 Stock Analysis App")
st.header("Analyze Stock Data with LLMs")


#-----Input date preparation------------#
## get stock price and historical data
user_input = st.text_input("Enter Stock Ticker (Capitalized)", "AAPL") 
ticker = user_input
curent_price, currency = ma.get_stock_price(ticker)
price_history = ma.historical_prices(ticker)
lastest_date = price_history.tail(1)["Date"].iloc[0].strftime("%Y-%m-%d") 
st.write(f"Current price of {ticker} is {curent_price} {currency} as of {lastest_date}")  




#---------------------#
# Metrics info
st.markdown(
    """
### Market Indicators Overview
This section provides an overview of key market metrics and indicators used in stock analysis.
| Indicator | Measures            | Key Use                   | Signal Triggers                       |
|-----------|---------------------|---------------------------|---------------------------------------|
| **MA**    | Trend (avg. price)  | Support / resistance zones| Golden Cross / Death Cross            |
| **RSI**   | Momentum (0–100)    | Overbought / Oversold     | RSI > 70 (sell), RSI < 30 (buy)       |
| **MACD**  | Trend + Momentum    | Entry / exit signals      | MACD line crosses Signal line         |

    """
)
#--------visualization of historical prices--------#
# historical chart
# plotting the historical prices in Candlestick

# candlestick chart
fig_candle = ma.plot_candlestick_chart(price_history, ticker, currency)
st.plotly_chart(fig_candle, use_container_width=True)

# SMA chart
fig_sma = ma.plot_SMA(price_history, ticker)
st.plotly_chart(fig_sma, use_container_width=True)

# RSI chart
fig_rsi = ma.plot_RSI(price_history, ticker)
st.plotly_chart(fig_rsi, use_container_width=True)

# MACD chart
fig_macd = ma.plot_MACD(price_history, ticker)
st.plotly_chart(fig_macd, use_container_width=True)
