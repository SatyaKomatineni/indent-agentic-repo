#!/usr/bin/env python
# coding: utf-8

# # L6: Multi-agent Collaboration for Financial Analysis
# 
# In this lesson, you will learn ways for making agents collaborate with each other.

# The libraries are already installed in the classroom. If you're running this notebook on your own machine, you can install the following:
# ```Python
# !pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29
# ```

# In[ ]:


# Warning control
import warnings
warnings.filterwarnings('ignore')


# - Import libraries, APIs and LLM

# In[ ]:


from crewai import Agent, Task, Crew
from dotenv import load_dotenv

import os
#from utils import get_openai_api_key, get_serper_api_key
# openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
#os.environ["SERPER_API_KEY"] = get_serper_api_key()
load_dotenv()

from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileWriterTool # YoutubeChannelSearchTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
filewrite_tool = FileWriterTool()
# youtubechannel_tool = YoutubeChannelSearchTool(youtube_channel_handle='@CNBCtelevision')

# ## Creating Agents

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
    tools = [scrape_tool, search_tool, filewrite_tool]
)

# Task for Data Analyst Agent: Analyze Market Data
data_analysis_task = Task(
    description=(
        "Get price and volume data for the selected stock ({stock_selection}) for the past 5 days."
        "Write this data in a document in the current directory in CSV format and give it name {stock_selection}.csv"
        "CSV file should have three columns: Date, Price and Volume"
    ),
    expected_output=(
        "CSV file with 5 rows and 3 columns that contains date, price and volume of stock: {stock_selection}."
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

# In[ ]:


# Example data for kicking off the process
financial_trading_inputs = {
    'stock_selection': 'NVDA',
    'initial_capital': '100000',
    'risk_tolerance': 'Medium',
    'trading_strategy_preference': 'Day Trading',
    'news_impact_consideration': True
}


# **Note**: LLMs can provide different outputs for they same input, so what you get might be different than what you see in the video.

# In[ ]:


### this execution will take some time to run
result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)


# - Display the final result as Markdown.

# In[ ]:


#from IPython.display import Markdown
#Markdown(result)