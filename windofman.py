#!/usr/bin/env -S sh -c '"`dirname $0`/venv/bin/python3" "$0" "$@"'
from hyprpy import Hyprland

from keyboardManager import KeyboardManager
from windowManager import WindowManager
from gui import GUIApp

import fcntl
import os
import socket
import threading


def focus_listener(gui: GUIApp):
    sock_path = "/tmp/windofman.sock"
    if os.path.exists(sock_path):
        os.remove(sock_path)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(sock_path)
    server.listen(1)
    while True:
        conn, _ = server.accept()
        data = conn.recv(1024)
        if data == b"focus":
            gui.focus_window()
        conn.close()


if __name__ == "__main__":
    hypr = Hyprland()
    lock_file_path = "/tmp/windofman.lock"
    lock_file = open(lock_file_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)

        wm = WindowManager(hypr=hypr)
        km = KeyboardManager(wm)
        gui = GUIApp(wm, km, hypr=hypr)

        listener_thread = threading.Thread(
            target=focus_listener, args=(gui,), daemon=True
        )
        listener_thread.start()

        gui.start()

    except BlockingIOError:
        print("Another instance is already running.")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect("/tmp/windofman.sock")
        sock.sendall(b"focus")
        sock.close()
