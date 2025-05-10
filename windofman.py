#!/usr/bin/env -S sh -c '"`dirname $0`/venv/bin/python3" "$0" "$@"'
from keyboardManager import KeyboardManager
from windowManager import WindowManager
from gui import GUIApp


def main():
    wm = WindowManager()
    gui = GUIApp(wm)
    KeyboardManager(wm)

    gui.start()


if __name__ == "__main__":
    main()
