# Extract structured content from Documents CrewAI

## Overview
This project implements a simple program for:
- Reading documents from the file system.
- Extract structured content from Documents based on multiple criteria.
- Writing the categorized data to the file system.

## Requirements
### Dependencies
Ensure you have the following installed:
- Python 3.x
- `crewAI`
- `crewAI_tools`
- `requests`
- `python-dotenv`

Install dependencies using:
```sh
pip install -r requirements.txt
```

## Setup
1. Clone the repository and navigate to the project directory:
```sh
git clone <repository_url>
cd indent-agentic-repo/exercises/pramod/contentCategorization1/
```

2. Set up environment variables:
   - Create a `.env` file in the project root and add your OpenAI API Key:
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   ```
   - Alternatively, ensure the existing `.env` file is correctly placed and accessible.

## Implementation Details
### Document Storage Path
Documents should be placed inside:
```
C:\tools\LocalGit\indent-agentic-repo\exercises\pramod\contentCategorization1\inputDocs\
```
The program reads and processes the document "Wedbush-Apple March 14 2025.txt" by default.

### Agent & Task Execution
1. **Agent Setup**: A `Financial Research Assistant` agent is created to:
   - Extract structured content from financial documents.
   - Identify stock recommendations (Buy, Sell, Hold).
   - Retrieve target price.
   - Summarize associated risks.

2. **Task Definition**: The agent reads the document and organizes information into three structured columns:
   - **Recommendation**
   - **Target Price**
   - **Risks**

3. **Execution**: A CrewAI workflow is used to process the task sequentially.

## Running the Program
Execute the script using:
```sh
python main.py
```

## Future Enhancements
- Add support for multiple document types.
- Implement a UI for easier interaction.
- Integrate machine learning models for better categorization.

## License
This project is open-source and available for use under the MIT License.

