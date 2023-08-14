from ewmh import EWMH

class WindowManager():

    def __init__(self):

        self.ewmh = EWMH()
        self.windows = self.get_windows()
        self.current_window = self.windows[0]
    
    def get_windows(self):
        windows = []
        for window in self.ewmh.getClientList():
            if b'Firefox' in self.ewmh.getWmName(window):
                windows.append(window)
        return windows

    def print_windows_name(self):
        for window in self.windows:
            print(self.ewmh.getWmName(window))

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

        self.active_current_window()

    def active_current_window(self):
        self.ewmh.setActiveWindow(self.current_window)
        self.ewmh.display.flush()