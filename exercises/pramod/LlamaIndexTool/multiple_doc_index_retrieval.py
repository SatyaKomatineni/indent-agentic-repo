import os
import requests
from crewai import Agent, Task, Crew, Process
from llama_index.core import SimpleDirectoryReader, GPTVectorStoreIndex
from crewai.tools import BaseTool
import os
from dotenv import load_dotenv
#dotenv_path = r"C:\tools\LocalGit\indent-agentic-repo\exercises\pramod\.env"
dotenv_path = "C:\\tools\\LocalGit\\indent-agentic-repo\\exercises\\pramod\\.env"
load_dotenv(dotenv_path)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Step 1: Load and Index Documents using LlamaIndex
documents = SimpleDirectoryReader("C:\\iwe\\WEE Book\\Draft 6\\New").load_data()
index = GPTVectorStoreIndex.from_documents(documents)
# converts an index into a query engine, allowing you to perform semantic search and retrieval over indexed documents
query_engine = index.as_query_engine()

# ✅ Step 2: Create a CrewAI Tool Wrapping LlamaIndex
class LlamaIndexQueryTool(BaseTool):
    name: str = "LlamaIndexQuery"
    description: str = "Searches indexed documents and retrieves relevant information."
    
    def _run(self, query: str):
        """Perform a query on indexed documents."""
        return query_engine.query(query).response

# ✅ Step 3: Create a CrewAI Agent with the Tool
research_agent = Agent(
    role="Research Assistant",
    goal="Answer knowledge-based questions using a document database.",
    backstory="An AI assistant specializing in retrieving and summarizing information from research papers.",
    verbose=True,
    tools=[LlamaIndexQueryTool()]
)

# ✅ Step 4: Define a Task for the Agent
research_task = Task(
    description="Find information about the physics of wind energy.",
    expected_output="A summary of the physics of wind energy.",
    agent=research_agent
)

# ✅ Step 5: Create and Run the Crew
crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    process=Process.sequential  # Runs tasks one after another
)

result = crew.kickoff()
# print("\n🔍 Research Output:", result)
from IPython.display import Markdown
Markdown(result.raw)