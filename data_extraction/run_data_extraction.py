"""
*************************************************
* Run data extraction command: python run_data_extraction.py
*************************************************
Goal:
1. Take two files as inputs
2. First is a domain specific unstructured file
3. Second is a prompt to extract structured data
4. Call the crew_data_extraction.py to extract

Logic:
1. instructions for the LLM
2. Create a batch file using typer library
3. It should take 2 file inputs
Use CrewAI to extract structured data Run the data extraction process

Approach:

Hello,
See if you can help me craft a batch file in python that works like this

1. if typed directly invoke -help
2. if typed with -run then prompt for the input filename
3. if the input filepath exists, prompt the "input filename.prompt.txt" 
   as the second file and prompt it as a default for the user to override
4. if typed with not an option starting with a "-" but a filename, ]
    use that as the input filename and prompt for the second file usign the previous approach
5. if both filenames are provided, run the data extraction process after validating the files
6. Assume the data extraction process to run is in a function called run_data_extraction(filename, prompt_filename)
7. See if you can generalize it where the parameters are positional and also prompted when not available
8. Allow some configuration at the beginning of the .py file to set this kind of parameters
9. Use "typer" library to create the batch file if it helps with any of this

*************************************************
End of global comment
"""
import sys
from data_extraction.TestCLI import MyCLI
from data_extraction.TestCLI import Parameter
import os

from typing import Dict, List, Any, Optional, Union, Callable, Type, Protocol, runtime_checkable
from pathlib import Path

#*************************************************
# Actual run imports
#*************************************************
from data_extraction.crew_data_extraction import run_data_extraction

def getPromptFilename(source: str) -> str:
    path = Path(source)
    parent = path.parent
    basename = path.stem
    ext = path.suffix
    return os.path.join(parent, f"{basename}.prompt.txt")

class DETool(MyCLI):
    """Example implementation of a data extraction tool."""
    
    def __init__(self):
        super().__init__(
            "Data Extraction Tool",
            "Extracts data from input sources based on prompts."
        )
        
        # Add parameters with type specification
        self.add_param(Parameter(
            name="source",
            prompt="Enter data source filename",
            required=True,
            param_type=str,
            position=0
        ))
        
        # Notice we use prompt_from_param to customize the prompt based on source
        self.add_param(Parameter(
            name="prompt_filename",
            prompt="Enter prompt filename",  # Base prompt text
            required=True,
            param_type=str,
            position=1,
            default_from_param="source",
            prompt_from_param="source"  # This parameter's prompt will be based on "source"
        ))
        
    
    # Override to provide custom prompts based on dependent values
    def get_prompt_text(self, param_name: str, dependent_value: Any) -> Optional[str]:
        if not (param_name == "prompt_filename" and dependent_value):
            return None
        return getPromptFilename(dependent_value)
    
    def run_tool(self) -> int:
        """Run the data extraction logic."""
        source = self.get_param("source")
        prompt = self.get_param("prompt_filename")
        
        print(f"Running data extraction with:")
        print(f"  Source: {source}")
        print(f"  Prompt: {prompt}")
        
        run_data_extraction(source, prompt);
        # Your data extraction logic would go here
        print("Data extraction completed successfully!")
        
        return 0

tool = DETool()
sys.exit(tool.execute())