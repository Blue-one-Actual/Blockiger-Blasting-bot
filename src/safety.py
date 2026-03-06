import logging
import threading

try:
    import keyboard
except Exception:
    keyboard = None

try:
    import pyautogui
    pyautogui.FAILSAFE = True
except Exception:
    pyautogui = None


def init_stop_handlers(stop_event):
    """Set up a global hotkey (Ctrl+Shift+X) to set `stop_event`.

    Falls `keyboard` nicht installiert ist, starte einen Thread, der auf Enter in der Konsole wartet.
    """
    if keyboard is not None:
        try:
            # Emergency stop bound to single key 'k' as requested
            keyboard.add_hotkey('k', lambda: _set(stop_event))
            logging.info("Registered hotkey 'K' for emergency stop")
        except Exception:
            logging.exception("Failed to register global hotkey; falling back to console input")
            _start_console_watcher(stop_event)
    else:
        logging.warning("keyboard module not available; use console Enter to stop")
        _start_console_watcher(stop_event)


def _start_console_watcher(stop_event):
    def waiter():
        try:
            input("Press Enter to stop the bot...\n")
            _set(stop_event)
        except Exception:
            _set(stop_event)

    t = threading.Thread(target=waiter, daemon=True)
    t.start()


def _set(stop_event):
    logging.info("Emergency stop triggered")
    stop_event.set()
