<!-- ********************* -->
# Parsing rules for extracting CrewAI agentic specifications
<!-- ********************* -->

1. These are instructions for an LLM
2. To identify Agents, Tasks, and Tools in a python one pager
3. Follow the examples shown in this document to identigy Agents, Tasks, and their English parts (Name, Description, output etc.). See the rules below for the full set of rules to identify them
4. Extract the English for Agents and Tasks
5. With the parsed English format the Agents and Tasks in a .md file as if it is documentation for each Agent and Task
6. Follow the specified format for Agents and Tasks below in this document

<!-- ********************* -->
# Rules to identify an Agent and its parts to be extracted
<!-- ********************* -->

An agent looks like this in a crew python file. This is an example

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

In this example 

Name = data_analyst_agent
Role = Data Analyst (identified role attribute)
goal = Monitor and analyze market data in real-time to identify trends and predict market movements. (identified by goal attribute)
backstory = Specializing....trading decisions." (all the multi-line text identified by )

<!-- ********************* -->
# Rules to identify a Task and its parts to be extracted
<!-- ********************* -->

Here is how you identify a task in the .py file

data_analysis_task = Task(
    description=(
        "1. First, use the 'Fetch Stock Data' tool to get price and volume data for the selected stock ({stock_selection}) for the past 5 days. "
        "2. Save this data in a CSV file named {stock_selection}.csv in the current directory. The CSV file should have three columns: Date, Price, and Volume. "
        "3. Then, use the 'Plot Stock Data' tool. The output of the 'Fetch Stock Data' tool should be used as the 'data' input for the 'Plot Stock Data' tool. "
        "4. Use the stock ticker '{stock_selection}' as the ticker input for the plot tool."

    ),
    expected_output=(
        "A CSV file named {stock_selection}.csv containing 5 rows and 3 columns (Date, Price, Volume). "
        "A plot of the stock's price and volume data."
    ),
    agent=data_analyst_agent,
    tools = [fetch_stock_tool, plot_stock_tool],

)

Just like before it has the following attributes whose values are in English

Name (the variable name)
Description
Expected_output
Agent this task is related to

<!-- ********************* -->
# Here is how I want you to extract and present the data
<!-- ********************* -->

1. Extract all agents
2. Extract all tasks

then 

1. write me an md file or give me an output that has..
2. A list of agents that you have extracted
3. Format for each agent
   1. Agent name (as a heading 1)
   2. Role (heading 2) followed by its english role as body of that heading
   3. backstory (heading 2) followed by its english role as body of that heading
4. A list of tasks
5. Format for each task
   1. Task: Name (Heading 1) 
   2. Description (heading 2) and its body
   3. Expected_output (heading 2) and its body
   4. Agent name (heading 2) Name of the agent as body

