@echo off
REM Run Real for Block Blast Bot (Windows CMD)
IF EXIST ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate.bat
)

python src\bot.py --mode run
