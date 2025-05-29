from pynput import keyboard
from windowManager import WindowManager
from confManager import ConfManager
import threading


class KeyboardManager:
    def __init__(self, windowManager: WindowManager):
        self.alt_pressed = False
        self.windowManager = windowManager

        self.next_key = keyboard.Key.f2
        self.previous_key = keyboard.Key.f3
        self.set_keys()

        self.start_thread()

    def set_keys(self):
        keys = ConfManager.get_keybinds()
        self.next_key = self.__parse_key(keys["next"])
        self.previous_key = self.__parse_key(keys["previous"])

    def __parse_key(self, key_str):
        try:
            key = key_str.lower()
            # Try special keys (e.g., f2, f3, alt)
            return getattr(keyboard.Key, key)
        except AttributeError:
            # Fallback to single character keys
            return keyboard.KeyCode.from_char(key_str)

    def on_press(self, key):
        if key == keyboard.Key.alt:
            self.alt_pressed = True

        try:
            if key == self.next_key:
                self.windowManager.next()
            if key == self.previous_key:
                self.windowManager.previous()
        except AttributeError:
            return

    def on_release(self, key):
        if key == keyboard.Key.alt:
            self.alt_pressed = False

    def start_thread(self):
        thread = threading.Thread(target=self.run, args=[])
        thread.daemon = True
        thread.start()

    def run(self):
        with keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()
