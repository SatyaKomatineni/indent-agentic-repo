# Implementation of simple program for reading documents from file system
# categorizing the documents based on multicriteria
# Write the categorization to file system
# 
# Goal of this program
#
# Say this filename is called: extract-data-ai.py
#
# then you can do the following:
#
# python extract-data-ai.py <input-document-filename> <prompt-file-name> <output-extracted-file-name>
#

import os
import pickle
import requests
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import os
from dotenv import load_dotenv
#dotenv_path = r"C:\tools\LocalGit\indent-agentic-repo\exercises\pramod\.env"
dotenv_path = "C:\\tools\\LocalGit\\indent-agentic-repo\\exercises\\pramod\\.env"
load_dotenv(dotenv_path)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DOC_STORAGE_PATH = "C:\\tools\\LocalGit\\indent-agentic-repo\\exercises\\pramod\\contentCategorization1\\inputDocs\\"
# DOC_STORAGE_PATH = r"C:\tools\LocalGit\indent-agentic-repo\exercises\pramod\contentCategorization1\"

DOC_STORAGE_PATH = ".\\exercises\\pramod\\contentCategorization1\\inputDocs\\"

from crewai_tools import FileReadTool

# Initialize the tool with a specific file path, so the agent can only read the content of the specified file
file_path = os.path.join(DOC_STORAGE_PATH, "Wedbush-Apple March 14 2025.txt")
prompt_path = os.path.join(DOC_STORAGE_PATH, "..\\prompt_rules\\cat_prompt.txt")

file_read_tool = FileReadTool(file_path=file_path)
prompt_read_tool = FileReadTool(file_path=prompt_path)

# ✅ Step 3: Create a CrewAI Agent with the Tool
research_agent = Agent(
    role="Financial Research Assistant",
    goal="Structured content and data extraction from an input document using a prompt document as the rule."
    " Read the input document using the file read tool"
    " Read the prompt document using the prompt read tool to apply the prompt against that input document."
    " Return the output as indicated by the prompt",
    backstory="An AI assistant specializing in retrieving structured content and summarizing information from articles about stocks.",
    verbose=True,
    tools=[file_read_tool, prompt_read_tool]
)

# ✅ Step 4: Define a Task for the Agent
research_task = Task(
   description="Use the Research Assistant Agent to read the input document and apply the prompt rules to extract structured data.",
   expected_output="Create 3 columns of content based on the three dimensions: Recommendation, Target Price and Risks",
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
# from IPython.display import Markdown
# Markdown(result.raw)

""" # ✅ Step 1: Check if the index already exists
if os.path.exists(INDEX_STORAGE_PATH):
    print("📂 Loading existing index from storage...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
    index = load_index_from_storage(storage_context)
else:
    print("📂 Creating a new index and saving it...")
    documents = SimpleDirectoryReader("C:\\iwe\\WEE Book\\Draft 6\\New").load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=INDEX_STORAGE_PATH)  # Save index to disk
 
query_engine = index.as_query_engine()

# ✅ Step 2: Create a CrewAI Tool Wrapping LlamaIndex
class LlamaIndexQueryTool(BaseTool):
    name: str = "LlamaIndexQuery"
    description: str = "Searches indexed documents and retrieves relevant information."
    
    def _run(self, query: str):
        #Perform a query on indexed documents.
        return query_engine.query(query).response
 """
