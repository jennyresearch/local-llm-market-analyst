import os
import streamlit as st
import yfinance as yf
from datetime import date
import market_analyst as ma
import datetime as datetime

# LangChain & llama-cpp
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate


#-----Input date preparation------------#
## get stock price and historical data
ticker = "AAPL"
curent_price, currency = ma.get_stock_price(ticker)
price_history = ma.historical_prices(ticker)
lastest_date = price_history.tail(1)["Date"].iloc[0].strftime("%Y-%m-%d")   

#------Contents in the app---------------#
# hearder
st.title("📈 Stock Analysis App")
st.header("Analyze Stock Data with LLMs")

# input ticker 
user_input = st.text_input("Enter Stock Ticker (Capitalized)", "AAPL") 
ticker = user_input
st.write(f"Current price of {ticker} is {curent_price} {currency} as of {lastest_date}")

# # historical chart
# # plotting the historical prices in Candlestick
# import plotly.graph_objects as go
# fig = go.Figure(data=[go.Candlestick(x=price_history['Date'],
#                                      open=price_history[f'Open {ticker}'],
#                                      high=price_history[f'High {ticker}'],
#                                      low=price_history[f'Low {ticker}'],
#                                      close=price_history[f'Close {ticker}'])])
# fig.update_layout(title=f"{ticker} Stock Price History (Candlestick Chart)",
#                   xaxis_title="Date",
#                   yaxis_title=f"Price ({currency})",
#                   xaxis_rangeslider_visible=True)
# st.plotly_chart(fig, use_container_width=True)

# LLM model selection
st.write(f"Stock Analysis: {ticker} Analysis is in process...\
         Please wait...\
         \nThis may take at lease 20 seconds to complete.")
start_time = datetime.datetime.now() 
st.write(ma.ticker_analysis(ticker, curent_price, price_history))
end_time = datetime.datetime.now()
processing_time = end_time - start_time
st.write(f"Prompt processing time: {processing_time}")


# # sidebar content
# st.sidebar.markdown(ma.indicator_description())