from ewmh import EWMH

from confManager import ConfManager
from tools import get_character_name

ewmh = EWMH()


class DofusWindow:
    def __init__(self, window):
        self.window = window
        self.name = get_character_name(ewmh.getWmName(window))

    def __str__(self):
        return f"{self.name}"


class WindowManager:
    def __init__(self):
        self.ewmh = ewmh
        self.windows = []
        self.ignored = []
        self.current_window = []
        self.on_top = False
        self.location = (None, None)

        self.get_data()

    def get_data(self):
        self.__get_windows()
        self.__get_setting()

    def save_settings(self):
        settings = {
            "on_top_settings": self.on_top,
            "location": self.location,
        }
        ConfManager.set_settings(settings)

    def __get_windows(self):
        windows = []

        for window in self.ewmh.getClientList():
            window_name = self.ewmh.getWmName(window)
            if window_name is not None and (
                b"Dofus 3." in window_name or window_name == b"Dofus"
            ):
                windows.append(DofusWindow(window))

        self.windows = windows
        self.sort_windows()
        self.__set_current_window()

    def __get_setting(self):
        settings = ConfManager.get_settings()
        self.on_top = settings["on_top_settings"]
        self.location = (
            settings["location"] if "location" in settings.keys() else (None, None)
        )

    def __set_current_window(self):
        self.current_window = self.windows[0] if self.windows else []

    def print_windows_name(self):
        for window in self.windows:
            print(window.name)

    def next(self):
        self.__switch(1)

    def previous(self):
        self.__switch(0)

    def __switch(self, forward: bool):
        step = 1 if forward else -1
        index = self.windows.index(self.current_window) + step

        if not index < len(self.windows):
            index = 0
        elif index < 0:
            index = len(self.windows) - 1

        self.current_window = self.windows[index]

        if self.ignored[index]:
            try:
                return self.__switch(forward)
            except RecursionError:
                return

        self.__active_current_window()

    def __active_current_window(self):
        self.__active_window(self.current_window)

    def __active_window(self, window: DofusWindow):
        self.ewmh.setActiveWindow(window.window)
        self.ewmh.display.flush()

    def active_window_by_ch_name(self, ch_name):
        for window in self.windows:
            if f"{ch_name}".encode() in window.name:
                self.__active_window(window)
                break

    def close_all_windows(self):
        for window in self.windows:
            self.ewmh.setCloseWindow(window.window)

    def sort_windows(self):
        try:
            initiative = ConfManager.get_initiative(self.windows)
            self.windows = sorted(
                self.windows,
                key=lambda w: initiative[w.name][
                    "initiative"
                ],
                reverse=True,
            )

            self.__sort_ignored(initiative)

        except Exception as e:
            print(f"Error sorting windows : {e}")
            pass

    def __sort_ignored(self, initiative):
        ignores_sort = []

        for window in self.windows:
            ignores_sort.append(
                initiative[window.name]["ignore"]
            )

        self.ignored = ignores_sort
