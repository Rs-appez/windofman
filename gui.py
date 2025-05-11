import tkinter as tk
from windowManager import WindowManager

DARK_COLOR = "#1f1f28"
LIGHT_COLOR = "#dcd7ba"


class GUIApp(tk.Tk):
    def __init__(self, wm: WindowManager):
        super().__init__()
        self.wm = wm

        self.title("Windofman")
        self.configure(bg=DARK_COLOR)
        self.protocol("WM_DELETE_WINDOW", self.__on_close)

        localization = self.wm.location
        self.geometry(
            "300x200" + f"+{localization[0]}+{localization[1]}"
            if localization[0] and localization[1]
            else ""
        )
        self.resizable(False, False)

        self.load_config()

        image = tk.PhotoImage("windofman.png")
        self.wm_iconphoto(True, image)

        self.frames = {}
        self.__init_frame()

    def start(self):
        self.go_page(HomePage)
        self.mainloop()

    def __init_frame(self):
        frame_classes = (HomePage, SettingsPage)
        for F in frame_classes:
            frame = F(self)
            frame.grid(row=0, column=0, sticky="nsew")

            self.frames[F] = frame

    def load_config(self):
        self.attributes("-topmost", self.wm.on_top)

    def go_page(self, page):
        try:
            self.frames[page].tkraise()
        except KeyError:
            print(f"Page {page} not found.")

    def __on_close(self):
        self.__save_location()
        self.destroy()

    def __save_location(self):
        location = self.geometry().split("+")[1:]
        if len(location) == 2:
            self.wm.location = (int(location[0]), int(location[1]))
        else:
            self.wm.location = (None, None)
        self.wm.save_settings()


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))
        self.create_widgets()

    def create_widgets(self):
        for character in self.parent.wm.windows:
            character_name = character.name
            row = self.parent.wm.windows.index(character)
            label = tk.Label(
                self,
                text=character_name,
                fg=LIGHT_COLOR,
                bg=DARK_COLOR,
            )
            label.bind(
                "<Button-1>", lambda e, c=character: self.parent.wm.active_window(c)
            )
            label.grid(row=row, column=0, padx=10, pady=10)

        btn_row = self.grid_size()[1]
        self.refresh_button = tk.Button(
            self,
            text="Refresh",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__refresh_windows,
        )
        self.refresh_button.grid(row=btn_row, column=0, padx=10, pady=10)

        self.settings_button = tk.Button(
            self,
            text="Settings",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(SettingsPage),
        )
        self.settings_button.grid(row=btn_row, column=1, padx=10, pady=10)

    def __refresh_windows(self):
        self.parent.wm.get_data()


class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        # settings
        self.on_top_var = tk.BooleanVar(value=self.parent.wm.on_top)

        self.create_widgets()

    def create_widgets(self):
        self.on_top_checkbutton = tk.Checkbutton(
            self,
            text="Always on top",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            variable=self.on_top_var,
        )
        self.on_top_checkbutton.grid(row=0, column=0, padx=10, pady=10)

        btn_row = self.grid_size()[1]
        self.back_button = tk.Button(
            self,
            text="Back to Home",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(HomePage),
        )
        self.back_button.grid(row=btn_row, column=0, padx=10, pady=10)

        self.save_button = tk.Button(
            self,
            text="Save Settings",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__save_settings,
        )
        self.save_button.grid(row=btn_row, column=1, padx=10, pady=10)

    def __save_settings(self):
        self.parent.wm.on_top = self.on_top_var.get()

        self.parent.wm.save_settings()
        self.parent.load_config()
