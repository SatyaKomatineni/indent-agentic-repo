#!/usr/bin/env python3
"""
MyCLI Framework - Object-Oriented Command Line Tool Framework

Provides interfaces and base classes for creating command line tools with parameter negotiation.
"""
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Callable, Type, Protocol, runtime_checkable


class Parameter:
    """Parameter definition for CLI tools."""
    
    def __init__(
        self,
        name: str,
        prompt: str,
        required: bool = True,
        position: Optional[int] = None,
        param_type: Type = str,
        default_value: Optional[Any] = None,
        default_from_param: Optional[str] = None,
        default_transform: Optional[Callable[[Any], Any]] = None,
        prompt_from_param: Optional[str] = None,
        validator: Optional[Callable[[Any], Union[Any, None]]] = None
    ):
        """
        Initialize a parameter definition.
        
        Args:
            name: Parameter name
            prompt: Base prompt to show user when asking for this parameter
            required: Whether this parameter is required
            position: Position in command line arguments (0-indexed)
            param_type: Type of the parameter (str, int, float, etc.)
            default_value: Static default value
            default_from_param: Name of another parameter to base default on
            default_transform: Function to transform value from another parameter
            prompt_from_param: Name of parameter to pass to get_prompt_text
            validator: Custom validation function
        """
        self.name = name
        self.base_prompt = prompt
        self.required = required
        self.position = position
        self.param_type = param_type
        self.default_value = default_value
        self.default_from_param = default_from_param
        self.default_transform = default_transform
        self.prompt_from_param = prompt_from_param
        self.validator = validator
        self.value = None
    
    def get_default(self, params: Dict[str, 'Parameter']) -> Optional[Any]:
        """Get default value, possibly based on another parameter."""
        if self.default_value is not None:
            return self.default_value
            
        if self.default_from_param and self.default_from_param in params:
            source_param = params[self.default_from_param]
            if source_param.value is not None:
                if self.default_transform:
                    return self.default_transform(source_param.value)
                return source_param.value
                
        return None
        
    def convert_type(self, value: str) -> Any:
        """Convert string value to the parameter's type."""
        if value is None or value == "":
            return None
            
        try:
            return self.param_type(value)
        except (ValueError, TypeError) as e:
            print(f"Error: Cannot convert '{value}' to {self.param_type.__name__}: {str(e)}")
            return None
        
    def validate(self, value: Any) -> Optional[Any]:
        """Validate parameter value."""
        if value is None and self.required:
            print(f"Error: Parameter '{self.name}' is required.")
            return None
            
        if self.validator and value is not None:
            return self.validator(value)
            
        return value


@runtime_checkable
class MyCLIInterface(Protocol):
    """Pure interface for MyCLI framework classes."""
    
    @property
    def name(self) -> str:
        """Get the name of the CLI tool."""
        ...
    
    @property
    def description(self) -> str:
        """Get the description of the CLI tool."""
        ...
    
    @property
    def params(self) -> Dict[str, Parameter]:
        """Get the parameters for the CLI tool."""
        ...
    
    def add_param(self, param: Parameter) -> 'MyCLIInterface':
        """Add a parameter to the tool."""
        ...
    
    def show_help(self) -> None:
        """Display help information for the tool."""
        ...
    
    def get_prompt_text(self, param_name: str, dependent_value: Any) -> Optional[str]:
        """Get custom prompt text for a parameter based on a dependent parameter's value."""
        ...
    
    def get_param_value(self, param: Parameter, args: List[str]) -> Optional[Any]:
        """Get parameter value through negotiation."""
        ...
    
    def parse_args(self) -> bool:
        """Parse command line arguments and negotiate parameter values."""
        ...
    
    def get_param(self, name: str) -> Any:
        """Get parameter value by name."""
        ...
    
    def run_tool(self) -> int:
        """Run the tool with the provided parameters."""
        ...
    
    def execute(self) -> int:
        """Execute the tool."""
        ...


