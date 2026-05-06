# This is a market analyst module that provides functions to fetch stock prices and historical data.

import yfinance as yf
from typing import Tuple
import pandas as pd
import datetime as datetime
import plotly.graph_objects as go

def get_stock_info(ticker: str) -> Tuple[str, str, str]:
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    name = info.get("longName", "")
    sector = info.get("sector", "")
    industry = info.get("industry", "")
    return name, sector, industry
def get_stock_price(ticker: str):
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    currency = info.get("currency", "")
    return price, currency

def historical_prices(ticker: str):
    # Download historical stock prices for the given ticker
    df = yf.download(ticker, period="2y", interval="1d")
    df.reset_index(inplace=True)
    # convert from multi-index to single index
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    # round float values to 2 digits
    df = df.round(2)
    
    # Calculate indicators
    # --- 1. Calculate Moving Averages (20‑day & 50‑day) ---
    df["SMA_20"] = df[f"Close {ticker}"].rolling(window=20).mean()
    df["SMA_50"] = df[f"Close {ticker}"].rolling(window=50).mean()

    # --- 2. Calculate RSI (14‑period) ---
    delta = df[f"Close {ticker}"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    # --- 3. Calculate MACD (12,26,9) ---
    ema12 = df[f"Close {ticker}"].ewm(span=12, adjust=False).mean()
    ema26 = df[f"Close {ticker}"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    df = df.round(2)

    return df

# promt definition: ticker analysis
from llm_provider import get_llm

def ticker_analysis(ticker, current_price, price_history):
    llm = get_llm()
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    cols = ['Date', f'Close {ticker}', 'SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Hist']
    recent_data = price_history[cols].tail(60).to_string(index=False)
    latest = price_history[cols].tail(1).iloc[0]
    latest_summary = f"""
- Date: {latest['Date'].strftime('%Y-%m-%d')}
- Close price: {latest[f'Close {ticker}']} USD
- SMA_20 (20-day moving average): {latest['SMA_20']}
- SMA_50 (50-day moving average): {latest['SMA_50']}
- RSI_14: {latest['RSI_14']}
- MACD: {latest['MACD']}, Signal: {latest['MACD_Signal']}, Histogram: {latest['MACD_Hist']}"""

    # Prepare the prompt
    prompt = f'''
    You are a stock analysis expert who specializes in using technical indicators to analyze {ticker} buying and selling price levels.
    Indicators: moving averages, RSI, and MACD.
    You are given data:
    - current price in USD of {ticker}: {current_price}
    - the LATEST indicator values (use these exact numbers in your analysis):
{latest_summary}
    - the most recent 60 days of historical price data for trend context (oldest to latest):
{recent_data}
    Columns: Date, Close price, SMA_20, SMA_50, RSI_14, MACD, MACD_Signal, MACD_Hist.
    Your answer:
    - print out the latest {ticker} price and date from the data above.
    - analyze the current price in relation to the historical data.
    - provide a recommendation on whether to "buy", "sell", or "hold" the stock based on your analysis.
    - explain your reasoning briefly, focusing on technical indicators and market trends.
    - answer is straightforward and concise, using simple language, and not too long.
    - do NOT use asterisks (*) for inline emphasis within sentences — only use ** for section headers.
    - do NOT use dollar signs ($) for prices — write the number followed by USD (e.g. 287.51 USD).
    - in the end, state that the recommendation is provided on {today_date}.
        '''
    result = llm.invoke(prompt)
    text = result.content if hasattr(result, 'content') else result
    return text.replace('$', r'\$')

# indicator description
def indicator_description():
    # Indicator descriptions
    return """
    # Indicator descriptions
    ## 📊 1. Moving Average (MA)
    A moving average smooths out price data by calculating the average price of a stock over a specific number of days. It helps you see the trend more clearly by filtering out day-to-day price noise.

    🧮 Example:
    5-day MA: average of the last 5 closing prices
    50-day MA: shows the medium-term trend
    200-day MA: long-term trend indicator

    📈 How it's used:
    If the short-term MA (e.g. 20-day) crosses above the long-term MA (e.g. 50-day), that’s a bullish signal ("Golden Cross").
    If it crosses below, that’s a bearish signal ("Death Cross").

    ## 🔄 2. RSI (Relative Strength Index)
    RSI is a momentum indicator that measures how strongly a stock is moving in either direction. It ranges from 0 to 100.

    🧮 Interpretation:
    RSI > 70 = Overbought (might fall soon)
    RSI < 30 = Oversold (might rise soon)
    RSI = 50 = Neutral

    📈 How it's used:
    Traders look for reversals when RSI hits extreme levels (30 or 70).
    A stock that keeps rising despite a high RSI might indicate strong bullish momentum.                    

    ## 📉 3. MACD (Moving Average Convergence Divergence)
    MACD tracks the relationship between two moving averages: the 12-day EMA and the 26-day EMA (exponential moving averages). It also includes a Signal Line (usually 9-day EMA of the MACD).

    🧮 Formula:
    MACD = 12-day EMA - 26-day EMA
    Signal Line = 9-day EMA of MACD

    📈 How it's used:
    MACD crosses above Signal Line = Bullish signal\\
    MACD crosses below Signal Line = Bearish signal\\
    Traders also watch the MACD histogram, which shows the gap between MACD and Signal Line
    """


## -----Metric Visual--------##
def plot_candlestick_chart(price_history, ticker, currency):
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Candlestick(x=price_history['Date'],
                                        open=price_history[f'Open {ticker}'],
                                        high=price_history[f'High {ticker}'],
                                        low=price_history[f'Low {ticker}'],
                                        close=price_history[f'Close {ticker}'])])
    fig.update_layout(title=f"{ticker} Stock Price History (Candlestick Chart)",
                    xaxis_title="Date",
                    yaxis_title=f"Price ({currency})",
                    xaxis_rangeslider_visible=True)
    #fig.show()
    return fig


