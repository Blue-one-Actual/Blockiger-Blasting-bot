"""Kleiner Test: bewegt die Maus zur Bildschirmmitte und zurück.

WARNUNG: Dieses Skript steuert die Maus. Drücke 'k' (Hotkey) oder bewege
die Maus in die obere linke Ecke, um abzubrechen (PyAutoGUI-Failsafe).
"""
import time
import logging

try:
    import pyautogui
except Exception:
    pyautogui = None

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

def main():
    logging.info("Starting input test")
    if pyautogui is None:
        logging.error("pyautogui not available in the environment")
        return

    w, h = pyautogui.size()
    cx, cy = w // 2, h // 2
    start_x, start_y = pyautogui.position()
    logging.info("Current pos=(%s,%s); moving to center (%s,%s)", start_x, start_y, cx, cy)
    try:
        pyautogui.moveTo(cx, cy, duration=0.5)
        time.sleep(1.0)
        pyautogui.moveTo(start_x, start_y, duration=0.5)
        logging.info("Returned to original position")
    except Exception as e:
        logging.exception("Input test aborted or failed: %s", e)


if __name__ == '__main__':
    main()
