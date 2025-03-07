#!/usr/bin/env python
# coding: utf-8

# Single-agent for getting recent buy, hold and sell recommendations by reading articles from SeekingAlpha
#
# ```Python
# !pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29
# ```

# Warning control
import warnings
warnings.filterwarnings('ignore')


# - Import libraries, APIs and LLM

from crewai import Agent, Task, Crew
from dotenv import load_dotenv

import os
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
load_dotenv()

from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileWriterTool,WebsiteSearchTool # YoutubeChannelSearchTool

# To enable the tool to search any website the agent comes across or learns about during its operation
website_search_tool = WebsiteSearchTool()
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
filewrite_tool = FileWriterTool()
# youtubechannel_tool = YoutubeChannelSearchTool(youtube_channel_handle='@CNBCtelevision')

# ## Creating Agents

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Monitor and analyze articles from seekingalpha.com website "
         "to identify trends and predict market movements.",
    backstory="Specializing in financial markets, this agent "
              "uses statistical modeling and machine learning "
              "to provide crucial insights. With a knack for data, "
              "the Data Analyst Agent is the cornerstone for "
              "informing trading decisions.",
    verbose=True,
    allow_delegation=True,
    tools = [scrape_tool, website_search_tool, filewrite_tool]
)

# Task for Data Analyst Agent: Analyze Market Data
data_analysis_task = Task(
    description=(
        "go to these two websites ONLY: https://seekingalpha.com/symbol/{stock_selection}/analysis and https://seekingalpha.com/symbol/{stock_selection}/news"
        "Read all the articles posted in the past 5 days and get these three attributes from each article: "
        "1. URL of the article"
        "2. Recommendation, which should be one of the three: Buy, Hold, Sell"
        "3. Price target of {stock_selection}"
        "Write the three attributes (one row for each article) in the current directory in CSV format and give it name {stock_selection}_URL.csv"
    ),
    expected_output=(
        "CSV file in the current directory with the three attributes with one row for each articl"
    ),
    agent=data_analyst_agent,
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
    process=Process.hierarchical,
    verbose=True
)


# ## Running the Crew
# 
# - Set the inputs for the execution of the crew.

# Example data for kicking off the process
financial_trading_inputs = {
    'stock_selection': 'NVDA',
    'initial_capital': '100000',
    'risk_tolerance': 'Medium',
    'trading_strategy_preference': 'Day Trading',
    'news_impact_consideration': True
}

### this execution will take some time to run
result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)

from IPython.display import Markdown
Markdown(result)

""" from markdown_pdf import MarkdownPdf,Section
# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define the path to save the PDF in the same directory as the script
pdf_path = os.path.join(script_dir, "financialReport.pdf")
### this execution will take some time to run. creating pdf object and converting markdown to pdf
pdf = MarkdownPdf(toc_level=1)
# creating sections and adding it to PDF.adding methods add_section to pdf object. 
pdf.add_section(Section(result))
# pdf.save("financialReport.pdf")
pdf.save(pdf_path)
# - Display the final result as Markdown. """