def plot_SMA(price_history, ticker):
    # Plotting the 20-day and 50-day Simple Moving Averages (SMA
    # Show more days by sorting ascending and plotting the full range
    price_history_sorted = price_history.sort_values(by='Date', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted[f'Close {ticker}'],
        mode='lines',
        name=f'Close {ticker}'
    ))
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted['SMA_20'],
        mode='lines',
        name='20‑day SMA'
    ))
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted['SMA_50'],
        mode='lines',
        name='50‑day SMA'
    ))
    fig.update_layout(
        title=f"{ticker} Price with 20‑day & 50‑day SMAs (Full History)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Legend",
        xaxis=dict(rangeslider=dict(visible=True))  # Add range slider for zooming
    )
    # move the legend to the top left corner
    fig.update_layout(legend=dict(x=0, y=1, traceorder='normal',
                                orientation='h', bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)'))

    return fig


def plot_RSI(price_history, ticker):
    # RSI (Relative Strength Index)
    price_history_sorted = price_history.sort_values(by='Date', ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted['RSI_14'],
        mode='lines',
        name='RSI 14'
    ))
    fig.update_layout(
        title=f"{ticker} RSI 14 (Full History)",
        xaxis_title="Date",
        yaxis_title="RSI",
        legend_title="Legend",
        xaxis=dict(rangeslider=dict(visible=True))  # Add range slider for zoomming
    )

    fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="RSI 30", annotation_position="top left")
    fig.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="RSI 70", annotation_position="top left")

    #shape the area axline=30 and annotation_text it as "Oversold" which show the label "Oversold Area/Buy Zone"    
    fig.add_shape(type="rect",
                x0=price_history_sorted['Date'].min(),
                x1=price_history_sorted['Date'].max(),
                y0=0,
                y1=30,
                fillcolor="red",
                opacity=0.2,
                line_width=0,
                name="Oversold Area/Buy Zone",
                layer="below")    

    fig.add_shape(type="rect",
                x0=price_history_sorted['Date'].min(),
                x1=price_history_sorted['Date'].max(),
                y0=70,
                y1=100,
                fillcolor="green",
                opacity=0.2,
                line_width=0,
                name="Overbought Area/Sell Zone",
                layer="below")    
    # add annotation_text for shaded area
    fig.add_annotation(
        x=price_history_sorted['Date'].max(),
        y=15,
        text="Oversold Area/Buy Zone",
        showarrow=False,
        font=dict(color="red")
    )
    fig.add_annotation(
        x=price_history_sorted['Date'].max(),
        y=85,
        text="Overbought Area/Sell Zone",
        showarrow=False,
        font=dict(color="green")
    )   

    # hover text showing the RSI value and close price
    fig.update_traces(hovertemplate="<b>Date:</b> %{x}<br><b>RSI:</b> %{y}<br><b>Close Price:</b> %{customdata[0]}",
                    customdata=price_history_sorted[['Close ' + ticker]].values)

    return fig


def plot_MACD(price_history, ticker):
    # plot the MACD (Moving Average Convergence Divergence)
    # Show more days by sorting ascending and plotting the full range
    price_history_sorted = price_history.sort_values(by='Date', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted['MACD'],
        mode='lines',
        name='MACD'
    ))
    fig.add_trace(go.Scatter(
        x=price_history_sorted['Date'],
        y=price_history_sorted['MACD_Signal'],
        mode='lines',
        name='MACD Signal'
    ))
    fig.add_trace(go.Bar(
        x=price_history_sorted['Date'],
        y=price_history_sorted['MACD_Hist'],
        name='MACD Histogram',
        marker_color='rgba(0, 0, 255, 0.5)',
        opacity=0.5
    ))      
    fig.update_layout(
        title=f"{ticker} MACD (Full History)",
        xaxis_title="Date",
        yaxis_title="MACD",
        legend_title="Legend",
        xaxis=dict(rangeslider=dict(visible=True))  # Add range slider for zoomming
    )
    # hover text showing the MACD, MACD Signal, MACD Histogram values and close price 
    fig.update_traces(hovertemplate="<b>Date:</b> %{x}<br><b>Close Price:</b> %{customdata[0]}<br><b>MACD:</b> %{y}<br><b>MACD Signal:</b> %{customdata[1]}<br><b>MACD Histogram:</b> %{customdata[2]}",
                    customdata=price_history_sorted[['Close ' + ticker, 'MACD', 'MACD_Signal', 'MACD_Hist']].values)
    fig.update_layout(legend=dict(x=0, y=1, traceorder='normal',
                                orientation='h', bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)'))

    return fig
