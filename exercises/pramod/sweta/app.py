from flask import Flask, render_template, request
from crewai import Agent, Task, Crew, Process
from llama_index.core import SimpleDirectoryReader, GPTVectorStoreIndex, load_index_from_storage, StorageContext
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment
load_dotenv("C:/tools/LocalGit/indent-agentic-repo/exercises/pramod/.env")
# Load or create index
INDEX_STORAGE_PATH = "C:/tools/LocalGit/indent-agentic-repo/exercises/pramod/sweta/indexStore"
DOC_STORAGE_PATH = "C:/tools/LocalGit/indent-agentic-repo/exercises/pramod/sweta/docs"

# Initialize Flask app
app = Flask(__name__)

companyinputs = {
    'company': ''
}

if os.path.exists(INDEX_STORAGE_PATH):
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader(DOC_STORAGE_PATH, recursive=True).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=INDEX_STORAGE_PATH)

query_engine = index.as_query_engine()

class LlamaIndexQueryTool(BaseTool):
    name: str = "LlamaIndexQuery"
    description: str = "Searches indexed documents and retrieves relevant information."

    def _run(self, query: str):
        return query_engine.query(query).response

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "GET":
        print("Rendering template with response:", response)
        return render_template("index.html", response=response)

    else:
        user_prompt = request.form["prompt"]
        if user_prompt == "":
            user_prompt = 'company'
        companyinputs['company'] = user_prompt

        research_agent = Agent(
            role="Research Assistant",
            goal="Answer knowledge-based questions using a document database.",
            backstory="An AI assistant specializing in retrieving and summarizing information from research papers.",
            verbose=True,
            tools=[LlamaIndexQueryTool()])

# ✅ Step 4: Define a Task for the Agent
        research_task = Task(
            description="Find information about {company} competitive advantage, technology, and innovation by reading all the documents in the folder: competitive advantage, JP Morgan, Mutual Benefit Life, On, P&G, PNB, Snapper, Walmart Blockchain.",
            expected_output="A summary of the competitive advantage, technology and innovation of companies. Create a paragraph of detailed content for each company.",
            agent=research_agent
        )
        editor_agent = Agent(
            role = "Editor Agent",
            goal = "Creates a formatted mark down file",
            backstory = "An AI assistant specializes in taking content and presenting it in a well formatted output.",
            verbose=True
        )
        editor_task = Task(
            description="Takes findings and content from the research agent and creates a summarizing table.",
            expected_output="A table outline each companies competitive advantage, technology and innovation. Create a table where each row is about one company. First columns is company name, parameters related to competitive advantage, industry, and specialized technology and innovation. After creating the table, create a paragraph of detailed content for the company.",
            agent=editor_agent
        )

# ✅ Step 5: Create and Run the Crew
        crew = Crew(
            agents=[research_agent, editor_agent],
            tasks=[research_task, editor_task],
            process=Process.sequential,
            manager_llm=ChatOpenAI(model="gpt-4o", 
                                temperature=0.7),
            verbose=True  # Runs tasks one after another
        )
        result = crew.kickoff(inputs = companyinputs)
        response = str(result)

    # (part 1) fine tune model
    # (part 3) agent to convert md into html (inserted into div section) result to response
    # connect to a rag mcp server : 1. file system exposes mcp tool, 2. expose vectorization/indexing mcp tool
    # search can be index as a mcp tool (single mcp server with multiple tools)
    # maintain the session:
    # sessions, use copilotkit as ui approach (react)
    # explore flask render template
    # (part 2) learn to do state management - copilotkit and react
    # fast api vs flask api (render template and state mngt)
        print("Rendering template with response:", response)
        return render_template("index.html", response=response)

@app.route("/react", methods=["GET"])
def hello_react():
    return render_template("react-ui/index.html")

@app.route("/test", methods=["GET"])
def hello_test():
    return render_template("hello_react.html")

if __name__ == "__main__":
    app.run(debug=True)