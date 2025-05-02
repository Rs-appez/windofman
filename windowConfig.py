from windowManager import WindowManager
from confManager import ConfManager

import PySimpleGUI as sg
from tools import get_character_name


class WindowConfig:
    def __init__(self, wm: WindowManager) -> None:
        self.wm = wm
        self.active_characters = []
        self.layout = []
        self.window = None
        self.page = "home"

        self.__create_window(location=self.wm.location)

    def start(self):
        while 1:
            event, values = self.window.read()

            if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
                self.__set_location()
                break

            # Home page events
            elif event[:4] in ["Ign_", "Ini_"]:
                self.__save_initative(values)
            elif event[:4] == "Win_":
                self.wm.active_window_by_ch_name(event[4:])
            elif event == "refresh":
                self.__switch_page()
            elif event == "settings":
                self.page = "settings"
                self.__switch_page()
            elif event == "close all windows":
                self.wm.close_all_windows()

            # Settings page events
            elif event == "back_home":
                self.page = "home"
                self.__switch_page()
            elif event == "on_top_settings":
                self.__set_on_top(values["on_top_settings"])
                self.__save_settings(values)

        self.window.close()

    def __create_window(self, location=(None, None)):
        self.__get_layout()
        self.window = sg.Window(
            title="Windofman",
            layout=self.layout,
            margins=(10, 10),
            location=location,
            icon="windofman.png",
            keep_on_top=self.wm.on_top,
            enable_close_attempted_event=True,
        )

    def __save_initative(self, values):
        ConfManager.set_initiative(values)
        self.wm.sort_windows()

    def __save_settings(self, values):
        ConfManager.set_settings(values)

    def __set_on_top(self, on_top: bool = True):
        self.window.KeepOnTop = on_top

    def __set_location(self):
        location = self.window.CurrentLocation(more_accurate=True)
        self.__save_settings({"location": location})

    def __get_active_character(self):
        self.active_characters = []
        for window in self.wm.windows:
            character = get_character_name(self.wm.ewmh.getWmName(window))
            self.active_characters.append(character)

    def __switch_page(self):
        self.wm.get_data()
        self.__get_layout()
        old_location = self.window.CurrentLocation(more_accurate=True)
        self.window.close()
        self.__create_window(location=old_location)

    def __get_layout(self):
        match self.page:
            case "settings":
                self.__set_settings_page()
            case _:
                self.__set_home_page()

    def __set_home_page(self):
        self.__get_active_character()
        initiative = ConfManager.get_json()["Initiatives"]
        character_names = [[sg.Text("Character")]]
        inputs = [[sg.Text("Initiative")]]
        ignore_checkbox = [[sg.Text("Ignore")]]
        close_all_button = [
            [
                sg.Button(
                    button_text="close all windows",
                    button_color=("white", "black"),
                    font=("Helvetica", 10, "bold"),
                )
            ]
        ]
        buttons = [
            [sg.Button(button_text="refresh"), sg.Button(button_text="settings")]
        ]
        for character in self.active_characters:
            character_names.append(
                [sg.Text(text=character, key="Win_" + character, enable_events=True)]
            )
            inputs.append(
                [
                    sg.Input(
                        size=5,
                        key="Ini_" + character,
                        default_text=initiative[character]["initiative"],
                        enable_events=True,
                    )
                ]
            )
            ignore_checkbox.append(
                [
                    sg.Checkbox(
                        "",
                        key="Ign_" + character,
                        default=initiative[character]["ignore"],
                        enable_events=True,
                    )
                ]
            )

        self.layout = [
            [sg.Column(close_all_button, justification="right")],
            [sg.Column(character_names), sg.Column(inputs), sg.Column(ignore_checkbox)],
            [
                sg.HSeparator(),
            ],
            [sg.Column(buttons)],
        ]

    def __set_settings_page(self):
        settings = ConfManager.get_settings()

        title = [
            [
                sg.Text(
                    "Settings",
                    font="Any 11",
                )
            ]
        ]
        settings_checkbox = [
            [
                sg.Checkbox(
                    text=" Windofman always on top",
                    key="on_top_settings",
                    default=settings["on_top_settings"],
                    enable_events=True,
                )
            ]
        ]
        buttons = [[sg.Button(key="back_home", button_text="Back")]]

        self.layout = [
            [sg.Column(title, justification="center")],
            [sg.Column(settings_checkbox)],
            [
                sg.HSeparator(),
            ],
            [sg.Column(buttons)],
        ]
