#!/usr/bin/env -S sh -c '"`dirname $0`/venv/bin/python3" "$0" "$@"'
from keyboardManager import KeyboardManager
from windowManager import WindowManager
from gui import GUIApp

import fcntl
import sys

if __name__ == "__main__":
    lock_file_path = '/tmp/windofman.lock'
    lock_file = open(lock_file_path, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        wm = WindowManager()
        km = KeyboardManager(wm)
        gui = GUIApp(wm, km)

        gui.start()
    except BlockingIOError:
        print("Another instance is already running.")
        sys.exit(1)