class MyCLI(ABC):
    """Abstract base implementation of MyCLIInterface."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize a CLI tool.
        
        Args:
            name: Tool name
            description: Tool description
        """
        self._name = name
        self._description = description
        self._params: Dict[str, Parameter] = {}
    
    @property
    def name(self) -> str:
        """Get the name of the CLI tool."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get the description of the CLI tool."""
        return self._description
    
    @property
    def params(self) -> Dict[str, Parameter]:
        """Get the parameters for the CLI tool."""
        return self._params
        
    def add_param(self, param: Parameter) -> 'MyCLI':
        """
        Add a parameter to the tool.
        
        Args:
            param: Parameter definition
            
        Returns:
            Self for method chaining
        """
        self._params[param.name] = param
        return self
        
    def show_help(self) -> None:
        """Display help information for the tool."""
        print(f"{self.name}")
        print("=" * len(self.name))
        print(f"\n{self.description}\n")
        
        print("Usage:")
        print(f"  {sys.argv[0]} [options] [parameters]")
        
        print("\nOptions:")
        print("  -help    Show this help message")
        print("  -run     Run the tool with parameter prompts")
        
        print("\nParameters:")
        for param in self.params.values():
            if param.position is not None:
                position_info = f"[position {param.position}]"
            else:
                position_info = ""
                
            req = "required" if param.required else "optional"
            type_info = f"({param.param_type.__name__})"
            print(f"  {param.name} {type_info} {position_info}: {param.base_prompt}")
            
            if param.default_value is not None:
                print(f"    Default: {param.default_value}")
            elif param.default_from_param:
                source = f"{param.default_from_param}"
                if param.default_transform:
                    source += " (transformed)"
                print(f"    Default: based on {source}")
                
        print("\nExample usage:")
        print(f"  {sys.argv[0]}")
        print(f"  {sys.argv[0]} -run")
        
        # Generate example with positional parameters
        positional = sorted(
            [(p.position, p.name) for p in self.params.values() if p.position is not None],
            key=lambda x: x[0]
        )
        if positional:
            example = f"  {sys.argv[0]}"
            for _, name in positional:
                example += f" <{name}>"
            print(example)
    
    def get_prompt_text(self, param_name: str, dependent_value: Any) -> Optional[str]:
        """
        Get custom prompt text for a parameter based on a dependent parameter's value.
        This method should be overridden in subclasses to provide custom prompts.
        
        Args:
            param_name: Name of the parameter being prompted
            dependent_value: Value of the dependent parameter
            
        Returns:
            Custom prompt text, or None to use the default
        """
        # Base implementation returns None to use the default prompt
        return None
    
    def get_param_value(self, param: Parameter, args: List[str]) -> Optional[Any]:
        """
        Get parameter value through negotiation.
        
        Args:
            param: Parameter to get value for
            args: Command line arguments
            
        Returns:
            Parameter value or None if validation fails
        """
        raw_value = None
        
        # Try to get from positional argument
        if param.position is not None and param.position < len(args):
            raw_value = args[param.position]
        
        # If no value yet, get default
        default = param.get_default(self.params)
        
        # Determine prompt text - either from base prompt or from dependent parameter
        prompt_text = param.base_prompt
        custom_value = ""
        if param.prompt_from_param and param.prompt_from_param in self.params:
            dependent_value = self.params[param.prompt_from_param].value
            if dependent_value is not None:
                custom_value = self.get_prompt_text(param.name, dependent_value)
                if custom_value:
                    prompt_text = f'{param.base_prompt} [{custom_value}]'
        
        # If still no value, prompt user (with default if available)
        if raw_value is None:
            if default is not None:
                raw_value = input(prompt_text)
                if not raw_value.strip():
                    # empty string, use default
                    raw_value = custom_value
            else:
                # default is None
                raw_value = input(f"{prompt_text}: ")
        
        # Convert to correct type
        if (raw_value is None):
            raw_value = ""
        typed_value = param.convert_type(raw_value)
        
        # Validate
        return param.validate(typed_value)
    
    def parse_args(self) -> bool:
        """
        Parse command line arguments and negotiate parameter values.
        
        Returns:
            True if successful, False otherwise
        """
        args = sys.argv[1:]
        
        # Handle help option
        if len(args) == 0 or "-help" in args:
            self.show_help()
            return False
        
        # Remove -run if present
        if "-run" in args:
            args.remove("-run")
        
        # Collect non-option arguments
        non_option_args = [arg for arg in args if not arg.startswith("-")]
        
        # Process parameters in order of position (when specified)
        ordered_params = sorted(
            self.params.values(),
            key=lambda p: p.position if p.position is not None else float('inf')
        )
        
        # Negotiate parameters
        for param in ordered_params:
            value = self.get_param_value(param, non_option_args)
            
            if value is None and param.required:
                return False
            
            param.value = value
        
        return True
    
    def get_param(self, name: str) -> Any:
        """
        Get parameter value by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter value or None if not set
        """
        if name in self.params:
            return self.params[name].value
        return None
    
    @abstractmethod
    def run_tool(self) -> int:
        """
        Run the tool with the provided parameters.
        
        Returns:
            Exit code (0 for success)
        """
        pass
    
    def execute(self) -> int:
        """
        Execute the tool.
        
        Returns:
            Exit code (0 for success)
        """
        if not self.parse_args():
            return 1
        
        try:
            return self.run_tool()
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1


# Example implementation
class DataExtractionTool(MyCLI):
    """Example implementation of a data extraction tool."""
    
    def __init__(self):
        super().__init__(
            "Data Extraction Tool",
            "Extracts data from input sources based on prompts."
        )
        
        # Add parameters with type specification
        self.add_param(Parameter(
            name="source",
            prompt="Enter data source",
            required=True,
            param_type=str,
            position=0
        ))
        
        # Notice we use prompt_from_param to customize the prompt based on source
        self.add_param(Parameter(
            name="prompt",
            prompt="Enter prompt source",  # Base prompt text
            required=True,
            param_type=str,
            position=1,
            default_from_param="source",
            default_transform=lambda s: f"{s}_prompt",
            prompt_from_param="source"  # This parameter's prompt will be based on "source"
        ))
        
        # Example of an integer parameter
        self.add_param(Parameter(
            name="iterations",
            prompt="Number of processing iterations",
            required=False,
            param_type=int,
            default_value=1
        ))
    
    # Override to provide custom prompts based on dependent values
    def get_prompt_text(self, param_name: str, dependent_value: Any) -> Optional[str]:
        if param_name == "prompt" and dependent_value:
            return f"Enter prompt for processing '{dependent_value}'"
        return None
    
    def run_tool(self) -> int:
        """Run the data extraction logic."""
        source = self.get_param("source")
        prompt = self.get_param("prompt")
        iterations = self.get_param("iterations")
        
        print(f"Running data extraction with:")
        print(f"  Source: {source}")
        print(f"  Prompt: {prompt}")
        print(f"  Iterations: {iterations}")
        
        # Your data extraction logic would go here
        print("Data extraction completed successfully!")
        
        return 0


# Example usage
if __name__ == "__main__":
    stool = DataExtractionTool()
    sys.exit(stool.execute())