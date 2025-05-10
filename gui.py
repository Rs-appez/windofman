import tkinter as tk
from windowManager import WindowManager

bg_color = "#1f1f28"


class GUIApp(tk.Tk):
    def __init__(self, wm: WindowManager):
        super().__init__()
        self.wm = wm

        self.title("Windofman")
        self.configure(bg=bg_color)

        localization = self.wm.location
        self.geometry(
            "300x200" + f"+{localization[0]}+{localization[1]}"
            if localization[0] and localization[1]
            else ""
        )
        self.resizable(False, False)

        self.load_config()

        image = tk.PhotoImage(file="windofman.png")
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


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=bg_color)
        self.create_widgets()

    def create_widgets(self):
        self.refresh_button = tk.Button(self, text="Refresh")
        self.refresh_button.pack(pady=10)

        self.settings_button = tk.Button(
            self, text="Settings", command=lambda: self.parent.go_page(SettingsPage)
        )
        self.settings_button.pack(pady=10)


class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=bg_color)

        # settings
        self.on_top_var = tk.BooleanVar(value=self.parent.wm.on_top)

        self.create_widgets()

    def create_widgets(self):
        self.on_top_checkbutton = tk.Checkbutton(
            self,
            text="Always on top",
            bg=bg_color,
            variable=self.on_top_var,
        )
        self.on_top_checkbutton.pack(pady=10)

        self.back_button = tk.Button(
            self, text="Back to Home", command=lambda: self.parent.go_page(HomePage)
        )
        self.back_button.pack(pady=10)

        self.save_button = tk.Button(
            self,
            text="Save Settings",
            command=self.__save_settings,
        )
        self.save_button.pack(pady=10)

    def __save_settings(self):
        self.parent.wm.on_top = self.on_top_var.get()

        self.parent.wm.save_settings()
        self.parent.load_config()
