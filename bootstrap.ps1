param(
    [Parameter(Mandatory = $true)][string]$Target,
    [string]$Tool = "auto"
)
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $Root "scripts\install.ps1") --tool $Tool --target $Target
