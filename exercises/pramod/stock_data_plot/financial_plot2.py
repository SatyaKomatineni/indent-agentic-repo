import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import yfinance as yf
import matplotlib.pyplot as plt
import io
import os 

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

load_dotenv()
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
class FetchStockDataTool(BaseTool):
    name: str = "Fetch Stock Data"
    description: str = "Fetches stock price and volume data for a given ticker and date range"
    ticker: str = Field(..., description="Stock ticker symbol")
    def _run(self, ticker: str, start_date: str, end_date: str):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

class PlotStockDataTool(BaseTool):
    name: str = "Plot Stock Data"
    description: str = "Plots stock price and volume data using matplotlib"
    ticker: str = Field(..., description="Stock ticker symbol")
    data: str = Field(None, description="Stock data to plot in three columns, date, Close price, volume")
    def _run(self, data: str, ticker: str):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Plot stock price
        ax1.plot(data.index, data['Close'], label='Close Price')
        ax1.set_title(f'{ticker} Stock Price and Volume')
        ax1.set_ylabel('Price')
        ax1.legend()
        
        # Plot volume
        ax2.bar(data.index, data['Volume'], label='Volume', color='green', alpha=0.7)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.legend()
        
        plt.tight_layout()
        
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        return buf


# Create instances of the tools
fetch_stock_tool = FetchStockDataTool(ticker="{stock_selection}")
plot_stock_tool = PlotStockDataTool(ticker="{stock_selection}")

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Monitor and analyze market data in real-time "
         "to identify trends and predict market movements.",
    backstory="Specializing in financial markets, this agent "
              "uses statistical modeling and machine learning "
              "to provide crucial insights. With a knack for data, "
              "the Data Analyst Agent is the cornerstone for "
              "informing trading decisions.",
    verbose=True,
    allow_delegation=True,

)

# Task for Data Analyst Agent: Analyze Market Data
data_analysis_task = Task(
    description=(
        "1. First, use the 'Fetch Stock Data' tool to get price and volume data for the selected stock ({stock_selection}) for the past 5 days. "
        "2. Save this data in a CSV file named {stock_selection}.csv in the current directory. The CSV file should have three columns: Date, Price, and Volume. "
        "3. Then, use the 'Plot Stock Data' tool. The output of the 'Fetch Stock Data' tool should be assigned to variable name 'data' which should be passed as input to the 'Plot Stock Data' tool. "
        "4. Use the stock ticker '{stock_selection}' as the ticker input for the plot tool."

    ),
    expected_output=(
        "A CSV file named {stock_selection}.csv containing 5 rows and 3 columns (Date, Price, Volume). "
        "A plot of the stock's price and volume data."
    ),
    agent=data_analyst_agent,
    tools = [fetch_stock_tool, plot_stock_tool],

)


from crewai import Crew, Process
from langchain_openai import ChatOpenAI

# Define the crew with agents and tasks
financial_trading_crew = Crew(
    agents=[data_analyst_agent #, 
            #trading_strategy_agent, 
            #execution_agent
            #, risk_management_agent
            ],
    
    tasks=[data_analysis_task #, 
           #strategy_development_task, 
           #execution_planning_task
           #, risk_assessment_task
           ],
    
    manager_llm=ChatOpenAI(model="gpt-3.5-turbo", 
                           temperature=0.7),
    verbose=True
)

# Example data for kicking off the process
financial_trading_inputs = {
    'stock_selection': 'NVDA',
}

### this execution will take some time to run
result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)