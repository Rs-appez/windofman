import tkinter as tk
from windowManager import WindowManager

bg_color = "#1f1f28"


class GUIApp(tk.Tk):
    def __init__(self, wm: WindowManager):
        super().__init__()
        self.wm = wm

        self.title("Windofman")
        self.geometry("300x200")
        self.configure(bg=bg_color)

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
        self.create_widgets()

    def create_widgets(self):
        self.on_top_checkbutton = tk.Checkbutton(
            self, text="Always on top", bg=bg_color
        )
        self.on_top_checkbutton.pack(pady=10)

        self.back_button = tk.Button(
            self, text="Back to Home", command=lambda: self.parent.go_page(HomePage)
        )
        self.back_button.pack(pady=10)
