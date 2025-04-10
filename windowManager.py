from ewmh import EWMH

from confManager import ConfManager
from tools import get_character_name


class WindowManager:
    def __init__(self):
        self.ewmh = EWMH()
        self.windows = []
        self.ignored = []
        self.current_window = []
        self.on_top = False
        self.location = (None, None)

        self.get_data()

    def get_data(self):
        self.__get_windows()
        self.__get_setting()

    def __get_windows(self):
        windows = []

        for window in self.ewmh.getClientList():
            if self.ewmh.getWmName(window) is not None and (
                b"Dofus 2." in self.ewmh.getWmName(window)
                or self.ewmh.getWmName(window) == b"Dofus"
            ):
                windows.append(window)

        self.windows = windows
        self.sort_windows()
        self.__set_current_window()

    def __get_setting(self):
        settings = ConfManager.get_settings()
        self.on_top = settings["on_top_settings"]
        self.location = (
            settings["location"] if "location" in settings.keys() else (
                None, None)
        )

    def __set_current_window(self):
        self.current_window = self.windows[0] if self.windows else []

    def print_windows_name(self):
        for window in self.windows:
            print(get_character_name(self.ewmh.getWmName(window)))

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

    def __active_window(self, window):
        self.ewmh.setActiveWindow(window)
        self.ewmh.display.flush()

    def active_window_by_ch_name(self, ch_name):
        for window in self.windows:
            if f"{ch_name}".encode() in self.ewmh.getWmName(window):
                self.__active_window(window)
                break

    def close_all_windows(self):
        for window in self.windows:
            self.ewmh.setCloseWindow(window)

    def sort_windows(self):
        try:
            initiative = ConfManager.get_initiative(self.windows, self.ewmh)
            self.windows = sorted(
                self.windows,
                key=lambda w: initiative[get_character_name(self.ewmh.getWmName(w))][
                    "initiative"
                ],
                reverse=True,
            )

            self.__sort_ignored(initiative)

        except Exception:
            pass

    def __sort_ignored(self, initiative):
        ignores_sort = []

        for window in self.windows:
            ignores_sort.append(
                initiative[get_character_name(
                    self.ewmh.getWmName(window))]["ignore"]
            )

        self.ignored = ignores_sort
