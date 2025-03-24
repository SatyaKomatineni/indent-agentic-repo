<#
A script to deactivate the current python environment.

1. Uses a global function that is defined in the activate.ps1 script itself..
2. This global function is resident in the current session making it available for calling.

#>
Write-host "Deactivating..."

deactivate