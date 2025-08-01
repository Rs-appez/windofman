import tkinter as tk

from windowManager import WindowManager, DofusWindow
from keyboardManager import KeyboardManager
from confManager import ConfManager

from difflib import get_close_matches

DARK_COLOR = "#1f1f28"
LIGHT_COLOR = "#dcd7ba"


class GUIApp(tk.Tk):
    def __init__(self, wm: WindowManager, km: KeyboardManager):
        super().__init__()
        self.wm = wm
        self.km = km

        self.edit_key = None

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
        self.__init_bindings()
        self.go_page(HomePage)
        self.mainloop()

    def __init_frame(self):
        frame_classes = (
            HomePage,
            SettingsPage,
            ActionPage,
            LinkPage,
            ShortcutPage,
            AssignKeyPage,
        )
        for F in frame_classes:
            self.__make_frame(F)

    def __init_bindings(self):
        self.unbind_all("<Return>")
        self.unbind_all("<KeyPress>")
        self.bind_all("<Escape>", lambda event: self.go_page(HomePage))

    def load_config(self):
        self.attributes("-topmost", self.wm.on_top)

    def go_page(self, page):
        try:
            self.__init_bindings()
            try:
                self.frames[page].set_bindings()
            except AttributeError:
                pass
            self.frames[page].tkraise()
        except KeyError:
            print(f"Page {page} not found.")

    def reload_frame(self, frame_class):
        if frame_class in self.frames:
            # old = self.frames[frame_class]
            # self.__make_frame(frame_class)
            # old.destroy()
            frame = self.frames[frame_class]
            for child in frame.winfo_children():
                child.destroy()
            frame.create_widgets()

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
            label.bind(
                "<Button-1>", lambda e, c=character: self.parent.wm.activate_window(
                    c)
            )
            label.grid(row=row, column=0, padx=10, pady=10, sticky="w")

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
                insertbackground=LIGHT_COLOR,
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
        btn_frame = tk.Frame(self, bg=DARK_COLOR)
        btn_row = self.grid_size()[1]
        btn_frame.grid(row=btn_row, column=0, columnspan=separator_span)
        refresh_button = tk.Button(
            btn_frame,
            text="Refresh",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__refresh_windows,
        )
        refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        action_button = tk.Button(
            btn_frame,
            text="Actions",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(ActionPage),
        )
        action_button.pack(side=tk.LEFT, padx=10, pady=10)

        settings_button = tk.Button(
            btn_frame,
            text="Settings",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(SettingsPage),
        )
        settings_button.pack(side=tk.LEFT, padx=10, pady=10)

        shortcut_button = tk.Button(
            btn_frame,
            text="Shortcuts",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(ShortcutPage),
        )
        shortcut_button.pack(side=tk.LEFT, padx=10, pady=10)

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

    def set_bindings(self):
        self.bind_all("<Return>", lambda event: self.__set_name())
        self.input_field.focus_set()

    def create_widgets(self):
        input_label = tk.Label(
            self, text="Enter your character name :", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        input_label.pack(padx=15, pady=5)
        self.input_field = tk.Entry(
            self,
            textvariable=self.input,
            width=30,
            bg=DARK_COLOR,
            fg=LIGHT_COLOR,
            insertbackground=LIGHT_COLOR,
        )
        self.input_field.pack(pady=5)

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
            self.parent.go_page(HomePage)


class ShortcutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        self.next_key = "F2"
        self.previous_key = "F3"

        self.create_widgets()

    def create_widgets(self):
        self.__get_shortcuts()
        next_label = tk.Label(
            self, text="Next character : ", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        next_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        next_shorcut_label = tk.Label(
            self, text=self.next_key, fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        next_shorcut_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        next_shorcut_edit_button = tk.Button(
            self,
            text="Edit",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.__edit_shortcut("next"),
        )
        next_shorcut_edit_button.grid(
            row=0, column=2, padx=5, pady=5, sticky="w")

        prev_label = tk.Label(
            self, text="Previous character : ", fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        prev_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        prev_shorcut_label = tk.Label(
            self, text=self.previous_key, fg=LIGHT_COLOR, bg=DARK_COLOR
        )
        prev_shorcut_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        prev_shorcut_edit_button = tk.Button(
            self,
            text="Edit",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.__edit_shortcut("previous"),
        )
        prev_shorcut_edit_button.grid(
            row=1, column=2, padx=5, pady=5, sticky="w")

        # btns
        btn_frame = tk.Frame(self, bg=DARK_COLOR)
        btn_row = self.grid_size()[1]
        btn_frame.grid(row=btn_row, column=0, columnspan=3, pady=10)
        self.back_button = tk.Button(
            btn_frame,
            text="Back",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=lambda: self.parent.go_page(HomePage),
        )
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.reset_button = tk.Button(
            btn_frame,
            text="Reset shortcuts",
            bg=LIGHT_COLOR,
            fg=DARK_COLOR,
            command=self.__reset_shortcuts,
        )
        self.reset_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def __edit_shortcut(self, key):
        self.parent.edit_key = key
        self.parent.reload_frame(AssignKeyPage)
        self.parent.go_page(AssignKeyPage)

    def __get_shortcuts(self):
        keys = ConfManager.get_keybinds()
        self.next_key = keys.get("next")
        self.previous_key = keys.get("previous")

    def __reset_shortcuts(self):
        ConfManager.reset_keybinds()
        self.parent.km.set_keys()
        self.parent.reload_frame(ShortcutPage)


class AssignKeyPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg=self.parent.cget("bg"))

        self.create_widgets()

    def set_bindings(self):
        self.bind_all(
            "<Escape>", lambda event: self.parent.go_page(ShortcutPage))
        self.bind_all("<KeyPress>", self.__assign_key)

    def create_widgets(self):
        self.label = tk.Label(
            self,
            text=f"Press a key to assign to {self.parent.edit_key}...",
            fg=LIGHT_COLOR,
            bg=DARK_COLOR,
        )
        self.label.pack(padx=15, pady=5)

    def __assign_key(self, event):
        key = event.char or event.keysym

        ConfManager.set_keybinds({self.parent.edit_key: key})
        self.parent.km.set_keys()
        self.parent.reload_frame(ShortcutPage)
        self.parent.go_page(ShortcutPage)
