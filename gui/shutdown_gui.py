import threading
try:
    import tkinter as tk
except Exception:
    tk = None


def open_shutdown_window(stop_event):
    if tk is None:
        print("Tkinter not available; GUI stop window cannot be shown")
        return

    def on_stop():
        stop_event.set()
        root.destroy()

    root = tk.Tk()
    root.title("Bot Stop")
    btn = tk.Button(root, text="STOP BOT", fg="white", bg="red", command=on_stop)
    btn.pack(padx=20, pady=20)
    threading.Thread(target=root.mainloop, daemon=True).start()
