import logging
import time

try:
    import pyautogui
except Exception:
    pyautogui = None


def click_at(x, y, stop_event=None):
    """Move to (x,y) and click. Respects `stop_event` if provided.

    Uses `pyautogui` when available; otherwise logs the action.
    """
    if stop_event is not None and stop_event.is_set():
        logging.info("Stop event set; aborting click")
        return

    if pyautogui is not None:
        try:
            pyautogui.moveTo(x, y, duration=0.12)
            if stop_event is not None and stop_event.is_set():
                logging.info("Stop event set before click; aborting")
                return
            pyautogui.click()
            logging.info("Clicked at (%s,%s)", x, y)
        except Exception as e:
            logging.exception("pyautogui click failed: %s", e)
    else:
        logging.info("(Simulated) click at (%s,%s)", x, y)
        time.sleep(0.05)
