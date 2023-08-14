from ewmh import EWMH
from pathlib import Path
import json
import os

class WindowManager():

    def __init__(self):

        self.ewmh = EWMH()
        self.windows = self.get_windows()
        self.current_window = self.windows[0]
    
        self.__sort_windows()

    def get_windows(self):
        windows = []
        for window in self.ewmh.getClientList():
            if 'Firefox' in self.get_window_name(window):
                windows.append(window)
        return windows

    def print_windows_name(self):
        for window in self.windows:
            print(self.get_window_name(window))

    def next(self):
       self.__switch(True)

    def previous(self):
        self.__switch(False)

    def __switch(self, forward : bool):
        step = 1 if forward else -1
        index = self.windows.index(self.current_window) + step

        if not index < len(self.windows) or not index > 0:
            index = 0

        self.current_window = self.windows[index]

        self.__active_current_window()

    def __active_current_window(self):
        self.ewmh.setActiveWindow(self.current_window)
        self.ewmh.display.flush()

    def __sort_windows(self):
        conf = self.__manage_config_file()
        self.windows = sorted(self.windows, key=lambda w : conf[self.get_window_name(w)])
        print ('ok')

    def __manage_config_file(self) -> dict():
        conf_file = Path("config.json")
        if not conf_file.is_file() :
            with open("config.json",'w') as cf :
                cf.write('{}')
            conf_file = Path("config.json")
        conf = json.load(conf_file.open())

        for window in self.windows:
            if not self.get_window_name(window) in conf:
                conf[self.get_window_name(window)] = 0

        with open("config.json",'w') as cf :
            json.dump(conf, cf)

        return conf

    def get_window_name(self,window) -> str :
        return str(self.ewmh.getWmName(window))