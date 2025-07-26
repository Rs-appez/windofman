from ewmh import EWMH

from confManager import ConfManager

import time

ewmh = EWMH()


class DofusWindow:
    @staticmethod
    def _get_window_link_number():
        n = 0
        while True:
            yield n
            n += 1

    _window_link_number = _get_window_link_number()

    def __init__(self, window, hypr=None):
        self.hypr = hypr
        self.window = window

        self.name = (
            window.title
            if not "Dofus'"
            else f"Need to be link {next(self._window_link_number)}"
        )

        self.initiative = 0
        self.ignore = False
        self.lastload = int(time.time())

        self.load_initiative()
        self.save_initiative()

        self.__float_window()

    def __str__(self):
        return f"{self.name} {self.initiative} {self.ignore}"

    def __float_window(self):
        self.hypr.dispatch(["setfloating", f"address:{self.window.address}"])

    def activate(self):
        # ewmh.setActiveWindow(self.window)
        # ewmh.display.flush()
        self.hypr.dispatch(["focuswindow", f"address:{self.window.address}"])
        self.hypr.dispatch(["alterzorder", "top"])
        # hypr.dispatch(["fullscreen", "1"])

    def set_name(self, name):
        self.name = name
        self.initiative = 0
        self.ignore = False
        self.load_initiative()
        self.save_initiative()

    def set_initiative(self, initiative: int = None, ignore: bool = None):
        if initiative:
            self.initiative = initiative
        if ignore is not None:
            self.ignore = ignore
        self.save_initiative()

    def load_initiative(self):
        if self.initiative == 0:
            initiative = ConfManager.get_initiative(self.name)
            self.initiative = initiative[self.name]["initiative"]
            self.ignore = initiative[self.name]["ignore"]

    def save_initiative(self):
        initiative = {
            self.name: {
                "initiative": self.initiative,
                "ignore": self.ignore,
                "lastload": self.lastload,
            }
        }
        ConfManager.set_initiative(initiative)


class WindowManager:
    def __init__(self, hypr=None):
        self.ewmh = ewmh
        self.hypr = hypr
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

    def save_initiatives(self):
        for window in self.windows:
            window.save_initiative()

    def get_alls_characters_names(self) -> list:
        characters = ConfManager.get_characters()
        characters.sort(key=lambda c: c[1], reverse=True)

        return [c[0] for c in characters]

    def __get_windows(self):
        windows = []
        old_windows = [w.window for w in self.windows]
        old_windows_address = [w.address for w in old_windows]

        for window in self.hypr.get_windows():
            window_class = window.wm_class

            if window_class == "Dofus.x64":
                if window.address in old_windows_address:
                    windows.append(
                        [w for w in self.windows if w.window.address == window.address][
                            0
                        ]
                    )
                else:
                    windows.append(DofusWindow(window, self.hypr))

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
        if not self.windows:
            return
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
        self.windows = sorted(
            self.windows,
            key=lambda w: w.initiative,
            reverse=True,
        )

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
