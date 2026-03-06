# Block Blast Automation Bot (Prototype)

Kurze Anleitung und Startpunkte für den Prototyp (Python).

Setup:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1    # oder aktiviere .venv in deiner Shell
pip install -r requirements.txt
```

Erster Dry-run (kein Klicken, nur Detection logs):

```powershell
.\
un_dry_run.ps1
```

Real-run (führt Klicks aus) — teste vorher die Not-Aus-Taste `k`:

```powershell
.\run_real.ps1
```

Templates:

- Lege Erkennungs-Templates als PNGs unter `templates/` ab (z. B. `templates/block.png`).
- Erzeuge ein Template aus dem aktuellen Bildschirm mit dem Kalibrier-Tool:

```powershell
python tools\calibrate.py --save-template block --x 100 --y 200 --w 64 --h 64
```

Wichtig: Teste zuerst die Not-Aus-Mechanismen (`k` oder Maus in obere linke Ecke) bevor du reale Klicks erlaubst.
# Blockiger-Blasting-bot