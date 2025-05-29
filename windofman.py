#!/usr/bin/env -S sh -c '"`dirname $0`/venv/bin/python3" "$0" "$@"'
from keyboardManager import KeyboardManager
from windowManager import WindowManager
from gui import GUIApp


if __name__ == "__main__":
    wm = WindowManager()
    km = KeyboardManager(wm)
    gui = GUIApp(wm, km)

    gui.start()
