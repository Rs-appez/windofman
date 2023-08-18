
import PySimpleGUI as sg

class WindowConfig():

    def __init__(self) -> None:
        
        self.window = sg.Window(title="Windofman", layout=[[]], margins=(600, 100))

    def start(self):

        event,values = self.window.read()

        while 1 :
            if event ==sg.WIN_CLOSED:
                break
