""" import yfinance as yf
import pandas as pd
import pandas_ta as ta

def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    return yf.download(symbol, start=start_date, end=end_date)

def calculate_indicators(data: pd.DataFrame, indicators: list) -> pd.DataFrame:
    for indicator in indicators:
        if indicator == 'SMA':
            data['SMA_20'] = ta.sma(data['Close'], length=20)
        elif indicator == 'RSI':
            data['RSI_14'] = ta.rsi(data['Close'], length=14)
        elif indicator == 'MACD':
            macd = ta.macd(data['Close'])
            data = pd.concat([data, macd], axis=1)
        elif indicator == 'OBV':
            data['OBV'] = ta.obv(data['Close'], data['Volume'])
    return data

# Usage example
symbol = "NVDA"
start_date = "2014-01-01"
end_date = "2025-03-10"
indicators = ['SMA', 'RSI', 'MACD', 'OBV']

# Fetch and save raw stock data
stock_data = fetch_stock_data(symbol, start_date, end_date)
stock_data.to_csv(f"{symbol}_raw_data.csv")

# Calculate indicators and save analyzed data
analyzed_data = calculate_indicators(stock_data, indicators)
analyzed_data.to_csv(f"{symbol}_analyzed_data.csv")

print(f"Raw data saved to {symbol}_raw_data.csv")
print(f"Analyzed data saved to {symbol}_analyzed_data.csv")
 """
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import matplotlib.pyplot as plt

def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    # Explicitly set auto_adjust=False to get all columns
    data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
    
    # Reset index and rename columns
    data = data.reset_index()
    data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    return data.set_index('Date')

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    # Calculate technical indicators
    data['SMA_20'] = ta.sma(data['Close'], length=20)
    data['SMA_50'] = ta.sma(data['Close'], length=50)
    data['RSI_14'] = ta.rsi(data['Close'], length=14)
    macd = ta.macd(data['Close'])
    data = pd.concat([data, macd], axis=1)
    data['OBV'] = ta.obv(data['Close'], data['Volume'])
    return data

def plot_stock_data(data: pd.DataFrame, symbol: str):
    # Prepare the style
    mc = mpf.make_marketcolors(up='g', down='r', volume='in', wick={'up':'g', 'down':'r'})
    s = mpf.make_mpf_style(marketcolors=mc)

    # Prepare additional plots
    add_plots = [
        mpf.make_addplot(data['SMA_20'], color='blue', width=0.7),
        mpf.make_addplot(data['SMA_50'], color='red', width=0.7),
        mpf.make_addplot(data['RSI_14'], panel=2, ylabel='RSI'),
        mpf.make_addplot(data['MACD_12_26_9'], panel=3, color='b', ylabel='MACD'),
        mpf.make_addplot(data['MACDs_12_26_9'], panel=3, color='r'),
        mpf.make_addplot(data['OBV'], panel=4, ylabel='OBV')
    ]
    # Create the plot
    fig, axes = mpf.plot(data, type='candle', style=s, addplot=add_plots,
                         volume=True, figsize=(12, 14), panel_ratios=(6,2,2,2,2),
                         title=f'\n{symbol} Stock Price with Technical Indicators',
                         returnfig=True)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f'{symbol}_technical_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
symbol = "NVDA"
start_date = "2014-01-01"
end_date = "2025-03-10"

# Fetch and save raw stock data
raw_data = fetch_stock_data(symbol, start_date, end_date)
raw_data.to_csv(f"{symbol}_raw_data.csv", index=True)


# Calculate indicators and save analyzed data
analyzed_data = calculate_indicators(raw_data)
analyzed_data.to_csv(f"{symbol}_analyzed_data.csv", index=True)

# Plot the data
plot_stock_data(analyzed_data, symbol)

print("Data successfully saved:")
print(f"Raw data shape: {raw_data.shape}")
print(f"Analyzed data shape: {analyzed_data.shape}")
print(f"Technical analysis chart saved as {symbol}_technical_analysis.png")