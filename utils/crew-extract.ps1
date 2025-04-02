#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Data extraction script using control files.
.DESCRIPTION
    This script performs data extraction based on a control file and home directory.
.NOTES
    File Name: crew-extract.ps1
#>

# Define parameters at the script level
[CmdletBinding()]
param (
    [Parameter(Position=0)]
    [string]$ControlFile,
    
    [Parameter()]
    [switch]$Run,
    
    [Parameter()]
    [Alias("h")]
    [switch]$Help
)

# Function to display help information
function help {
    Write-Host "Usage: .\crew-extract.ps1 <controlfile> [-run] | [-help|-h]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -run     Run the extraction process"
    Write-Host "  -help    Display this help message"
    Write-Host "  -h       Display this help message"
    Write-Host ""
    Write-Host "Arguments:"
    Write-Host "  controlfile    The control file for extraction"
    Write-Host ""
    Write-Host "Environment Variables:"
    Write-Host "  data_extraction_home    Home directory for data extraction"
}

# Function to handle run/help logic and return whether to continue
function dealWithRunHelp {
    param (
        [switch]$Run,
        [switch]$Help
    )
    
    # Show help if requested or if -run is not specified
    if ($Help -or -not $Run) {
        help
        return $false
    }
    
    return $true
}

# Function to validate parameters
function validate {
    param (
        [string]$ControlFile,
        [string]$HomeDir
    )
    
    # Check if controlFile is provided
    if ([string]::IsNullOrEmpty($ControlFile)) {
        Write-Host "Error: Missing control file argument"
        return $false
    }
    
    # Check if homedir is properly set
    if ([string]::IsNullOrEmpty($HomeDir)) {
        Write-Host "Error: data_extraction_home environment variable is not set"
        return $false
    }
    
    # Resolve the full path of the control file
    $controlFileFullPath = Resolve-Path $ControlFile -ErrorAction SilentlyContinue
    
    # If resolution failed, use the input path
    if (-not $controlFileFullPath) {
        $controlFileFullPath = $ControlFile
    } else {
        $ControlFile = $controlFileFullPath.Path
    }
    
    # Check if control file exists
    if (-not (Test-Path -Path $ControlFile -PathType Leaf)) {
        Write-Host "Error: Control file not found: $ControlFile"
        return $false
    }
    
    # If all validations pass, return true
    return $true
}

# Function to execute the extraction
function execute {
    param (
        [string]$ControlFile
    )
    
    # Get homedir from environment variable
    $homedir = $env:data_extraction_home
    
    Write-Host "Executing data extraction with:"
    Write-Host "  Home Directory: $homedir"
    Write-Host "  Control File: $ControlFile"
    
    # Actual extraction logic would go here
    
    return 0
}

# Main function to orchestrate the script
function main {
    param (
        [string]$ControlFile,
        [switch]$Run,
        [switch]$Help
    )
    
    # Check run/help flags first
    $shouldContinue = dealWithRunHelp -Run:$Run -Help:$Help
    if (-not $shouldContinue) {
        return 0
    }
    
    # Get homedir from environment variable
    $homedir = $env:data_extraction_home
    
    # Validate parameters
    if (-not (validate -ControlFile $ControlFile -HomeDir $homedir)) {
        help
        return 1
    }
    
    # Execute the process
    return (execute -ControlFile $ControlFile)
}

# Call the main function with script parameters
$exitCode = main -ControlFile $ControlFile -Run:$Run -Help:$Help
exit $exitCode