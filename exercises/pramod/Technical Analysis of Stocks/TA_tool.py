from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dotenv import load_dotenv

import os
#from utils import get_openai_api_key, get_serper_api_key
# openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
#os.environ["SERPER_API_KEY"] = get_serper_api_key()
load_dotenv()


class StockAnalysisTool(BaseTool):
    name: str = "Stock Analysis and Visualization Tool"
    description: str = "Fetches stock data, calculates technical indicators, and generates an interactive chart"
    
    class InputSchema(BaseModel):
        symbol: str = Field(..., description="Stock symbol (e.g., AAPL for Apple Inc.)")
        start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
        end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    
    args_schema: Type[BaseModel] = InputSchema

    def _run(self, symbol: str, start_date: str, end_date: str) -> str:
        try:
            raw_data = self.fetch_stock_data(symbol, start_date, end_date)
            analyzed_data = self.calculate_indicators(raw_data)
            self.plot_stock_data_interactive(analyzed_data, symbol)
            return f"Analysis complete. Interactive chart saved as {symbol}_interactive_chart.html"
        except Exception as e:
            return f"Error during stock analysis: {str(e)}"

    def fetch_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
        data = data.reset_index()
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        return data.set_index('Date')

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        data['SMA_20'] = ta.sma(data['Close'], length=20)
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        macd = ta.macd(data['Close'])
        data = pd.concat([data, macd], axis=1)
        data['OBV'] = ta.obv(data['Close'], data['Volume'])
        return data

    def plot_stock_data_interactive(self, data: pd.DataFrame, symbol: str):
        fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                            row_heights=[0.5, 0.1, 0.1, 0.1, 0.1],
                            subplot_titles=(f"{symbol} Stock Price", "Volume", "RSI", "MACD", "OBV"))
        
        # Add traces for candlestick, moving averages, volume, RSI, MACD, and OBV
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                     low=data['Low'], close=data['Close'], name='Price'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='blue', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='red', width=1)), row=1, col=1)
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'), row=2, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD_12_26_9'], name='MACD', line=dict(color='blue')), row=4, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['MACDs_12_26_9'], name='Signal', line=dict(color='red')), row=4, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], name='OBV', line=dict(color='green')), row=5, col=1)
        
        # Update layout and axes
        fig.update_layout(height=1200, width=1200, title_text=f"{symbol} Technical Analysis",
                          xaxis_rangeslider_visible=False)
        fig.update_xaxes(tickangle=45, tickmode='auto', nticks=100)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        fig.update_yaxes(title_text="MACD", row=4, col=1)
        fig.update_yaxes(title_text="OBV", row=5, col=1)
        
        fig.write_html(f"{symbol}_interactive_chart.html")


from crewai import Crew, Agent, Task
#from stock_analysis_tool import StockAnalysisTool

# Create the StockAnalysisTool
stock_tool = StockAnalysisTool()

# Create an agent that will use the tool
analyst_agent = Agent(
    role="Stock Analyst",
    goal="Stock Analyst",
    backstory="Good at gathering stock data, computes technical analysis and plots",
    tools=[stock_tool]
)

# Create a task for the agent
analysis_task = Task(
    description=("Analyze stock data for NVDA from 2023-01-01 to 2024-03-10"),
    expected_output=(
        "CSV file with 5 rows and 3 columns that contains date, price and volume of stock: {stock_selection}."
    ),
    agent=analyst_agent
)

# Create a crew with the agent and task
crew = Crew(
    agents=[analyst_agent],
    tasks=[analysis_task]
)

# Run the crew
result = crew.kickoff()

print(result)
