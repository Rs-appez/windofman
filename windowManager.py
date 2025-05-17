from ewmh import EWMH

from confManager import ConfManager
from tools import get_character_name

ewmh = EWMH()


class DofusWindow:
    @staticmethod
    def _get_window_link_number():
        n = 0
        while True:
            yield n
            n += 1

    _window_link_number = _get_window_link_number()

    def __init__(self, window):
        self.window = window

        character_name = get_character_name(ewmh.getWmName(window))
        self.name = (
            character_name
            if not "Dofus'"
            else f"Need to be link {next(self._window_link_number)}"
        )

        self.initiative = 0
        self.ignore = False

    def __str__(self):
        return f"{self.name} {self.initiative} {self.ignore}"

    def activate(self):
        ewmh.setActiveWindow(self.window)
        ewmh.display.flush()

    def set_name(self, name):
        self.name = name

    def load_initiative(self):
        initiative = ConfManager.get_initiative(self.name)
        self.initiative = initiative[self.name]["initiative"]
        self.ignore = initiative[self.name]["ignore"]


class WindowManager:
    def __init__(self):
        self.ewmh = ewmh
        self.windows = []
        self.ignored = []
        self.current_window = []
        self.on_top = False
        self.location = (None, None)

        self.window_to_link = None

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

    def save_initiative(self, values):
        ConfManager.set_initiative(values)

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
        self.current_window.activate()

    def activate_window(self, window: DofusWindow):
        self.current_window = window
        self.__active_current_window()

    def close_all_windows(self):
        for window in self.windows:
            self.ewmh.setCloseWindow(window.window)

    def sort_windows(self):
        self.__get_initiatives()
        self.windows = sorted(
            self.windows,
            key=lambda w: w.initiative,
            reverse=True,
        )

    def __get_initiatives(self):
        for window in self.windows:
            window.load_initiative()

        self.__sort_ignored()

    def __sort_ignored(self):
        ignores_sort = []

        for window in self.windows:
            ignores_sort.append(window.ignore)

        self.ignored = ignores_sort

    def set_name_to_link(self, name: str):
        if self.window_to_link is not None:
            self.window_to_link.set_name(name)
            self.window_to_link = None
        else:
            print("No window to link")
