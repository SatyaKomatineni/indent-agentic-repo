#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Data extraction script using control files.
.DESCRIPTION
    This script performs data extraction based on a control file and home directory.
.NOTES
    File Name: crew-extract.ps1
#>

function help() {
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

function validate($homedir, $controlfile) {
    # Check if homedir is properly set
    if ([string]::IsNullOrEmpty($homedir)) {
        Write-Host "Error: data_extraction_home environment variable is not set"
        return $false
    }

    # Check if control file exists
    if (-not (Test-Path -Path $controlfile -PathType Leaf)) {
        Write-Host "Error: Control file not found: $controlfile"
        return $false
    }

    return $true
}

function execute($homedir, $controlfile) {
    Write-Host "Executing data extraction with:"
    Write-Host "  Home Directory: $homedir"
    Write-Host "  Control File: $controlfile"
}

function main {
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
    
    # Display help if -help/-h is specified or if -run is not specified
    if ($Help -or -not $Run) {
        help
        return 0
    }
    
    # At this point we know -run is specified and -help/-h is not
    
    # Check if control file is provided
    if ([string]::IsNullOrEmpty($ControlFile)) {
        Write-Host "Error: Missing control file argument"
        help
        return 1
    }
    
    # Resolve the full path of the control file
    $controlFileFullPath = Resolve-Path $ControlFile -ErrorAction SilentlyContinue
    
    # If resolution failed, use the input path
    if (-not $controlFileFullPath) {
        $controlFileFullPath = $ControlFile
    }
    
    # Get homedir from environment variable
    $homedir = $env:data_extraction_home
    
    # Validate inputs
    if (-not (validate $homedir $controlFileFullPath)) {
        # Display help when validation fails
        help
        return 1
    }
    
    # Execute the process
    execute $homedir $controlFileFullPath
    return 0
}

# Call the main function (PowerShell automatically passes arguments to the param block)
$exitCode = main
exit $exitCode