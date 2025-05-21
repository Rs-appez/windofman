import tkinter as tk

from windowManager import WindowManager, DofusWindow

from difflib import get_close_matches

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
            f"+{localization[0]}+{localization[1]}"
            if localization[0] and localization[1]
            else ""
        )
        self.minsize(100, 100)
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
        frame_classes = (HomePage, SettingsPage,
                         ActionPage, LinkPage, ShortcutPage)
        for F in frame_classes:
            self.__make_frame(F)

    def load_config(self):
        self.attributes("-topmost", self.wm.on_top)

    def go_page(self, page):
        try:
            self.frames[page].tkraise()
        except KeyError:
            print(f"Page {page} not found.")

    def reload_frame(self, frame_class):
        if frame_class in self.frames:
            old = self.frames[frame_class]
            self.__make_frame(frame_class)
            old.destroy()

    def __make_frame(self, frame_class):
        frame = frame_class(self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_propagate(True)
        self.frames[frame_class] = frame

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

        # Initiatives
        self.datas = {}

        self.create_widgets()

    def create_widgets(self):
        # Label
        label_character = tk.Label(
            self, text="Character", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        label_character.grid(row=0, column=0, padx=10, pady=10)

        label_initiative = tk.Label(
            self, text="Initiative", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        label_initiative.grid(row=0, column=1, padx=10, pady=10)

        label_ignore = tk.Label(self, text="Ignore",
                                fg=LIGHT_COLOR, bg=DARK_COLOR)
        label_ignore.grid(row=0, column=2, padx=10, pady=10)

        label_link = tk.Label(self, text="Link", fg=LIGHT_COLOR, bg=DARK_COLOR)
        label_link.grid(row=0, column=3, padx=10, pady=10)

        # Separator
        separator = tk.Frame(self, bg=LIGHT_COLOR, height=2)
        separator_span = self.grid_size()[0]
        separator.grid(
            row=1, column=0, columnspan=separator_span, sticky="ew", padx=10, pady=5
        )

        # Characters
        for character in self.parent.wm.windows:
            character_name = character.name
            self.datas[character_name] = {}
            row = self.parent.wm.windows.index(character) + 2

            # Name
            label = tk.Label(
                self,
                text=character_name,
                fg=LIGHT_COLOR,
                bg=DARK_COLOR,
            )
            label.bind("<Button-1>", lambda e, c=character: c.activate())
            label.grid(row=row, column=0, padx=10, pady=10)

            # Initiative
            initiative_var = tk.StringVar(value=str(character.initiative))
            initiative_var.trace(
                "w",
                lambda *args, c=character: self.__save_initiatives(c),
            )
            self.datas[character_name]["ini"] = initiative_var
            initiative = tk.Entry(
                self,
                textvariable=initiative_var,
                width=5,
                bg=DARK_COLOR,
                fg=LIGHT_COLOR,
            )
            initiative.grid(row=row, column=1, padx=10, pady=10)

            # Ignore
            ignore_var = tk.BooleanVar(value=character.ignore)
            ignore_var.trace(
                "w",
                lambda *args, c=character: self.__save_initiatives(c),
            )
            self.datas[character_name]["ign"] = ignore_var
            ignore_checkbox = tk.Checkbutton(
                self, variable=ignore_var, bg=DARK_COLOR)
            ignore_checkbox.grid(row=row, column=2, padx=10, pady=10)

            # Link button
            link_button = tk.Button(
                self,
                text="Link",
                bg=DARK_COLOR,
                fg=LIGHT_COLOR,
                command=lambda c=character: self.__link_window(c),
            )
            link_button.grid(row=row, column=3, padx=10, pady=10)

        # Separator
        separator_row = self.grid_size()[1]
        separator = tk.Frame(self, bg=LIGHT_COLOR, height=2)
        separator.grid(
            row=separator_row,
            column=0,
            columnspan=separator_span,
            sticky="ew",
            padx=10,
            pady=5,
        )

        # Buttons
        btn_row = self.grid_size()[1]
        refresh_button = tk.Button(
            self,
            text="Refresh",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__refresh_windows,
        )
        refresh_button.grid(row=btn_row, column=0, padx=10, pady=10)

        action_button = tk.Button(
            self,
            text="Actions",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(ActionPage),
        )
        action_button.grid(row=btn_row, column=1, padx=10, pady=10)

        settings_button = tk.Button(
            self,
            text="Settings",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(SettingsPage),
        )
        settings_button.grid(row=btn_row, column=2, padx=10, pady=10)

        shortcut_button = tk.Button(
            self,
            text="Shortcuts",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(ShortcutPage),
        )
        shortcut_button.grid(row=btn_row, column=3, padx=10, pady=10)

    def __refresh_windows(self):
        self.parent.wm.get_data()
        self.parent.reload_frame(HomePage)

    def __save_initiatives(self, character: DofusWindow):
        data = self.datas[character.name]
        try:
            ini = int(data["ini"].get())
        except ValueError:
            ini = 0
        character.set_initiative(initiative=ini, ignore=data["ign"].get())
        self.parent.wm.sort_windows()

    def __link_window(self, window):
        self.parent.wm.window_to_link = window
        self.parent.go_page(LinkPage)


class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        # settings
        self.on_top_var = tk.BooleanVar(value=self.parent.wm.on_top)

        # Bindings
        self.bind_all("<Escape>", lambda event: self.parent.go_page(HomePage))

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


class ActionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))
        self.create_widgets()

        # Bindings
        self.bind_all("<Escape>", lambda event: self.parent.go_page(HomePage))

    def create_widgets(self):
        self.close_all_button = tk.Button(
            self,
            text="Close all windows",
            background=LIGHT_COLOR,
            foreground=DARK_COLOR,
            command=self.__close_all_windows,
        )
        self.close_all_button.grid(row=0, column=0, padx=10, pady=10)

        btn_row = self.grid_size()[1]
        self.back_button = tk.Button(
            self,
            text="Back to Home",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(HomePage),
        )
        self.back_button.grid(row=btn_row, column=0, padx=10, pady=10)

    def __close_all_windows(self):
        self.parent.wm.close_all_windows()


class LinkPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        self.characters = self.parent.wm.get_alls_characters_names()
        self.input = tk.StringVar()

        self.create_widgets()

        # Bindings
        self.bind_all("<Escape>", lambda event: self.parent.go_page(HomePage))
        self.bind_all("<Return>", lambda event: self.__set_name())

    def create_widgets(self):
        input_label = tk.Label(
            self, text="Enter your character name :", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        input_label.pack(padx=15, pady=5)
        input_field = tk.Entry(
            self,
            textvariable=self.input,
            width=30,
            bg=DARK_COLOR,
            fg=LIGHT_COLOR,
        )
        input_field.pack(pady=5)
        input_field.focus_set()

        btn_add_new = tk.Button(
            self,
            text="Add new",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__set_new_name,
        )
        btn_add_new.pack(pady=5, side=tk.RIGHT)

        self.list_input = tk.Listbox(
            self,
            listvariable=self.characters,
            selectmode=tk.SINGLE,
            height=5,
            width=30,
            bg=DARK_COLOR,
            fg=LIGHT_COLOR,
        )
        self.__update_list(self.characters)
        self.list_input.pack(pady=5)

        self.input.trace("w", self.__filter_list)
        self.list_input.bind(
            "<<ListboxSelect>>",
            lambda event: self.__set_name(),
        )

        self.back_button = tk.Button(
            self,
            text="Back",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(HomePage),
        )
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.link_button = tk.Button(
            self,
            text="Validate",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__set_name,
        )
        self.link_button.pack(side=tk.LEFT, padx=5, pady=5)

    def __update_list(self, items):
        self.list_input.delete(0, tk.END)
        for item in items:
            self.list_input.insert(tk.END, item)
        if self.list_input.size() > 0:
            self.list_input.select_set(0)

    def __filter_list(self, *args):
        name = self.input.get()
        matches = self.characters

        if name.strip():
            matches = get_close_matches(name, self.characters, n=5, cutoff=0.2)

        self.__update_list(matches)

    def __set_new_name(self):
        name = self.input.get()
        self.input.set("")
        self.__link_window(name)
        self.characters = self.parent.wm.get_alls_characters_names()

    def __set_name(self):
        selection = self.list_input.curselection()
        name = self.list_input.get(selection) if selection else None
        self.input.set("")
        if name:
            self.list_input.selection_clear(selection)
            self.list_input.selection_set(0)
            self.__link_window(name)

    def __link_window(self, name):
        if name:
            self.parent.wm.set_name_to_link(name)
            self.parent.wm.sort_windows()
            self.parent.reload_frame(HomePage)


class ShortcutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        # Bindings
        self.bind_all("<Escape>", lambda event: self.parent.go_page(HomePage))

        self.create_widgets()

    def create_widgets(self):
        self.back_button = tk.Button(
            self,
            text="Back",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(HomePage),
        )
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)
