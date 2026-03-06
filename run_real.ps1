# Run Real (active input) for Block Blast Bot (PowerShell)
$activate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    try {
        & $activate
    } catch {
        Write-Host "Failed to activate venv, continuing without activation"
    }
}

python .\src\bot.py --mode run
