import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    # Explicitly set auto_adjust=False to get all columns
    data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
    
    # Reset index and rename columns
    data = data.reset_index()
    data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    return data.set_index('Date')

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    data['SMA_20'] = ta.sma(data['Close'], length=20)
    data['SMA_50'] = ta.sma(data['Close'], length=50)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    macd = ta.macd(data['Close'])
    data = pd.concat([data, macd], axis=1)
    data['OBV'] = ta.obv(data['Close'], data['Volume'])
    return data

def plot_stock_data_interactive(data: pd.DataFrame, symbol: str):
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                        row_heights=[0.5, 0.1, 0.1, 0.1, 0.1],
                        subplot_titles=(f"{symbol} Stock Price", "Volume", "RSI", "MACD", "OBV"))

    # Candlestick chart
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                 low=data['Low'], close=data['Close'], name='Price'), row=1, col=1)
    
    # Moving Averages
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='blue', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='red', width=1)), row=1, col=1)

    # Volume
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')), row=3, col=1)

    # MACD
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD_12_26_9'], name='MACD', line=dict(color='blue')), row=4, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['MACDs_12_26_9'], name='Signal', line=dict(color='red')), row=4, col=1)

    # OBV
    fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], name='OBV', line=dict(color='green')), row=5, col=1)

    # Update layout for better readability
    fig.update_layout(height=1200, width=1200, title_text=f"{symbol} Technical Analysis",
                      xaxis_rangeslider_visible=False)

    # Increase number of x-axis labels
    fig.update_xaxes(tickangle=45, tickmode='auto', nticks=100)

    # Add y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    fig.update_yaxes(title_text="MACD", row=4, col=1)
    fig.update_yaxes(title_text="OBV", row=5, col=1)

    # Save as interactive HTML (which uses SVG for rendering)
    fig.write_html(f"{symbol}_interactive_chart.html")

    print(f"Interactive chart saved as {symbol}_interactive_chart.html")

# Usage example
symbol = "NVDA"
start_date = "2023-01-01"
end_date = "2024-03-10"

# Fetch and analyze data
raw_data = fetch_stock_data(symbol, start_date, end_date)
analyzed_data = calculate_indicators(raw_data)

# Create interactive plot
plot_stock_data_interactive(analyzed_data, symbol)

