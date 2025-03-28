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
from dotenv import load_dotenv
from crewai_tools import FileReadTool

def get_research_agent(file_read_tool, prompt_read_tool):
    return Agent(
        role="Financial Research Assistant",
        goal="Structured content and data extraction from an input document using a prompt document as the rule."
             " Read the input document using the file read tool"
             " Read the prompt document using the prompt read tool to apply the prompt against that input document."
             " Return the output as indicated by the prompt",
        backstory="An AI assistant specializing in retrieving structured content and summarizing information from articles about stocks.",
        verbose=True,
        tools=[file_read_tool, prompt_read_tool]
    )

def get_research_task(agent):
    return Task(
        description="Use the Research Assistant Agent to read the input document and apply the prompt rules to extract structured data.",
        expected_output="Create 3 columns of content based on the three dimensions: Recommendation, Target Price and Risks",
        agent=agent
    )

def validate_environment_variables():
    """Validate that required environment variables are set."""
    required_env_vars = ["OPENAI_MODEL_NAME", "OPENAI_API_KEY"]
    for var in required_env_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Environment variable {var} is not set.")

def set_environment_for_crew():
    load_dotenv()
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
    # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def validate_path(path):
    """Validate if the given path exists."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path does not exist: {path}")

def validate_file_paths(file_path, prompt_path):
    """Validate the input document and prompt file paths."""
    validate_path(file_path)
    validate_path(prompt_path)

def run_data_extraction(file_path, prompt_path):
    set_environment_for_crew()

    # Validate paths before proceeding
    validate_file_paths(file_path, prompt_path)
    validate_environment_variables()

    file_read_tool = FileReadTool(file_path=file_path)
    prompt_read_tool = FileReadTool(file_path=prompt_path)

    research_agent = get_research_agent(file_read_tool, prompt_read_tool)
    research_task = get_research_task(research_agent)

    crew = Crew(
        agents=[research_agent],
        tasks=[research_task],
        process=Process.sequential  # Runs tasks one after another
    )

    result = crew.kickoff()
    return result

def get_file_paths(doc_storage_path):
    file_path = os.path.join(doc_storage_path, "Wedbush-Apple March 14 2025.txt")
    prompt_path = os.path.join(doc_storage_path, "..\\prompt_rules\\cat_prompt.txt")
    return file_path, prompt_path

# Example usage:
if __name__ == "__main__":
    DOC_STORAGE_PATH = ".\\exercises\\pramod\\contentCategorization1\\inputDocs\\"
    file_path, prompt_path = get_file_paths(DOC_STORAGE_PATH)
    
    output = run_data_extraction(file_path, prompt_path)
    print("\n🔍 Research Output:", output)


