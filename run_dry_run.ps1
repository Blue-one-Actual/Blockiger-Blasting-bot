# Run Dry-Run for Block Blast Bot (PowerShell)
# Activates venv if present, then runs the bot in dry-run mode
$activate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    try {
        & $activate
    } catch {
        Write-Host "Failed to activate venv, continuing without activation"
    }
}

python .\src\bot.py --mode dry-run
