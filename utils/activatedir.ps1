param (
    [string]$dir
)

# Check if a directory argument is provided
if (-Not $dir) {
    Write-Host "Error: No directory specified. Please provide a directory path as an argument." -ForegroundColor Red
    Write-Host "Usage: .\activatedir.ps1 <directory-path>" -ForegroundColor Yellow
    exit 1
}

# Check if the directory exists
if (-Not (Test-Path -Path $dir -PathType Container)) {
    Write-Host "Error: The specified directory '$dir' does not exist." -ForegroundColor Red
    exit 1
}

# Check if .venv directory exists inside it
$venvPath = Join-Path -Path $dir -ChildPath ".venv"
if (-Not (Test-Path -Path $venvPath -PathType Container)) {
    Write-Host "Error: No virtual environment found in '$dir' (.venv directory missing)." -ForegroundColor Red
    exit 1
}

# Change to the directory
Set-Location -Path $dir

# Activate the virtual environment
$activateScript = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
if (Test-Path -Path $activateScript) {
    Write-Host "Activating virtual environment in '$dir'..." -ForegroundColor Green
    & $activateScript
} else {
    Write-Host "Error: Activation script not found in '$venvPath\Scripts'." -ForegroundColor Red
    exit 1
}
