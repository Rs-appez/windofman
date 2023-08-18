from windowManager import WindowManager
from confManager import ConfManager

import PySimpleGUI as sg
from tools import get_character_name

class WindowConfig():

    def __init__(self,wm : WindowManager) -> None:
        self.wm = wm
        self.active_characters = []
        self.layout = []
        self.window = None

        self.__create_window()

    def start(self):
        while 1 :
            event,values = self.window.read()
            if event == 'save':
                self.__save(values)
            elif event == 'refresh':
                self.__refresh()
            elif event ==sg.WIN_CLOSED:
                break
        self.window.close()

    def __create_window(self,location= (None, None)):
        self.__get_layout()
        self.window = sg.Window(title="Windofman", layout=self.layout, margins=(10, 10),location=location)

    def __get_active_character(self):
        
        self.active_characters = []
        for window in self.wm.windows:
            character = get_character_name(self.wm.ewmh.getWmName(window))
            self.active_characters.append(character)

    def __get_layout(self):
        self.__get_active_character()
        initiative = ConfManager.get_json()
        character_names = []
        inputs = []
        buttons = [
            [sg.Button(button_text="refresh"),sg.Button(button_text="save")]
            ]
        for character in self.active_characters:
            character_names.append([sg.Text(character)])
            inputs.append([sg.Input(size = 5,key=character,default_text=initiative[character])])

        self.layout = [
            [sg.Column(character_names),
            sg.Column(inputs),
            ],
            [sg.HSeparator(),],
            [
            sg.Column(buttons)
            ]
        ]

    def __save(self,values):
        ConfManager.set_initiative(values)
        self.wm.sort_windows()

    def __refresh(self):
        self.wm.get_windows()
        old_location = self.window.CurrentLocation(more_accurate = True)
        self.window.close()
        self.__create_window(location=old_location)
 