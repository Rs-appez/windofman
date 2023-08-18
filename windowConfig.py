
import PySimpleGUI as sg

class WindowConfig():

    def __init__(self) -> None:
        
        self.window = sg.Window(title="Windofman", layout=[[]], margins=(600, 100))

    def start(self):

        self.window.read()