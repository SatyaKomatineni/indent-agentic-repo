# README - Simple RAG Implementation

## Purpose
This program demonstrates the implementation of a **Retrieval-Augmented Generation (RAG)** system. RAG is an approach to indexing a set of documents so that user queries in the form of prompts can be answered using relevant retrieved information. The answers are then further enriched by a **Large Language Model (LLM)** to provide more context and depth.

## Features
- Loads and indexes documents using **LlamaIndex**.
- Enables **semantic search** over indexed documents.
- Utilizes **CrewAI** to create an AI agent capable of retrieving and summarizing knowledge from the indexed documents.
- Uses **OpenAI's GPT-3.5-Turbo** as the LLM for enhancing responses.

---

## Installation & Setup
### Prerequisites
Ensure you have Python installed along with the following dependencies:
```sh
pip install crewai llama-index dotenv
```

### Environment Variables
Create a `.env` file in the common directory and set your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```
Ensure that your Python script correctly loads this `.env` file.

---

## How It Works
### 1️⃣ Load and Index Documents
The program loads documents from a specified directory and creates an **index** using LlamaIndex:
```python
documents = SimpleDirectoryReader("C:\\iwe\\WEE Book\\Draft 6\\New").load_data()
index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
```

### 2️⃣ Define a CrewAI Tool for Document Querying
A custom tool `LlamaIndexQueryTool` is created using CrewAI's `BaseTool`. This tool allows agents to query indexed documents:
```python
class LlamaIndexQueryTool(BaseTool):
    name: str = "LlamaIndexQuery"
    description: str = "Searches indexed documents and retrieves relevant information."
    
    def _run(self, query: str):
        return query_engine.query(query).response
```

### 3️⃣ Create an AI Agent
An AI **Research Assistant** is created using CrewAI. This agent specializes in retrieving and summarizing information from research documents:
```python
research_agent = Agent(
    role="Research Assistant",
    goal="Answer knowledge-based questions using a document database.",
    backstory="An AI assistant specializing in retrieving and summarizing information from research papers.",
    verbose=True,
    tools=[LlamaIndexQueryTool()]
)
```

### 4️⃣ Define a Research Task
The agent is assigned a specific research task:
```python
research_task = Task(
    description="Find information about the physics of wind energy.",
    expected_output="A summary of the physics of wind energy.",
    agent=research_agent
)
```

### 5️⃣ Execute the Crew
A **Crew** is created with the agent and task, executing the research process sequentially:
```python
crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    process=Process.sequential
)

result = crew.kickoff()
```
The output of the research process is displayed using Markdown:
```python
from IPython.display import Markdown
Markdown(result.raw)
```

---

## Use Cases
- **Academic Research**: Quickly summarize research papers and books.
- **Enterprise Knowledge Management**: Retrieve information from company documents.
- **Chatbot Integration**: Power chatbots with document-based knowledge retrieval.

---

## Future Enhancements
- Support for multiple document formats (PDF, DOCX, etc.).
- Improve retrieval accuracy using advanced embedding techniques.
- Integration with a web-based UI for interactive queries.

---

## Conclusion
This program is a simple but effective **RAG** implementation using **LlamaIndex** and **CrewAI**. It enables efficient document indexing and knowledge retrieval, making it useful for research, enterprise, and chatbot applications.