@echo off
REM Run Dry-Run for Block Blast Bot (Windows CMD)
IF EXIST ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate.bat
)

python src\bot.py --mode dry-run
